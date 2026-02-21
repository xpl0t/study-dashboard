from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import DataTable
from src.logic import StudiumLogic
from rich.text import Text

class SemesterTable(Widget):
    """"Widget das alle Semester/Module in einer Tabelle darstellt."""

    DEFAULT_CLASSES="h-auto"

    def __init__(self, logic: StudiumLogic):
        super().__init__()
        self.logic = logic

    def compose(self) -> ComposeResult:
        # Durch die compose Funktion, werden die Anzeigeelemete definiert.
        yield DataTable()

    def on_mount(self):
        table = self.query_one(DataTable)
        # Hervorhebung von Zellen vermeiden
        table.cursor_type = "none"

        self.update_data()

    def update_data(self):
        # Datenstand in der Anzeige reflektieren

        table = self.query_one(DataTable)
        columns = self.get_columns()
        rows = self.get_rows()

        # Zunächst muss die Tabelle zurückgesetzt werden, ansonsten werden die Spalten und Zeilen angehängt.
        table.clear(columns=True)

        table.add_columns(*columns)
        for number, row in enumerate(rows, start=1):
            label = Text(str(number), style="italic")
            table.add_row(*row, label=label)

    def get_columns(self):
        sg = self.logic.get_studiengang()
        return [ f"Semester {s.nummer}" for s in sg.semester ]

    def get_rows(self):
        sg = self.logic.get_studiengang()
        rows = []

        # Maximale Modulanzahl ermitteln = Anzahl Zeilen
        maxModule = max([ len(s.module) for s in sg.semester ])

        for i in range(0, maxModule):
            # Pro Iteration wird eine Zeile der Tabelle berechnet
            row = []

            # Pro Semester wird geprüft, ob es ein Modul mit dem Index i hat.
            for s in sg.semester:
                # Wenn das Semester weniger Module als maxModule besitzt, tritt dieser Fall ein und eine leere Zeile wird eingefügt.
                if (i >= len(s.module)):
                    row.append("")
                    continue

                module = s.module[i]

                # Je nach erreichter Leistung oder Anrechnung, wird eine entsprechende Checkbox eingefügt.
                if module.angerechnet:
                    row.append(Text("☑", style="blue"))
                elif module.leistung is not None:
                    row.append(Text("☑", style="green"))
                else:
                    row.append("☐")

            rows.append(row)

        return rows
