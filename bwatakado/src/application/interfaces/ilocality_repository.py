from abc import ABC, abstractmethod

from bwatakado.src.domain.entities.locality import Locality


class ILocalityRepository(ABC):
    """Interface that provides locality read functionalities."""

    @abstractmethod
    def get_by_id(self, identifier: int) -> Locality | None:
        """Gets the locality by identifier."""
