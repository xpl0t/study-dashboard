# Init Dateien erlauben es, Python-Objekte gebündelt zu importieren.
# Außerdem können sie beschreiben, welche Objecte aus den Unterordnern exportiert werden.

from .modul import Modul
from .semester import Semester
from .studiengang import Studiengang
from .prüfungsleistung import Prüfungsleistung

__all__ = [
    "Modul",
    "Semester",
    "Studiengang",
    "Prüfungsleistung"
]
