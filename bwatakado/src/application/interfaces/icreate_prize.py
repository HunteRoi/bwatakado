from abc import ABC, abstractmethod

from bwatakado.src.domain.entities.prize import Prize


class ICreatePrize(ABC):
    """Interface that provides prize creation functionality."""

    @abstractmethod
    def execute(self, create_prize_dto: Prize) -> Prize:
        """Creates the prize."""
