import pytest

from bwatakado.src.domain.entities.customer import Customer
from bwatakado.src.domain.entities.ticket import Ticket
from bwatakado.src.domain.exceptions.ticket_already_claimed_error import (
    TicketAlreadyClaimedError,
)


class TestCustomer:
    """Test suite on a customer entity"""

    @pytest.mark.parametrize(
        "firstname, lastname, phone_number, email, address, pin_code",
        [
            ("firstname", "lastname", "0000000000", "email", "address", "0000"),
            ("f", "l", "0", "e", "a", "1234"),
        ],
    )
    def test_initialize_customer(
        self,
        firstname: str,
        lastname: str,
        phone_number: str,
        email: str,
        address: str,
        pin_code: str,
    ):
        """Validates that initializing a customer with the provided values does so properly."""
        customer = Customer(firstname, lastname, phone_number, email, address, pin_code)

        assert customer is not None
        assert customer.firstname == firstname
        assert customer.lastname == lastname
        assert customer.phone_number == phone_number
        assert customer.email == email
        assert customer.address == address
        assert customer.pin_code == pin_code

    @pytest.mark.parametrize("is_winning_ticket", [True, False])
    def test_add_ticket(self, is_winning_ticket: bool):
        """Validates that a ticket can be added to a customer's list of tickets"""
        customer = Customer(
            "firstname", "lastname", "0000000000", "email", "address", "0000"
        )
        ticket = Ticket(is_winning_ticket)

        customer.add_ticket(ticket)

        assert ticket in customer.tickets

    @pytest.mark.parametrize("is_winning_ticket", [True, False])
    def test_add_ticket_fails_if_ticket_is_already_claimed(
        self, is_winning_ticket: bool
    ):
        """Validates that adding an already claimed ticket to a customer's list
        of tickets is not possible"""
        customer = Customer(
            "firstname", "lastname", "0000000000", "email", "address", "0000"
        )
        ticket = Ticket(is_winning_ticket, has_been_claimed=True)

        with pytest.raises(TicketAlreadyClaimedError):
            customer.add_ticket(ticket)
