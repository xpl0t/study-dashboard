"""Set Exam Performance screen."""

from datetime import datetime
from textual.containers import Container, Horizontal
from textual.widgets import Button, Input, Label, Select
from textual.validation import Number
from src.models.prüfungsleistung import Prüfungsleistung
from src.logic import StudiumLogic
from .base import BaseScreen


class SetLeistungScreen(BaseScreen):
    """Screen for setting exam performance for a module."""

    def __init__(self, logic: StudiumLogic):
        """Initialize the screen.

        Args:
            logic: The StudiumLogic instance
            modul_id: The module ID to set performance for
        """
        super().__init__()
        self.logic = logic

    def _get_plausible_grades(self):
        # Folgenden Code hab ich von Ihnen aus dem Course Feed geklaut ;)
        return [f"{x:.1f}" for x in (
            [i + j for i in range(1, 4) for j in (0.0, 0.3, 0.7)]
            + [4.0, 5.0]
        )]

    def compose(self):
        """Compose the screen layout."""

        with Container(classes="content"):
            yield Label(f"Leistung setzen", classes="mb-1")
            yield Select(
                [],
                id="module",
                prompt="Modul auswählen"
            )
            yield Input(
                placeholder="Note",
                id="grade",
                validators=[Number()]
            )
            yield Input(
                placeholder="Datum (DD.MM.YYYY)",
                id="date",
                classes="mb-1"
            )
            with Horizontal():
                yield Button("Speichern", id="save", variant="primary")
                yield Button("Abbrechen", id="cancel")

    def on_mount(self):
        s = self.logic.get_studiengang()

        # Module aus Semestern extrahieren (flat map)
        modules = [m for se in s.semester for m in se.module if not m.angerechnet]

        module_select = self.query_one("#module", Select)
        module_select.set_options((f"{m.id} - {m.name}", m.id) for m in modules)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "save":
            self.add_leistung()
        elif event.button.id == "cancel":
            self.app.pop_screen()

    def add_leistung(self) -> None:
        """Set the exam performance."""
        try:
            module = self.query_one("#module", Select).value
            grade = float(self.query_one("#grade", Input).value)
            date = self.query_one("#date", Input).value

            if not all([module, date]):
                self.notify("Bitte füllen Sie alle Felder aus", timeout=3, severity="error")
                return

            grades = self._get_plausible_grades()
            if not f"{grade:.1f}" in grades:
                self.notify(f"Professor sagt nein! Note ungülitg. Plausible Werte: {" ".join(grades)}", timeout=10, severity="error")
                return

            leistung = Prüfungsleistung(
                note=grade,
                datum=datetime.strptime(date, "%d.%m.%Y")
            )

            self.logic.set_leistung(module, leistung)

            self.notify(f"Leistung für Modul '{module}' gespeichert", timeout=2)
            self.app.pop_screen()
        except ValueError:
            self.notify("Ungültige Eingabe", timeout=3, severity="error")
