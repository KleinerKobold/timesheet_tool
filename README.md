# timesheet_tool
groups timesheet.io app exports per day and project

Dieses Tool hilft dabei erfasste Arbeitszeit von der Timesheet-App leichter zu analysieren

# Anleitung

## Konfiguration 
Die App kann man wie gewünscht einstellen, es gibt nur hier eine Einstellung die getroffen werden soll:
[Einstellung](img/Einstellungen.jpg)
- Datumsformat yyyy-MM-dd
- Format Dauer XX.XX h

## Export 
Die App kann dann die Daten exportieren:
![Export](img/Export.jpg =250x)

Dabei sollte man den Zeitrahmen einstellen. Der Export erfolgt nach XLS.

Die Felder für den Export sind wie folgt zu treffen:

![Export_1](img/Export_einstellung_1.jpg =250x)
![Export_2](img/Export_einstellung_2.jpg =250x)

## Python Skript
Die Python abhängigkeiten müssen installiert werden. Dies kann man einfach machen mit dem Befehl

```
pip install -r requirements.txt
```

Danach sollte die config.yaml bereitgestellt werden, eine vorlage ist unter config.example.yaml zu finden.

Die Exportierten Daten kommen in den Ordner des Skriptes, die Berechnungen starten dann mit 

```
python generate.py
```

Auf der Konsole gibt es einige Ausgaben, dazu kommt eine excel Datei als Ausgabe, Calced_timesheet.xlsx.