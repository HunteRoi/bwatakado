import pytest

from bwatakado.src.domain.entities.customer import Customer
from bwatakado.src.infrastructure.models.base import Base
from bwatakado.src.application.interfaces.icustomer_repository import ICustomerRepository
from bwatakado.src.infrastructure.repositories.customer_repository import CustomerRepository
from bwatakado.src.domain.value_objects.address import Address


class TestPrizeRepository:
    """PrizeRepository test cases."""

    @pytest.fixture(autouse=True, name="customer")
    def generate_customer(self):
        """Initialize a customer."""
        return Customer(
            "firstname",
            "lastname",
            "0000000000",
            "email@example.com",
            Address("city", "state", "country", "0000"),
            "0000"
        )

    @pytest.fixture(autouse=True, name="repository")
    def generate_repository(self) -> ICustomerRepository:
        """Initialize the repository."""

        repository: ICustomerRepository = CustomerRepository(":memory:")
        Base().metadata.create_all(repository.engine)

        return repository

    def test_create_customer(self, repository: ICustomerRepository, customer: Customer):
        """Validates that a customer can be added to the repository"""
        received_customer = repository.create_customer(customer)

        assert received_customer == customer
