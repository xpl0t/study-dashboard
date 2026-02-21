from src.models.studiengang import Studiengang
from abc import ABC, abstractmethod
from src.models.modul import Modul
from src.models.prüfungsleistung import Prüfungsleistung
from src.models.semester import Semester


class ConfigRepository(ABC):
    """Abstrakte Basisklasse für Repository."""

    @abstractmethod
    def get_studiengang(self) -> Studiengang:
        """Studiengang aus JSON Datei laden."""
        pass

    @abstractmethod
    def update_studiengang(self, obj: Studiengang) -> None:
        """Eigenschaften des Studiengangs aktualisieren. Semester werden nicht aktualisiert. (lazy update)"""
        pass

    @abstractmethod
    def add_semester(self, obj: Semester) -> None:
        """Semester über Semesternummer hinzufügen."""
        pass

    @abstractmethod
    def del_semester(self, semester: int) -> None:
        """Semester über Semesternummer löschen."""
        pass

    @abstractmethod
    def add_modul(self, semester: int, obj: Modul) -> None:
        """Modul über Semesternummer hinzufügen."""
        pass

    @abstractmethod
    def del_modul(self, id: str) -> None:
        """Modul über ID löschen."""
        pass

    @abstractmethod
    def set_leistung(self, id: str, obj: Prüfungsleistung) -> None:
        """Leistung über Modul ID setzen."""
        pass

    @abstractmethod
    def del_leistung(self, id: str) -> None:
        """Leistung über Modul ID löschen."""
        pass
