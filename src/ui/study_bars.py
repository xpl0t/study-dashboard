from textual.app import ComposeResult
from textual.containers import Container, Horizontal
from textual.widget import Widget
from textual.widgets import Label, ProgressBar
from src.logic import StudiumLogic


class StudyBars(Widget):
    """"Widget welches den ECTS- und Tagesfortschrittsbalken darstellt."""

    DEFAULT_CLASSES="h-auto"
    DEFAULT_CSS="""
        StudyBars Bar {
            /* Benötigt, damit die Fortschrittsbalken den leeren Bereich füllen. */
            width: 1fr;
        }
    """

    def __init__(self, logic: StudiumLogic):
        super().__init__()
        self.logic = logic

    def compose(self) -> ComposeResult:
        # Durch die compose Funktion, werden die Anzeigeelemete definiert.
        self.ectsBar = ProgressBar(show_bar=True, show_percentage=False, show_eta=False, classes="w-100")
        self.dayBar = ProgressBar(show_bar=True, show_percentage=False, show_eta=False, classes="w-100")

        with Container(classes="h-auto"):
            with Horizontal(classes="single-line"):
                yield Label("ECTS 0/0".ljust(20), id="ects")
                yield self.ectsBar

            with Horizontal(classes="single-line"):
                yield Label("Tag 0/0".ljust(20), id="day")
                yield self.dayBar

    def on_mount(self):
        self.update_data()

    def update_data(self):
        total_ects = self.logic.get_total_ects()
        current_ects = self.logic.get_current_ects()
        total_days = self.logic.get_total_days()
        current_day = self.logic.get_current_day()

        # Labels befüllen. ljust(20) füllt den String auf 20 Zeichen auf, damit beide Fortschrittsbalken an der gleichen Stelle Beginnen.
        self.query_one("#ects", Label).update(f"ECTS {current_ects}/{total_ects}".ljust(20))
        self.query_one("#day", Label).update(f"Tag {current_day}/{total_days}".ljust(20))

        # Fortschrittsbalken aktualisieren
        self.ectsBar.update(progress=current_ects, total=total_ects)
        self.dayBar.update(progress=current_day, total=total_days)
