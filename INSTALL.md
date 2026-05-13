# Installationsanleitung

## Python installieren

Laden Sie sich eine Python-Version ab Version *3.14* von [python.org](https://www.python.org/downloads/) herunter und installieren Sie diese.

## Quellcode herunterladen

Laden Sie sich den Quellcode der Anwendung über den Link [github.com/xpl0t/study-dashboard.zip](https://github.com/xpl0t/study-dashboard/archive/refs/heads/main.zip) als Zip-Datei herunter.

Entpacken Sie die Datei in ein beliebiges Verzeichnis.

## Kommandozeile öffnen

Öffnen Sie ein Powershell-Fenster in dem Verzeichnis, in dem sich die Datei `main.py` befindet.

## Virtuelle Umgebung erstellen

Um die Laufzeitabhängigkeiten isoliert vom restlichen System zu installieren, wird eine virtuelle Umgebung (Venv) benötigt. Erstellen Sie diese mit folgendem Kommandozeilenbefehl:

`python -m venv .venv`

## Virtuelle Umgebung laden

Bevor Sie die Abhängigkeiten installieren oder die Anwendung ausführen können, muss die soeben erstellte virtuelle Umgebung geladen bzw. aktiviert werden. Führen Sie dazu folgenden Befehl aus:

`.venv/Scripts/Activate.ps1`

## Laufzeitabhängigkeiten installieren

Die Anwendung erfordert die Laufzeitabhängigkeiten *textual*, *dataclasses-json* und *python-dateutil*. Diese Abhängigkeiten werden mit folgendem Kommandozeilenbefehl in die aktivierte virtuelle Umgebung installiert:

`pip install -r requirements.txt`

## Anwendung ausführen

Nachdem nun alle Voraussetzungen erfüllt sind, kann die Anwendung mit folgendem Befehl gestartet werden:

`python main.py`
