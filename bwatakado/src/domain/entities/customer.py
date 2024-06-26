from bwatakado.src.domain.entities.locality import Locality
from bwatakado.src.domain.entities.ticket import Ticket
from bwatakado.src.domain.exceptions.ticket_already_claimed_error import (
    TicketAlreadyClaimedError,
)
from bwatakado.src.domain.value_objects.address import Address


class Customer:
    """The entity representing a customer"""

    def __init__(
        self,
        firstname: str,
        lastname: str,
        phone_number: str,
        email: str,
        address: Address,
        pin_code: str,
        locality: Locality,
        tickets: list[Ticket] = None,
        customer_id: int = None,
    ):
        if customer_id is not None and (
            not isinstance(customer_id, int) or customer_id < 0
        ):
            raise ValueError("customer_id must be an integer greater than 0")
        self.id = customer_id

        if not firstname or not isinstance(firstname, str) or not firstname.isalpha():
            raise ValueError(
                "firstname must be a non-empty string of alphabetic characters"
            )
        self.firstname = firstname

        if not lastname or not isinstance(lastname, str) or not lastname.isalpha():
            raise ValueError(
                "lastname must be a non-empty string of alphabetic characters"
            )
        self.lastname = lastname

        if (
            not phone_number
            or not isinstance(phone_number, str)
            or len(phone_number) != 10
            or not phone_number.isnumeric()
        ):
            raise ValueError("phone_number must be a non-empty string of 10 digits")
        self.phone_number = phone_number

        if (
            not email
            or not isinstance(email, str)
            or "@" not in email
            or "." not in email
        ):
            raise ValueError("email must be a non-empty string with a valid format")
        self.email = email

        if not address or not isinstance(address, Address):
            raise ValueError("address must be a valid address object")
        self.address = address

        if (
            not pin_code
            or not isinstance(pin_code, str)
            or len(pin_code) != 4
            or not pin_code.isnumeric()
        ):
            raise ValueError("pin_code must be a non-empty string of 4 digits")
        self.pin_code = pin_code

        if not locality or not isinstance(locality, Locality):
            raise ValueError("locality must be a valid locality object")
        self.locality = locality

        self.tickets = [] if tickets is None else tickets

    def add_ticket(self, ticket: Ticket):
        """Redeems a ticket for themselves"""
        if ticket.has_been_claimed:
            raise TicketAlreadyClaimedError(ticket.id)

        self.tickets.append(ticket)
        ticket.has_been_claimed = True

    def claim_tickets(self, tickets_codes: list[str]):
        """Redeems a list of tickets for themselves"""
        _ = [ticket.draw() for ticket in self.tickets if ticket.code in tickets_codes]

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Customer):
            return False
        return (
            self.phone_number == other.phone_number and self.pin_code == other.pin_code
        )
