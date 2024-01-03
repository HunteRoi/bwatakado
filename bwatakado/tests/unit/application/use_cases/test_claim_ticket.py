from unittest import mock
from unittest.mock import MagicMock
import pytest

from bwatakado.src.application.use_cases.claim_ticket import (
    ClaimTicket,
)
from bwatakado.src.domain.entities.customer import Customer
from bwatakado.src.domain.entities.locality import Locality
from bwatakado.src.domain.entities.province import Province
from bwatakado.src.domain.entities.ticket import Ticket
from bwatakado.src.domain.exceptions.customer_not_found_error import (
    CustomerNotFoundError,
)
from bwatakado.src.domain.exceptions.ticket_already_claimed_error import (
    TicketAlreadyClaimedError,
)
from bwatakado.src.domain.exceptions.ticket_not_found_error import TicketNotFoundError
from bwatakado.src.domain.value_objects.address import Address


class TestClaimTicket:
    """Test the ClaimTicket usecase"""

    @pytest.fixture(scope="function", autouse=True, name="customer")
    def generate_customer(self) -> Customer:
        """Generate a customer object"""
        return Customer(
            firstname="firstname",
            lastname="lastname",
            email="e@e.c",
            phone_number="0000000000",
            address=Address("city", "state", "country", "0000"),
            pin_code="0000",
            locality=Locality(1, 1000, "Bruxelles", Province(1, "Bruxelles")),
        )

    @pytest.fixture(scope="function", autouse=True, name="ticket")
    def generate_ticket(self) -> Ticket:
        """Generate a ticket object"""
        return Ticket(is_winning=False)

    @pytest.fixture(scope="function", autouse=True, name="usecase")
    @mock.patch(
        "bwatakado.src.application.interfaces.iticket_repository",
        name="ticket_repo_mock",
    )
    @mock.patch(
        "bwatakado.src.application.interfaces.icustomer_repository",
        name="customer_repo_mock",
    )
    def generate_usecase(
        self, customer_repo_mock: MagicMock, ticket_repo_mock: MagicMock
    ) -> ClaimTicket:
        """Generate the usecase"""
        return ClaimTicket(customer_repo_mock, ticket_repo_mock)

    def test_claim_ticketraises_error_when_customer_does_not_exist(
        self, customer: Customer, ticket: Ticket, usecase: ClaimTicket
    ):
        """Test that the usecase raises an error when the customer does not exist"""
        usecase.customer_repository.find_by_phone_number.return_value = None

        with pytest.raises(CustomerNotFoundError):
            usecase.execute(customer.phone_number, ticket.code)

    def test_claim_ticketraises_error_when_ticket_does_not_exist(
        self, customer: Customer, ticket: Ticket, usecase: ClaimTicket
    ):
        """Test that the usecase raises an error when the ticket does not exist"""
        usecase.ticket_repository.find_by_code.return_value = None

        with pytest.raises(TicketNotFoundError):
            usecase.execute(customer.phone_number, ticket.code)

    def test_claim_ticketraises_error_when_ticket_is_already_linked(
        self, customer: Customer, ticket: Ticket, usecase: ClaimTicket
    ):
        """Test that the usecase raises an error when the ticket is already linked"""
        ticket.has_been_claimed = True
        usecase.ticket_repository.find_by_code.return_value = ticket
        usecase.customer_repository.find_by_phone_number.return_value = MagicMock(
            add_ticket=MagicMock(side_effect=TicketAlreadyClaimedError(ticket.id))
        )

        with pytest.raises(TicketAlreadyClaimedError):
            usecase.execute(customer.phone_number, ticket.code)

    def test_claim_ticketlinks_ticket_to_customer(
        self, customer: Customer, ticket: Ticket, usecase: ClaimTicket
    ):
        """Test that the usecase links the ticket to the customer"""
        previously_not_claimed = not ticket.has_been_claimed
        usecase.customer_repository.find_by_phone_number.return_value = customer
        usecase.ticket_repository.find_by_code.return_value = ticket

        usecase.execute(customer.phone_number, ticket.code)

        assert previously_not_claimed
        assert ticket.has_been_claimed
        assert ticket in customer.tickets

    def test_claim_ticketcalls_dependencies(
        self, customer: Customer, ticket: Ticket, usecase: ClaimTicket
    ):
        """Test that the usecase calls the dependencies"""
        usecase.customer_repository.find_by_phone_number.return_value = customer
        usecase.ticket_repository.find_by_code.return_value = ticket

        usecase.execute(customer.phone_number, ticket.code)

        usecase.customer_repository.find_by_phone_number.assert_called_once_with(
            customer.phone_number
        )
        usecase.ticket_repository.find_by_code.assert_called_once_with(ticket.code)
        usecase.customer_repository.update_customer.assert_called_once()
