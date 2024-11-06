import logging
import json
from datetime import datetime
from pathlib import Path
import os

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

# Prüfen, ob die Datei alltime.json existiert und laden, oder eine leere Struktur erstellen
try:
    with open("alltime.json", "r", encoding="utf-8") as file:
        data_alltime = json.load(file)
    last_timestamp = data_alltime.get("timestamp", "000000_00_00")
except FileNotFoundError:
    data_alltime = {"timestamp": "000000_00_00"}
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
                if location not in data_alltime:
                    data_alltime[location] = []

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
                data_alltime[location].append(data_entry)

            # Den aktuellsten Timestamp aktualisieren, falls die Datei neuer ist
            if file_timestamp > latest_timestamp:
                latest_timestamp = file_timestamp

# Aktualisieren des Timestamps in alltime.json
data_alltime["timestamp"] = latest_timestamp.strftime("%y%m%d_%H_%M")

# Die geänderten Daten in alltime.json speichern
with open("alltime.json", "w", encoding="utf-8") as file:
    json.dump(data_alltime, file, ensure_ascii=False, indent=4)

logging.info("Daten erfolgreich hinzugefügt und Timestamp aktualisiert.")