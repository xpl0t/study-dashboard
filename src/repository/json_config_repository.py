from src.repository import ConfigRepository
import json
from pathlib import Path
from src.models import Studiengang, Modul, Prüfungsleistung, Semester


class JsonConfigRepository(ConfigRepository):
    """Implementation von ConfigRepository mit JSON basierendem Backend."""

    def __init__(self, path: str = "studium.json"):
        self.path = Path(path)

    def __load(self) -> Studiengang:
        """Studiengang aus JSON Datei laden."""

        if not self.path.exists():
            return Studiengang()

        with open(self.path, "r", encoding="utf-8") as f:
            str = f.read()
            return Studiengang.from_json(str)

    def __save(self, studiengang: Studiengang) -> None:
        """Speichern des Studiengangs in JSON Datei."""

        with open(self.path, "w", encoding="utf-8") as f:
            # Schreiben der JSON-Datei.
            # indent sorgt für eine ansprechende Formatierung der Datei, um manuelle Korrekturen zu erleichern.
            # sort_keys sortiert die JSON Eigenschaften, um ein einheitliches Format zu schaffen.
            f.write(studiengang.to_json(indent=2, sort_keys=True))

    def get_studiengang(self) -> Studiengang:
        """Gesamtes Studiengang-Object abrufen."""

        return self.__load()

    def update_studiengang(self, obj: Studiengang) -> None:
        """Eigenschaften des Studiengangs aktualisieren. Semester werden nicht aktualisiert. (lazy update)"""

        sg = self.__load()
        sg.name = obj.name
        sg.beginn = obj.beginn
        sg.zielende = obj.zielende
        sg.ects_insgesamt = obj.ects_insgesamt
        sg.zielnote = obj.zielnote
        self.__save(sg)

    def add_semester(self, obj: Semester) -> None:
        """Semester hinzufügen."""

        studiengang = self.__load()
        studiengang.semester.append(obj)
        self.__save(studiengang)

    def del_semester(self, semester: int) -> None:
        """Semester über Semesternummer löschen."""

        studiengang = self.__load()
        studiengang.semester = [s for s in studiengang.semester if s.nummer != semester]
        self.__save(studiengang)

    def add_modul(self, semester: int, obj: Modul) -> None:
        """Modul hinzufügen über Semesternummer hinzufügen."""

        studiengang = self.__load()

        # Zunächst muss das passende Semster herausgesucht werden, bevor das Modul hinzugefügt werden kann.
        for s in studiengang.semester:
            if s.nummer == semester:
                s.module.append(obj)
                break

        self.__save(studiengang)

    def del_modul(self, id: str) -> None:
        """Modul über ID löschen."""

        studiengang = self.__load()

        # Das Modul wird gelöscht, in dem die Semester itteriert werden und die Modulliste mit einer gefilterten Version überschrieben wird.
        for s in studiengang.semester:
            s.module = [m for m in s.module if m.id != id]

        self.__save(studiengang)

    def set_leistung(self, id: str, obj: Prüfungsleistung) -> None:
        """Leistung für Modul setzen."""

        studiengang = self.__load()

        # Verschachtelte Module iterieren und gegebenenfalls Aktualisierung der Leistung bei Übereinstimmung.
        for s in studiengang.semester:
            for m in s.module:
                if m.id == id:
                    m.leistung = obj
                    break

        self.__save(studiengang)

    def del_leistung(self, id: str) -> None:
        """Leistung über Modul ID löschen."""

        sg = self.__load()

        # Verschachtelte Module iterieren und gegebenenfalls Löschung der Leistung bei Übereinstimmung.
        for s in sg.semester:
            for m in s.module:
                if m.id == id:
                    m.leistung = None
                    break

        self.__save(sg)
