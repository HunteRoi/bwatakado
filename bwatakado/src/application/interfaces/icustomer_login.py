from abc import ABC, abstractmethod

from bwatakado.src.domain.entities.customer import Customer


class ICustomerLogin(ABC):
    """Interface that provides customer login functionalities."""

    @abstractmethod
    def execute(self, phone_number: str) -> Customer:
        """Logs in a customer."""
