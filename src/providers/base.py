from abc import ABC, abstractmethod

class VideoProvider(ABC):
    @abstractmethod
    def can_handle(self, url: str) -> bool:
        """Vérifie si l'URL appartient à cette plateforme."""
        pass

    @abstractmethod
    def fetch_metadata(self, url: str) -> dict:
        """Récupère titre, durée, et thumbnail."""
        pass
