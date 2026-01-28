---
title: Abschlussprojekt
sidebar_position: 3
---
# Abschlussprojekt: Übertragungsfunktionsrechner über Freedyn

## Kurzbeschreibung
Das Programm dient zur Schrittweisen Berechnung einer Übertragungsfunktion von einem Freedyn Model.
Das Freedyn Model darf nur einen Eingang und einen Ausgang haben.
Eine Übertragungsfunktion von einem Model benötigt man sehr oft (z.B. Prüfstandstechnik, Inverse Kinematik, Regelungstechnik, ....).
Zusätzlich interresiert mich die Software Freedyn und die möglichkeit mit Freedyn zu arbeiten über eine andere Software (z.B. Scilab, Python, ...) 

## Funktionen
Auflistung der wichtigsten Funktionen/Fähigkeiten
Hervorhebung interessanter Aspekte

### Rosa Rauschen und Lesen der Messung von Freedyn
Der Orginal Code in Scilab wurde von Professor Witteween uns bei den Fallstudien im 2. Semester zur verfügung gestellt.

## Verwendete Technologien
Das Programm wurde in Visual-Studio-Code mit der Programmiersprache Python programmiert.

### Verwendete Python-Bibliotheken
- sys
- os
- pathlib
- subprocess
- numpy
- matplotlib
- PyQt6
    
### Verwendete Techniken
Die Interaktion und Bildausgabe erfolgt über QMainWindow.
Das Program ist in mehre Funktionen strukturiert. 

## Installation und Einrichtung

```bash
cd final-assignment/your-name/code
pip install -r requirements.txt  # wen noch kein Virtual Environment, mit den richtigen Pakten, exisitert.
```

Um den Programteil Siumlation durchführen zu können, müssen für den jeweiligen Rechner zwei Anpassungen vorgenommen werden.
1. Im Code "main" muss in der Funktion "run_simulation" Zeile 406 die aktuelle Adresse von FreeDyn.exe ersetzt werden.
2. Freedyn muss gestartet werden und das Simulationsfile geöffnet werden. Danach muss unter "Data Object/spline" die Anregungsdatei unter data ausgewählt werden.

## Verwendung
Nach der Vorbereitung kann das Program gestart werden, indem main ausgeführt wird.
```bash
python main.py
```
Unter Datei muss das richtige Simulationsfile ausgewählt werden.
Danach kann das Programm muss das Programm Schritt für Schritt (von oben nach unten) durchgegangen werden.
### Thema = Rauschen
- Unter dem Thema Rauschen können die Parameter für das Rauschsignal an die Anwendung Angepasst werden.
- Danach kann man die Taste "Rauschenerzeugen" klicken. Das Programm erstellt dann das Rauschen. Das Rauschsignal ist nur im Programm gespeichert.
- Als nächstes kann man das Rauschen in der rechten Grafik darstellen lassen.
- Um das Rauschsignal dann in der Simulation verwenden zu können, muss das Rauschsignal exportiert werden. Als Name muss der Name verwendet werden mit dem der Eingang in Freedyn eingelesen wird.
### Thema = Simulation
- Die Simulation kann ausgeführt werden.
- Wenn die Simulation fertig ist, erscheint dann in der unteren linken Ecke die Meldung "Simulation erfolgreich"
- Das einlesen des Ergebnis (measure_file) findet automatisch statt.
- Danach kann das Simulationsergebnis dargstellt werden.
### Thema = Übertragungsfunktion
- Die Übertragungsfunktion kann berechnet werden.
- Dann kann die Übertragungsfunktion dargestellt werden.
- Als letztes kann die Übertragungsfunktion exportiert werden.

### Zusatzinformationen
- Meldungen erscheinen in der unteren linken Ecke.
- Das Programm kann nur von oben nach unten ausgeführt werden. Da kein Import von Datein (Rauschsignal, Übertragungsfunktion) implementiert ist und die Sicherheitüberprüfungen auf intern (im Programm) gespiecherte Variablen zugrundeliegt.

## Daten
- Verwendet werden folgende Daten "Dateiname.fds"
- Die Daten befinden isch im Ordner Data.
- Die Ausgaben (Rauschsignal, Übertragungsfunktion) werden als txt gespeichert.

## Implementierungsdetails

    Interessante Algorithmen oder Ansätze
    Herausforderungen, die Sie gelöst haben
    Überlegungen zur Leistung

## Screenshots
Das Fenster im Ausgangszustand:
![Ausgangsfenster](assets/Ausgang_Fenster.png)
<img src="assets/Ausgang_Fenster.png" alt="Ausgangsfenster" width="500">

Das Fenster unter dem Thema:Rausche nach dem das Rauschsignal exportiert wurde:
![Ausgangsfenster](assets/Rauschen_Fenster.png)

## Zukünftige Verbesserungen (optional)
Weitere Ideen die im Programm implementiert werden könnten sind:
- Extra importieren vom Rauschsignal und oder der Übertragungsfunktion. Damit ältere Ergebnisse auch dargestellt werden können.
- Das Programm so aufbauen, dass das Progamm nicht immer von vorne durchlaufen werden muss. Mit dem geht einher, dass die vordere Idee (importierern) realisiert ist.

