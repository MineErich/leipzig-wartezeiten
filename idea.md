###### Idee

1. aktuelle Anzahl Personen und Wartezeit spiegeln
2. stündlich Daten sammeln

###### zu 2.

- stündliche Daten speichern
- Graph bauen, wann wie viele Leute da sind

###### Quelle

- https://dev.lehst.de/Projects/Wartezeiten/ {json}


##### automatisierte Speicherung

###### get_data.py

- ruft bei Ausführung api ab
- speichert json ab in Ordner "rawdata"
- sollte nur zwischen 7 und 20 Uhr tätig sein!!

###### interprete.py

- ließt alle json's aus rawdata ein und erstellt verarbeitbare Daten
- wird geseichert in all_data.json

- Ideen dazu:
- es sollte eine json mit den Daten der letzten 30 Tage geben und eine für all-time
- in der json sind die Werte für alle Bürgerbüros (Bb)
- interprete.py ließt immer nur die neusten rawdata-json's ein und ergänzt sie
- dazu sollte in 30days.json und alltime.json ein timestamp mit dem neusten Datenabruf drin stehen

<code>
IN:
rawdata/*.json

OUT:
alltime.json
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
</code>

### Progress

- [DONE] get_data
- [DONE] interprete
- [DONE] alltime entält alle
- [OPEN] 30days soll nur letzte 30 Tage enthalten
- [OPEN] csv-export
- [OPEN] graph
- [OPEN] web-view 

### Speicherprognose

1. alle raw json
- 5,8 kb pro Aufruf
- 5,8kb*24 = 139,2kb pro Tag 
- 139,2kb *365,25 = 50842,8 pro Jahr
- = ~50mb pro Jahr

2. alltime.json
- ?

3. 30days.json
- sollte feste größe haben
