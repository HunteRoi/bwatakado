from abc import ABC, abstractmethod


class IGenerateTickets(ABC):
    """Interface that provides ticket generation functionality"""

    @abstractmethod
    def execute(self, prize_id: int, tickets_to_generate: int):
        """Generate tickets for a prize and save in database."""
