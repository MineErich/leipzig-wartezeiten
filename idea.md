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

###### interprete.py
- ließt alle json's aus rawdata ein und erstellt verarbeitbare Daten
- wird geseichert in all_data.json

- Ideen dazu:
- es sollte eine json mit den Daten der letzten 30 Tage geben und eine für all-time
- in der json sind die Werte für alle Bürgerbüros (Bb)
- interprete.py ließt immer nur die neusten rawdata-json's ein und ergänzt sie
- dazu sollte in 30days.json und alltime.json ein timestamp mit dem neusten Datenabruf drin stehen


### Progress
- [DONE] get_data
- [DONE] interprete
- [OPEN] csv-export
- [OPEN] graph
- [OPEN] web-view 