# Init Dateien erlauben es, Python-Objekte gebündelt zu importieren.
# Außerdem können sie beschreiben, welche Objecte aus den Unterordnern exportiert werden.

from src.ui.dashboard_app import DashboardApp
from src.ui.semester_table import SemesterTable
from src.ui.study_bars import StudyBars
from src.ui.study_stats import StudyStats

__all__ = [
    "DashboardApp",
    "SemesterTable",
    "StudyBars",
    "StudyStats"
]
