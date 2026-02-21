from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.widget import Widget
from textual.widgets import Static
from src.logic import StudiumLogic
from rich.text import Text

class StudyStats(Widget):
    """"Widget welched die 4 Studienstatistiken darstellt."""

    DEFAULT_CSS = """
    Horizontal {
        height: auto;
    }

    .box {
        width: 1fr;
        border: solid;
        content-align: center middle;
        padding: 1;
    }

    .box-blue {
        border: solid lightblue;
    }

    .box-green {
        border: solid lightgreen;
    }

    .box-coral {
        border: solid lightcoral;
    }

    .box-yellow {
        border: solid lightyellow;
    }
    """

    def __init__(self, logic: StudiumLogic):
        super().__init__()
        self.logic = logic

    def compose(self) -> ComposeResult:
        # Durch die compose Funktion, werden die Anzeigeelemete definiert.

        self.days_adv_box = Static("", classes="box box-blue")
        self.time_5_ects_box = Static("", classes="box box-green")
        self.avg_grade = Static("", classes="box box-coral")
        self.max_avg_remain_box = Static("", classes="box box-yellow")

        self.days_adv_box.border_title = "Vorsprung / Verzug"
        self.time_5_ects_box.border_title = "Zeit für 5 ECTS"
        self.avg_grade.border_title = "Durchschnittsnote"
        self.max_avg_remain_box.border_title = "Maximalrestdurchschnitt"

        with Horizontal():
            yield self.days_adv_box
            yield self.time_5_ects_box
            yield self.avg_grade
            yield self.max_avg_remain_box

    def on_mount(self):
        self.update_data()

    def update_data(self):
        sg = self.logic.get_studiengang()
        days_adv = self.logic.get_days_advance()
        time_5_ects = self.logic.get_days_5_ects()
        avg_grade = self.logic.get_average_grade()
        max_avg_remain = self.logic.get_max_remaining_average()

        # Farben für die positiv/negativ Darstellung der Metrikwerte.
        lightred_hex = "#FF8585"
        lightgreen_hex = "#8DFFA6"

        # Metrikwerte aktualisieren.
        self.days_adv_box.update(Text(f"{days_adv} Tage", style=lightgreen_hex if days_adv >= 0 else lightred_hex))
        self.time_5_ects_box.update(f"{time_5_ects} Tage")
        self.avg_grade.update(Text(f"{avg_grade:.2f}", style="" if avg_grade < sg.zielnote else lightred_hex))
        self.max_avg_remain_box.update(f"{max_avg_remain:.2f}")
