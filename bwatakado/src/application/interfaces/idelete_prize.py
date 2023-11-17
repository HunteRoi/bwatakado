from abc import ABC, abstractmethod


class IDeletePrize(ABC):
    """Interface that provides prize deletion functionality."""

    @abstractmethod
    def execute(self, prize_id: int) -> None:
        """Deletes the prize."""
