from unittest import mock
from unittest.mock import MagicMock

import pytest

from bwatakado.src.application.use_cases.draw_tickets import DrawTickets
from bwatakado.src.domain.entities.customer import Customer
from bwatakado.src.domain.entities.locality import Locality
from bwatakado.src.domain.entities.province import Province
from bwatakado.src.domain.entities.ticket import Ticket
from bwatakado.src.domain.exceptions.customer_not_found_error import (
    CustomerNotFoundError,
)
from bwatakado.src.domain.exceptions.invalid_pin_code_error import InvalidPinCodeError
from bwatakado.src.domain.exceptions.tickets_not_found_error import TicketsNotFoundError
from bwatakado.src.domain.value_objects.address import Address


class TestDrawTickets:
    """Test class for DrawTickets use case."""

    @pytest.fixture(scope="function", autouse=True, name="customer")
    def generate_customer(self):
        """Generate a customer."""

        return Customer(
            "firstname",
            "lastname",
            "0000000000",
            "e@e.c",
            Address("city", "state", "country", "0000"),
            "0000",
            Locality(1, 1000, "Bruxelles", Province(1, "Bruxelles")),
        )

    @pytest.fixture(autouse=True, name="usecase", scope="function")
    @mock.patch(
        "bwatakado.src.application.interfaces.icustomer_repository",
        name="mock_customer_repository",
    )
    @mock.patch(
        "bwatakado.src.application.interfaces.iticket_repository",
        name="mock_ticket_repository",
    )
    def generate_usecase(
        self, mock_customer_repository: MagicMock, mock_ticket_repository: MagicMock
    ) -> DrawTickets:
        """Generate the use case with mocked repositories."""

        return DrawTickets(
            mock_customer_repository,
            mock_ticket_repository,
        )

    @pytest.mark.parametrize(
        "phone_number",
        [
            None,
            "",
            "1234567890",
            "0987654321",
        ],
    )
    def test_draw_tickets_on_unknown_customer(
        self, usecase: DrawTickets, phone_number: str
    ):
        """Test that drawing tickets on an unknown customer raises an exception."""

        usecase.customer_repository.find_by_phone_number.return_value = None
        tickets_codes = set()

        with pytest.raises(CustomerNotFoundError):
            usecase.execute(phone_number, "0000", tickets_codes)

    def test_draw_tickets_gets_known_customer(
        self, usecase: DrawTickets, customer: Customer
    ):
        """Test that drawing tickets on a known customer gets the customer."""

        usecase.customer_repository.find_by_phone_number.return_value = customer
        tickets_codes = set()

        usecase.execute(customer.phone_number, customer.pin_code, tickets_codes)

        usecase.customer_repository.find_by_phone_number.assert_called_once_with(
            customer.phone_number
        )

    def test_draw_tickets_on_known_customer_with_wrong_pin_code(
        self, usecase: DrawTickets, customer: Customer
    ):
        """Test that drawing tickets on a known customer with a wrong pin code raises an error."""

        usecase.customer_repository.find_by_phone_number.return_value = customer
        tickets_codes = set()

        with pytest.raises(InvalidPinCodeError):
            usecase.execute(customer.phone_number, "0001", tickets_codes)

    def test_draw_tickets_raises_exception_when_given_tickets_are_not_claimed_by_customer(
        self, usecase: DrawTickets, customer: Customer
    ):
        """Test that drawing wrong tickets on a customer raises an exception."""

        usecase.customer_repository.find_by_phone_number.return_value = customer
        tickets_codes = {"1"}

        with pytest.raises(TicketsNotFoundError):
            usecase.execute(customer.phone_number, customer.pin_code, tickets_codes)

    def test_draw_tickets_updates_customer_tickets(
        self, usecase: DrawTickets, customer: Customer
    ):
        """Test that drawing tickets updates the customer tickets."""

        ticket = Ticket(True, code="1")
        customer.add_ticket(ticket)
        usecase.customer_repository.find_by_phone_number.return_value = customer
        tickets_codes = set(ticket.code)

        usecase.execute(customer.phone_number, customer.pin_code, tickets_codes)

        usecase.ticket_repository.update_tickets.assert_called_once()
