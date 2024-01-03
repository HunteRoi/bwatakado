from abc import ABC, abstractmethod


class IDrawTickets(ABC):
    """Interface that provides tickets drawing functionality."""

    @abstractmethod
    def execute(
        self,
        customer_phone_number: str,
        customer_pin_code: str,
        customer_tickets_codes: set[str],
    ) -> None:
        """Draw tickets for a given customer."""
