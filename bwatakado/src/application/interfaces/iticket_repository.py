from abc import ABC, abstractmethod

from bwatakado.src.domain.entities.ticket import Ticket


class ITicketRepository(ABC):
    """Interface to manage tickets"""

    @abstractmethod
    def find_by_code(self, code: str) -> Ticket | None:
        """Get a ticket by its code"""
