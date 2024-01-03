import pytest

from bwatakado.src.application.interfaces.icustomer_repository import (
    ICustomerRepository,
)
from bwatakado.src.application.interfaces.iprize_repository import IPrizeRepository
from bwatakado.src.domain.entities.customer import Customer
from bwatakado.src.domain.entities.locality import Locality
from bwatakado.src.domain.entities.prize import Prize
from bwatakado.src.domain.entities.province import Province
from bwatakado.src.domain.value_objects.address import Address
from bwatakado.src.infrastructure.models.base import Base
from bwatakado.src.infrastructure.repositories.customer_repository import (
    CustomerRepository,
)
from bwatakado.src.infrastructure.repositories.prize_repository import PrizeRepository


class TestPrizeRepository:
    """PrizeRepository test cases."""

    @pytest.fixture(scope="function", autouse=True, name="customer")
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

    @pytest.fixture(scope="function", autouse=True, name="repositories")
    def generate_repositories(self) -> tuple[ICustomerRepository, IPrizeRepository]:
        """Initialize the repository."""

        customer_repository: ICustomerRepository = CustomerRepository(":memory:")
        prize_repository: IPrizeRepository = PrizeRepository(":memory:")

        prize_repository.engine = customer_repository.engine
        Base().metadata.create_all(customer_repository.engine)

        return customer_repository, prize_repository

    def test_create_customer(
        self,
        repositories: tuple[ICustomerRepository, IPrizeRepository],
        customer: Customer,
    ):
        """Validates that a customer can be added to the repository"""
        customer_repository, _ = repositories
        received_customer = customer_repository.create_or_update_customer(customer)

        assert received_customer == customer

    def test_get_customer_by_phone(
        self,
        repositories: tuple[ICustomerRepository, IPrizeRepository],
        customer: Customer,
    ):
        """Test that a customer is returned when there's a match on the phone number."""
        customer_repository, _ = repositories
        customer_repository.create_or_update_customer(customer)

        received_customer = customer_repository.find_by_phone_number(
            customer.phone_number
        )

        assert customer == received_customer

    def test_get_customer_by_phone_returns_none_when_not_existing(
        self,
        repositories: tuple[ICustomerRepository, IPrizeRepository],
        customer: Customer,
    ):
        """Test that a customer is not returned when the phone number does not match."""
        customer_repository, _ = repositories

        received_customer = customer_repository.find_by_phone_number(
            customer.phone_number
        )

        assert received_customer is None

    def test_get_customer_with_tickets(
        self,
        repositories: tuple[ICustomerRepository, IPrizeRepository],
        customer: Customer,
    ):
        """Test that a customer is returned with his tickets."""
        customer_repository, prize_repository = repositories
        prize = Prize("test_name", "test_type", "test_description", 1)
        prize.generate_tickets(1)
        prize = prize_repository.create_prize(prize)
        ticket = prize.tickets[prize.tickets_nbr - 1]
        customer.add_ticket(ticket)
        customer_repository.create_or_update_customer(customer)

        received_customer = customer_repository.find_by_phone_number(
            customer.phone_number
        )

        assert customer.email == received_customer.email
        assert ticket in received_customer.tickets
