from abc import ABC, abstractmethod


class IClaimTicket(ABC):
    """Interface to claim a ticket for a customer"""

    @abstractmethod
    def execute(self, customer_phone_number: str, ticket_code: str) -> None:
        """Link a ticket to a customer"""
