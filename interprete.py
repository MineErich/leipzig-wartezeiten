import logging
import json
from datetime import datetime
from pathlib import Path
import os

"""
IN:
rawdata/*.json

OUT:
30days.json
    für jedes Bb
        30 tage á 24h, also 720 datenpunkte
alltime.json
    für jedes Bb
        alltime á 24h, also 24*n datenpunkte

Aufbau JSON
timestamp
location
    $name$
        $datetime$
            active_counter_count	    (sind das die vorab gemachten Termine?)
            walkin_waiting_count	    (!)
            walkin_serving_count	    (Anzahl Sachbearbeiter*innen)
            walkin_average_waitingtime	(?)
            walkin_end_count	        (?)
            predicted_waiting_time	    (!)
    $name$
        $datetime$
            active_counter_count
            walkin_waiting_count
            walkin_serving_count  
            walkin_average_waitingtime
            walkin_end_count
            predicted_waiting_time
    ...
"""


# default logfile: lwartezeiten.log
logfile = "lwinterprete.log"

# logging conf
FORMAT = '%(asctime)s %(levelname)s [%(funcName)s] %(message)s'
logging.basicConfig(filename=logfile, encoding='utf-8', level=logging.INFO, format=FORMAT)

# get current dir
source_path = Path(__file__).resolve()
source_dir = source_path.parent.absolute()

# Verzeichnis mit den Eingabedateien
input_directory = str(source_dir)+'/rawdata/'

# Prüfen, ob die Datei 30days.json existiert und laden, oder eine leere Struktur erstellen
try:
    with open("30days.json", "r", encoding="utf-8") as file:
        data_30days = json.load(file)
    last_timestamp = data_30days.get("timestamp", "000000_00_00")
except FileNotFoundError:
    data_30days = {"timestamp": "000000_00_00"}
    last_timestamp = "000000_00_00"

# Funktion zum Umwandeln eines Timestamps im Dateinamenformat in ein datetime-Objekt
def parse_timestamp(timestamp_str):
    return datetime.strptime(timestamp_str, "%y%m%d_%H_%M")

# Aktuellsten Timestamp der verarbeiteten Dateien speichern
latest_timestamp = parse_timestamp(last_timestamp)

# Alle Dateien im Verzeichnis durchgehen
for filename in os.listdir(input_directory):
    if filename.endswith(".json"):
        # Timestamp aus dem Dateinamen extrahieren
        file_timestamp_str = filename.replace(".json", "")
        file_timestamp = parse_timestamp(file_timestamp_str)

        # Nur Dateien verarbeiten, die neuer sind als der letzte gespeicherte Timestamp
        if file_timestamp > latest_timestamp:
            # JSON-Daten aus der Datei laden
            with open(os.path.join(input_directory, filename), "r", encoding="utf-8") as json_file:
                original_data = json.load(json_file)

            # Datum und Uhrzeit im gewünschten Format generieren
            formatted_date_time = file_timestamp.strftime("%y%m%d-%H-%M")

            # Daten für jeden Standort hinzufügen
            for location, values in original_data["locations"].items():
                # Liste für den Standort erstellen, falls sie noch nicht existiert
                if location not in data_30days:
                    data_30days[location] = []

                # Datenstruktur mit Datum und Uhrzeit als Schlüssel und Werten als Objekt
                data_entry = {
                    formatted_date_time: {
                        "active_counter_count": values["active_counter_count"],
                        "walkin_waiting_count": values["walkin_waiting_count"],
                        "walkin_serving_count": values["walkin_serving_count"],
                        "walkin_average_waitingtime": values["walkin_average_waitingtime"],
                        "walkin_end_count": values["walkin_end_count"],
                        "predicted_waiting_time": values["predicted_waiting_time"]
                    }
                }
                
                # Daten zur Liste des Standorts hinzufügen
                data_30days[location].append(data_entry)

            # Den aktuellsten Timestamp aktualisieren, falls die Datei neuer ist
            if file_timestamp > latest_timestamp:
                latest_timestamp = file_timestamp

# Aktualisieren des Timestamps in 30days.json
data_30days["timestamp"] = latest_timestamp.strftime("%y%m%d_%H_%M")

# Die geänderten Daten in 30days.json speichern
with open("30days.json", "w", encoding="utf-8") as file:
    json.dump(data_30days, file, ensure_ascii=False, indent=4)

logging.info("Daten erfolgreich hinzugefügt und Timestamp aktualisiert.")