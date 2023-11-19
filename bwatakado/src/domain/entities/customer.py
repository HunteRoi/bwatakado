from bwatakado.src.domain.entities.ticket import Ticket
from bwatakado.src.domain.exceptions.ticket_already_claimed_error import (
    TicketAlreadyClaimedError,
)


class Customer:
    """The entity representing a customer"""

    def __init__(
        self,
        firstname: str,
        lastname: str,
        phone_number: str,
        email: str,
        address: str,
        pin_code: str,
    ):
        self.firstname = firstname
        self.lastname = lastname
        self.phone_number = phone_number
        self.email = email
        self.address = address
        self.pin_code = pin_code
        self.tickets = list[Ticket]()

    def add_ticket(self, ticket: Ticket):
        """Redeems a ticket for themselves"""
        if ticket.has_been_claimed:
            raise TicketAlreadyClaimedError(ticket.id)

        self.tickets.append(ticket)
