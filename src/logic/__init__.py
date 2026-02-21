# Init Dateien erlauben es, Python-Objekte gebündelt zu importieren.
# Außerdem können sie beschreiben, welche Objecte aus den Unterordnern exportiert werden.

from .studium_logic import StudiumLogic

__all__ = [
    "StudiumLogic"
]

