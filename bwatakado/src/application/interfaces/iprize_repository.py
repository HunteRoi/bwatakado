from abc import ABC, abstractmethod

from bwatakado.src.domain.entities.prize import Prize


class IPrizeRepository(ABC):
    """Interface that provides prize CRUD functionalities."""

    @abstractmethod
    def create_prize(self, prize: Prize) -> Prize:
        """Creates the prize."""

    @abstractmethod
    def get_prize(self, prize_id: int) -> Prize | None:
        """Gets the prize by its id."""

    @abstractmethod
    def update_prize(self, prize: Prize) -> Prize:
        """Updates the prize."""

    @abstractmethod
    def delete_prize(self, prize_id: int) -> None:
        """Deletes the prize."""
