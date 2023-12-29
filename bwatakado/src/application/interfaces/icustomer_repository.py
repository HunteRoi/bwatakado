from abc import ABC, abstractmethod

from bwatakado.src.domain.entities.customer import Customer


class ICustomerRepository(ABC):
    """Interface that provides customer CRUD functionalities."""

    @abstractmethod
    def create_customer(self, customer: Customer) -> Customer:
        """Creates the customer."""
