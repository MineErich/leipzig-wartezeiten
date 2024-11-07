###### Idee

1. aktuelle Anzahl Personen und Wartezeit spiegeln
2. stündlich Daten sammeln

###### zu 2.

- stündliche Daten speichern
- Graph bauen, wann wie viele Leute da sind

###### Quelle

- https://dev.lehst.de/Projects/Wartezeiten/ {json}


##### automatisierte Speicherung

###### crawler.py
- speichert einfach nur bei Aufruf das aktuelle json ab
- sollte nur zwischen 7 und 20 Uhr tätig sein!!

###### get_data.py

- ruft bei Ausführung api ab
- speichert relevante Daten in daily/monthly/alltime ab
- speichert json ab in Ordner "rawdata"
- sollte nur zwischen 7 und 20 Uhr tätig sein!!

##### Aufbau raw JSON

<code>
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

- [DONE] crawler (py)
- [DONE] get_data (py)
- [WHY?] interprete (py)
- [DONE] alltime,montly,daily (py)
- [OPEN] csv-export (py)
- [OPEN] graph (js)
- [OPEN] web-view (js)

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
