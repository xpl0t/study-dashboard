# Init Dateien erlauben es, Python-Objekte gebündelt zu importieren.
# Außerdem können sie beschreiben, welche Objecte aus den Unterordnern exportiert werden.

from .config_repository import ConfigRepository
from .json_config_repository import JsonConfigRepository

__all__ = [
    "ConfigRepository",
    "JsonConfigRepository"
]
