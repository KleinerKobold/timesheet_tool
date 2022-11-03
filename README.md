# timesheet_tool
groups timesheet.io app exports per day and project

Dieses Tool hilft dabei erfasste Arbeitszeit von der Timesheet-App leichter zu analysieren

# Anleitung

## App bekommen

[Android](https://play.google.com/store/apps/details?id=com.rauscha.apps.timesheet&referrer=utm_source%3Dlanding%26utm_medium%3Dbanner%26utm_campaign%3Ddownload)

[Apple](https://timesheet.io/img/webp/appstore.webp)

## Konfiguration der App
Die App kann man wie gewünscht einstellen, es gibt nur hier eine Einstellung die getroffen werden soll:

<img src="img/Einstellungen.jpg" alt="Einstellungen" style="width:200px;"/>

- Datumsformat yyyy-MM-dd
- Format Dauer XX.XX h

## Export aus der App
Die App kann dann die Daten exportieren:

<img src="img/Export.jpg" alt="Export" style="width:200px;"/>


Dabei sollte man den Zeitrahmen einstellen. Der Export erfolgt nach XLS.

Die Felder für den Export sind wie folgt zu treffen:

<img src="img/Export_einstellung_1.jpg" alt="Export_einstellung_1" style="width:200px;"/>
<img src="img/Export_einstellung_2.jpg" alt="Export_einstellung_2" style="width:200px;"/>


## Python Skript

### Bauen und Installation

Es sollte auf dem System ein Python installiert sein > 3.9 und git

```
  git clone https://github.com/KleinerKobold/timesheet_tool.git
  cd timesheet_tool
  pip install --upgrade setuptools
  pip install --upgrade build
  python -m build
  pip install . 
```

### Konfiguration 

Danach sollte die config.yaml bereitgestellt werden, eine Vorlage ist unter config.example.yaml zu finden.
Die Datei wird im Pfad `c:/users/user/.timesheet/config.yaml` erwartet
Das Programm kann aber auch ohne eine Konfiguration arbeiten.

#### Konfiguration von Farben

Die Farben in der Excel Datei können in der Konfigration angepasst werden.
```
colors:
  - "Team 1": "00CCFF"
  - "Team 2": "f2b24b"
  - "Team 2 customer": "f2b24b"
  - "Division 1": "00CCFF"
  - "Intern": "f2594b"
```
Hier kann man in der Konfig die Farben für Projekte einstellen. Dies Hilft dabei schneller die Projekte in andere Systeme abzuschreiben.

#### Konfiguration von CSV Exporten

Folgender Teil in der Konfiguration steuert den Export nach CSV.
```
csv:
  "fileName": "export.csv"
  "round": True
  elements:
    "Team 1": "0001"
    "Team 2": "0002"
    "Team 2 customer": "1002"
```
Es werden nur Elemente exportiert, die entsprechend unter Elements aufgeführt sind. Dabei werden die Namen der Projekte in die Werte in Elements geändert. So können Kontennummern angegeben werden. 
Der Parameter Round sagt, ob die Stunden auf die nächsten vollen 1/4 aufgerundet werden sollen oder nicht. 
Der Parameter Filename nennt den Speicherot der CSV Datei.

### Skript ausführen

Man legt den Excel Export der Daten in ein Verzeichnis und fürt dort `timesheet` aus. 
Auf der Konsole gibt es einige Ausgaben, dazu kommt eine excel Datei als Ausgabe, Calced_timesheet.xlsx.