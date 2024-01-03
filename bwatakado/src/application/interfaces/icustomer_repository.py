from abc import ABC, abstractmethod

from bwatakado.src.domain.entities.customer import Customer


class ICustomerRepository(ABC):
    """Interface that provides customer CRUD functionalities."""

    @abstractmethod
    def create_customer(self, customer: Customer) -> Customer:
        """Creates the customer."""

    @abstractmethod
    def find_by_phone_number(self, phone_number: str) -> Customer | None:
        """Finds the customer by phone number."""

    @abstractmethod
    def update_customer(self, customer: Customer) -> Customer:
        """Updates the customer."""
