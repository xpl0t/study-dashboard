from src.models.semester import Semester
from dataclasses_json import dataclass_json
from dataclasses import dataclass, field
from datetime import datetime
from typing import List
from dateutil.relativedelta import relativedelta


@dataclass_json
@dataclass
class Studiengang:
    name: str = "Python verstehen 🐍"
    beginn: datetime = field(default_factory=datetime.now)
    # Der Standardwert für das Zielende ergibt sich aus dem aktuellen Zeitstempel + 3 Jahre, da dies die Regelstudienzeit ist.
    zielende: datetime = field(default_factory=lambda: datetime.now() + relativedelta(years=3))
    zielnote: float = 2.0
    ects_insgesamt: int = 180

    semester: List[Semester] = field(default_factory=list)
