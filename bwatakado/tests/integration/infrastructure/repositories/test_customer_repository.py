import pytest

from bwatakado.src.application.interfaces.icustomer_repository import (
    ICustomerRepository,
)
from bwatakado.src.domain.entities.customer import Customer
from bwatakado.src.domain.entities.locality import Locality
from bwatakado.src.domain.entities.province import Province
from bwatakado.src.domain.value_objects.address import Address
from bwatakado.src.infrastructure.models.base import Base
from bwatakado.src.infrastructure.repositories.customer_repository import (
    CustomerRepository,
)


class TestPrizeRepository:
    """PrizeRepository test cases."""

    @pytest.fixture(autouse=True, name="customer")
    def generate_customer(self):
        """Initialize a customer."""
        return Customer(
            firstname="firstname",
            lastname="lastname",
            phone_number="0000000000",
            email="email@example.com",
            address=Address("city", "state", "country", "0000"),
            pin_code="0000",
            locality=Locality(1, 1000, "Bruxelles", Province(1, "Bruxelles")),
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

    def test_get_customer_by_phone(
        self, repository: ICustomerRepository, customer: Customer
    ):
        """Test that a customer is returned when there's a match on the phone number."""
        repository.create_customer(customer)

        received_customer = repository.find_by_phone_number(customer.phone_number)

        assert customer == received_customer

    def test_get_customer_by_phone_returns_none_when_not_existing(
        self, repository: ICustomerRepository, customer: Customer
    ):
        """Test that a customer is not returned when the phone number does not match."""

        received_customer = repository.find_by_phone_number(customer.phone_number)

        assert received_customer is None
