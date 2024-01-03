from unittest import mock
from unittest.mock import MagicMock
import pytest
from bwatakado.src.application.use_cases.get_customer_tickets import (
    GetCustomerTickets,
)

from bwatakado.src.domain.entities.customer import Customer
from bwatakado.src.domain.entities.locality import Locality
from bwatakado.src.domain.entities.province import Province
from bwatakado.src.domain.entities.ticket import Ticket
from bwatakado.src.domain.exceptions.invalid_pin_code_error import InvalidPinCodeError
from bwatakado.src.domain.value_objects.address import Address


class TestGetCustomerTickets:
    """Test suite to get tickets of a customer."""

    @pytest.fixture(scope="function", autouse=True, name="customer")
    def generate_customer(self) -> Customer:
        """Generate a customer."""
        return Customer(
            firstname="firstname",
            lastname="lastname",
            email="e@e.c",
            phone_number="0000000000",
            address=Address("city", "state", "country", "0000"),
            pin_code="0000",
            locality=Locality(1, 1000, "Bruxelles", Province(1, "Bruxelles")),
        )

    @pytest.fixture(scope="function", autouse=True, name="usecase")
    @mock.patch(
        "bwatakado.src.application.interfaces.icustomer_repository",
        name="customer_repo_mock",
    )
    def generate_usecase(self, customer_repo_mock: MagicMock) -> GetCustomerTickets:
        """Generate the use case."""
        return GetCustomerTickets(customer_repo_mock)

    def test_get_tickets_returns_empty_list_when_customer_has_no_tickets(
        self, customer: Customer, usecase: GetCustomerTickets
    ) -> None:
        """Validates that getting a customer's tickets when he has none returns an empty list."""
        usecase.customer_repository.find_by_phone_number.return_value = customer

        tickets = usecase.execute(customer.phone_number, customer.pin_code)

        assert tickets == []

    def test_get_tickets_gets_customer_by_phone_number(
        self, customer: Customer, usecase: GetCustomerTickets
    ) -> None:
        """Validates that getting a customer's tickets gets the customer by phone number."""
        usecase.customer_repository.find_by_phone_number.return_value = customer

        usecase.execute(customer.phone_number, customer.pin_code)

        usecase.customer_repository.find_by_phone_number.assert_called_once_with(
            customer.phone_number
        )

    def test_get_tickets_returns_customer_tickets_when_customer_has_some(
        self, customer: Customer, usecase: GetCustomerTickets
    ):
        """Validates that getting a customer's tickets returns
        the customer's tickets when he has some."""
        ticket = Ticket(True)
        customer.add_ticket(ticket)
        usecase.customer_repository.find_by_phone_number.return_value = customer

        tickets = usecase.execute(customer.phone_number, customer.pin_code)

        assert len(tickets) == 1
        assert ticket in tickets

    def test_get_tickets_raises_invalid_pin_code_error_when_customer_pin_code_is_invalid(
        self, customer: Customer, usecase: GetCustomerTickets
    ) -> None:
        """Validates that getting a customer's tickets raises an InvalidPinCodeError
        when the customer's pin code is invalid."""
        usecase.customer_repository.find_by_phone_number.return_value = customer

        with pytest.raises(InvalidPinCodeError):
            usecase.execute(customer.phone_number, "0001")
