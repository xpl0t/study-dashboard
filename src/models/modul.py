from typing import Optional
from src.models.prüfungsleistung import Prüfungsleistung
from dataclasses_json import dataclass_json
from dataclasses import dataclass


@dataclass_json
@dataclass
class Modul:
    id: str
    name: str
    ects: int
    angerechnet: bool

    leistung: Optional[Prüfungsleistung] = None
