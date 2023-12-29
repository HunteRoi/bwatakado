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
    ):
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
            raise ValueError(
                "phone_number must be a non-empty string of 10 digits")
        self.phone_number = phone_number

        if (
            not email
            or not isinstance(email, str)
            or "@" not in email
            or "." not in email
        ):
            raise ValueError(
                "email must be a non-empty string with a valid format")
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

        self.tickets = list[Ticket]()

    def add_ticket(self, ticket: Ticket):
        """Redeems a ticket for themselves"""
        if ticket.has_been_claimed:
            raise TicketAlreadyClaimedError(ticket.id)

        self.tickets.append(ticket)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Customer):
            return False
        return (
            self.phone_number == other.phone_number
            and self.pin_code == other.pin_code
        )
