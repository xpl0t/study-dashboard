"""Add Semester screen."""

from textual.containers import Container, Vertical, Horizontal
from textual.widgets import Button, Input, Label, Static
from textual.validation import Integer
from src.models.semester import Semester
from src.logic import StudiumLogic
from .base import BaseScreen


class AddSemesterScreen(BaseScreen):
    """UI-Klasse zum Hinzufügen eines neuen Semesters."""

    CSS_PATH = "add_semester.tcss"

    def __init__(self, logic: StudiumLogic):
        super().__init__()
        self.logic = logic

    def compose(self):
        """Compose the screen layout."""
        with Container(classes="content"):
            with Vertical():
                yield Label("Semster hinzufügen", classes="mb-1")

                yield Input(
                    placeholder="Semester ID",
                    id="id",
                    classes="mb-1",
                    validators=[Integer()]
                )

                with Horizontal():
                    yield Button("Hinzufügen", id="add", variant="primary")
                    yield Button("Abbrechen", id="cancel")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "add":
            self.add_semester()
        elif event.button.id == "cancel":
            self.app.pop_screen()

    def add_semester(self) -> None:
        try:
            s = self.logic.get_studiengang()
            id = int(self.query_one("#id", Input).value)

            if [s.nummer for s in s.semester].count(id) > 0:
                self.notify(f"Semester '{id}' existiert bereits", timeout=3, severity="error")
                return

            semester = Semester(
                nummer=id,
                module=[]
            )

            self.logic.add_semester(semester)
            self.notify(f"Semester '{id}' hinzugefügt", timeout=2)
            self.app.pop_screen()

        except ValueError:
            self.notify("Ungültige Eingabe", timeout=3, severity="error")
