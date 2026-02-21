"""Base screen classes for the UI."""

from textual.screen import Screen
from textual.containers import Container, Vertical
from textual.widgets import Header, Footer, Button, Input, Label, Static


class BaseScreen(Screen):
    """Base class for all screens in the application."""

    BINDINGS = [("escape", "app.pop_screen", "Back")]

    def compose(self):
        """Compose the screen layout."""
        yield Header()
        yield Container(
            Vertical(id="content")
        )
        yield Footer()
