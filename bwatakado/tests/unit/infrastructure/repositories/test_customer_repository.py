from unittest import mock
from unittest.mock import MagicMock

from bwatakado.src.domain.entities.customer import Customer
from bwatakado.src.domain.value_objects.address import Address
from bwatakado.src.infrastructure.repositories.customer_repository import (
    CustomerRepository,
)


class TestCustomerRepository:
    """Test suite for the customer repository."""

    @mock.patch(
        "bwatakado.src.infrastructure.repositories.customer_repository.Session",
        name="session_mock"
    )
    @mock.patch(
        "bwatakado.src.infrastructure.repositories.customer_repository.create_engine",
        name="create_engine_mock"
    )
    def test_create_customer(
        self,
        create_engine_mock: MagicMock,
        session_mock: MagicMock,
    ):
        """Test that a customer is created."""
        session_mock.return_value = session_mock
        session_mock.__enter__.return_value = session_mock
        customer = Customer(
            "firstname",
            "lastname",
            "0000000000",
            "email@example.com",
            Address("city", "state", "country", "0000"),
            "0000",
        )
        repository = CustomerRepository()

        repository.create_customer(customer)

        session_mock.add.assert_called_once()
        session_mock.commit.assert_called()
