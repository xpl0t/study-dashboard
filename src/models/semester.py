from src.models.modul import Modul
from dataclasses_json import dataclass_json
from dataclasses import dataclass, field
from typing import List


@dataclass_json
@dataclass
class Semester:
    nummer: int
    module: List[Modul] = field(default_factory=list)
