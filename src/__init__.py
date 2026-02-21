# Init Dateien erlauben es, Python-Objekte gebündelt zu importieren.
# Außerdem können sie beschreiben, welche Objecte aus den Unterordnern exportiert werden.

from src.repository import ConfigRepository, JsonConfigRepository
from src.models import Studiengang, Modul, Prüfungsleistung, Semester
from src.ui import DashboardApp

__all__ = [
    "Studiengang",
    "Semester",
    "Modul",
    "Prüfungsleistung",
    "ConfigRepository",
    "JsonConfigRepository",
    "DashboardApp",
]
