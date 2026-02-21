from textual.app import ComposeResult, App
from textual.binding import Binding
from textual.containers import Container
from textual.widgets import Header, Footer, Button, Label
from src.logic import StudiumLogic
from src.ui.screens import (
    AddSemesterScreen,
    AddModulScreen,
    SetLeistungScreen,
)
from src.ui.semester_table import SemesterTable
from src.ui.study_bars import StudyBars
from src.ui.study_stats import StudyStats


class DashboardApp(App):
    """Hauptanzeigeklasse. Definiert den Header, Footer und den Inhaltsbereich der Anwendung."""

    CSS_PATH = "dashboard.tcss"

    # Tastaturaktionen definieren
    BINDINGS = [
        Binding("q", "quit", "Beenden"),
        Binding("s", "add_semester", "Semester hinzufügen"),
        Binding("m", "add_modul", "Modul hinzufügen"),
        Binding("l", "set_leistung", "Leistung setzen"),
    ]

    def __init__(self, logic: StudiumLogic):
        super().__init__()
        self.logic = logic

    def compose(self) -> ComposeResult:
        # Durch die compose Funktion, werden die Anzeigeelemete definiert.

        self.study_bars = StudyBars(self.logic)
        self.semester_table = SemesterTable(self.logic)
        self.stats = StudyStats(self.logic)

        yield Header()

        with Container(classes="content"):
            yield self.study_bars
            yield Label("") # TODO: Improve spacer. Maybe with margin?
            yield Label("")
            yield self.semester_table
            yield Label("")
            yield Label("")
            yield self.stats

        yield Footer()

    def on_mount(self) -> None:
        # Datenstand in der Anzeige reflektieren
        studiengang = self.logic.get_studiengang()

        self.title = f"📚 Dashboard: {studiengang.name}"

    def action_add_semester(self) -> None:
        """Screen starten, um ein neues Modul hinzuzufügen."""
        self.push_screen(AddSemesterScreen(self.logic))

    def action_add_modul(self) -> None:
        """Screen starten, um ein neues Modul hinzuzufügen."""
        self.push_screen(AddModulScreen(self.logic))

    def action_set_leistung(self) -> None:
        """Screen starten, um eine Leistung zu setzen."""
        self.push_screen(SetLeistungScreen(self.logic))

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-semester":
            self.action_add_semester()
        elif event.button.id == "btn-modul":
            self.action_add_modul()
        elif event.button.id == "btn-leistung":
            self.action_set_leistung()

    def pop_screen(self):
        # Überschreibt die pop_screen Methode, welche von den Screens aufgerufen wird, wenn sie beendet werden.

        # Die Beendigung eines Screens bedeutet unter Umständen, dass sich Daten geändert haben.
        # Daher werden sicherheitshalber alle Widgets aktualisiert.

        self.study_bars.update_data()
        self.semester_table.update_data()
        self.stats.update_data()

        return super().pop_screen()
