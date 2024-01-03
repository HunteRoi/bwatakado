from abc import ABC, abstractmethod

from bwatakado.src.domain.entities.ticket import Ticket


class IGetCustomerTickets(ABC):
    """Interface for getting tickets of a customer"""

    @abstractmethod
    def execute(
        self, customer_phone_number: str, customer_pin_code: str
    ) -> list[Ticket]:
        """Gets the tickets of a customer based on its phone number and PIN code."""
