from src.models.modul import Modul
from src.models.prüfungsleistung import Prüfungsleistung
from src.models.semester import Semester
from src.models.studiengang import Studiengang
from datetime import datetime, timezone
from src.repository import ConfigRepository


class StudiumLogic:
    """Geschäftslogik für Studienverwaltung."""

    def __init__(self, repo: ConfigRepository):
        self.repo = repo

    def get_studiengang(self) -> Studiengang:
        """Studiengang aus JSON Datei laden."""
        return self.repo.get_studiengang()

    # Semester Operationen

    def add_semester(self, obj: Semester) -> None:
        """Semester hinzufügen."""
        self.repo.add_semester(obj)

    def del_semester(self, semester: int):
        """Semester über Semesternummer löschen."""
        self.repo.del_semester(semester)

    # Modul Operationen

    def add_modul(self, semester: int, obj: Modul):
        """Modul über Semesternummer hinzufügen."""
        self.repo.add_modul(semester, obj)

    def del_modul(self, id: str):
        """Modul über ID löschen."""
        self.repo.del_modul(id)

    # Prüfungsleistung Operationen

    def set_leistung(self, id: str, obj: Prüfungsleistung):
        """Leistung über Modul ID setzen."""
        self.repo.set_leistung(id, obj)

    def del_leistung(self, id: str):
        """Leistung über Modul ID löschen."""
        self.repo.del_leistung(id)

    # Berechnungsmethoden

    def get_total_ects(self) -> int:
        """Gibt Gesamt-ECTS zurück."""
        sg = self.get_studiengang()
        return sg.ects_insgesamt

    def get_current_ects(self) -> int:
        """Berechnet die aktuell erreichten ECTS."""
        sg = self.get_studiengang()
        # Hier werden die Module über die Semester itteriert und die ECTS zusammengezählt, wenn eine Leistung vorhanden ist oder das Modul angerechnet wurde.
        return sum([ m.ects for semester in sg.semester for m in semester.module if m.leistung != None or m.angerechnet ])

    def get_total_days(self) -> int:
        """Berechnet die Anzahl an Tagen der geplanten Studienzeit."""
        sg = self.get_studiengang()
        # Zuerst wird die Zeitspanne durch Substraktion berechnet, danach wird die Zeitspanne als Tage zurückgegeben.
        return (sg.zielende.astimezone(timezone.utc) - sg.beginn.astimezone(timezone.utc)).days

    def get_current_day(self) -> int:
        """Berechnet den aktuellen Tag im Studium."""
        sg = self.get_studiengang()
        return (datetime.now(timezone.utc) - sg.beginn.astimezone(timezone.utc)).days

    def get_days_advance(self) -> int:
        """Berechnet den Vorsprung oder Verzug in Tagen."""
        total_days = self.get_total_days()
        current_day = self.get_current_day()
        current_ects = self.get_current_ects()
        total_ects = self.get_total_ects()

        # Um Division durch 0 zu vermeiden, wird dieser Fall abgefangen.
        if total_days == 0 or total_ects == 0:
            return 0

        # Um den Vorsprung/Verzug zu berechnen wird zunächst ermittelt,
        # wieviele ECTS zu diesem Zeitpunkt erreicht sein sollten.
        expected_ects = (current_day / total_days) * total_ects

        # Anschließend wird berechnet, wieviel Zeit planmäßig für ein ECTS zur Verfügung stehen.
        days_per_1_ects = total_days / total_ects

        # Nun kann der Vorsprung/Verzug, aus der ECTS-Differenz multipliziert mit der Zeit pro einem ECTS berechnet werden.
        return int((current_ects - expected_ects) * days_per_1_ects)

    def get_days_5_ects(self) -> int:
        """Berechnet die Anzahl an Tagen, die in der verbleibenden Zeit durchschnittlich für 5 ECTS zur Verfügung stehen."""

        sg = self.get_studiengang()

        # Um diese Metrik zu berechnen, wird die Anzahl der verbleibenden ECTS den verbleibenden Tagen gegenübergestellt.
        days_left = (sg.zielende.astimezone(timezone.utc) - datetime.now(timezone.utc)).days
        etcs_left = sg.ects_insgesamt - self.get_current_ects()

        # int() sorgt für eine bedingungslose Abrundung der Zahl
        return int(days_left / (etcs_left / 5))

    def get_average_grade(self) -> float:
        """Berechnet die durchschnittliche Note."""

        sg = self.get_studiengang()

        # Alle Noten in einer Liste sammeln.
        grades = [ m.leistung.note for semester in sg.semester for m in semester.module if m.leistung != None ]

        # Vermeidet Division durch 0
        if not grades:
            return 0

        # Durchschnitt berechnen
        return sum(grades) / len(grades)

    def get_max_remaining_average(self) -> float:
        """Gibt den maximalen Schnitt zurück, der mit den restlichen Modulen erreicht werden muss, um die Zielnote zu erreichen."""

        # Die Berechnung basiert auf der allgemeinen Formel zur Berechnung gewichteter Durchschnitte.
        # Wenn der aktuelle Schnitt, bei 30% Fortschritt 3.0 beträgt und die Zielnote 2.0 ist, ergibt sich folgende Gleichung:
        # 0.3 * 3.0 + 0.7 * x = 2.0
        # Dabei ist x unser gesuchter Maximalrestdurchschnitt. Durch Umformen ergibt sich folgende Formel zur Berechnung:
        # x = 2.0 - 0.3 * 3.0 / 0.7

        sg = self.get_studiengang()

        quota_done = self.get_current_ects() / sg.ects_insgesamt
        quota_remaining = 1 - quota_done
        # Falls noch keine Note vorhanden ist, wird stellvertretend mit der Zielnote gerechnet.
        # Dies verhindert Berechnungsfehler, wenn beispielsweise einige Kurse angerechnet wurden, aber keine normale Leistung eingetragen ist.
        avg_grade = self.get_average_grade() if self.get_average_grade() != 0 else sg.zielnote

        return (sg.zielnote - quota_done * avg_grade) / quota_remaining
