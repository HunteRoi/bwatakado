from abc import ABC, abstractmethod

from bwatakado.src.domain.entities.prize import Prize


class IDuplicatePrize(ABC):
    """Interface that provides the feature to duplicate an existing prize."""

    @abstractmethod
    def execute(self, prize_id: int) -> Prize:
        """Duplicates the given prize"""
