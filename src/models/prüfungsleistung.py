from datetime import datetime
from dataclasses_json import dataclass_json
from dataclasses import dataclass, field


@dataclass_json
@dataclass
class Prüfungsleistung:
    note: float
    datum: datetime = field(default_factory=datetime.now)
