"""Add Module screen."""

from textual.containers import Container, Vertical, Horizontal
from textual.widgets import Button, Checkbox, Input, Label, Select
from textual.validation import Integer
from src.models.modul import Modul
from src.logic import StudiumLogic
from .base import BaseScreen


class AddModulScreen(BaseScreen):
    """Screen for adding a new module."""

    def __init__(self, logic: StudiumLogic):
        super().__init__()
        self.logic = logic

    def compose(self):
        s = self.logic.get_studiengang()

        with Container(classes="content"):
            with Vertical():
                yield Label(f"Modul hinzufügen", classes="mb-1")
                yield Select(
                    ((f"Semester {semester.nummer}", semester.nummer) for semester in s.semester),
                    id="semester",
                    prompt="Semester auswählen"
                )
                yield Input(
                    placeholder="ID",
                    id="id"
                )
                yield Input(
                    placeholder="Name",
                    id="name"
                )
                yield Input(
                    placeholder="ECTS",
                    id="ects",
                    validators=[Integer()],
                    classes="mb-1"
                )
                yield Checkbox(
                    label="Angerechnet",
                    id="credited",
                    classes="mb-1",
                    compact=True
                )
                with Horizontal():
                    yield Button("Hinzufügen", id="add", variant="primary")
                    yield Button("Abbrechen", id="cancel")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "add":
            self.add_modul()
        elif event.button.id == "cancel":
            self.app.pop_screen()

    def add_modul(self) -> None:
        """Add a new module."""
        try:
            semester = self.query_one("#semester", Select).value
            id = self.query_one("#id", Input).value
            name = self.query_one("#name", Input).value
            ects = int(self.query_one("#ects", Input).value)
            credited = self.query_one("#credited", Checkbox).value

            if not all([semester, id, name, ects]):
                self.notify("Bitte füllen Sie alle Felder aus", timeout=3, severity="error")
                return

            modul = Modul(
                id=id,
                name=name,
                ects=ects,
                angerechnet=credited
            )

            self.logic.add_modul(semester, modul)
            self.notify(f"Modul '{name}' hinzugefügt", timeout=2)
            self.app.pop_screen()
        except ValueError:
            self.notify("Ungültige Eingabe", timeout=3, severity="error")
