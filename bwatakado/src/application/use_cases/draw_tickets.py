from bwatakado.src.application.interfaces.icustomer_repository import (
    ICustomerRepository,
)
from bwatakado.src.application.interfaces.idraw_tickets import IDrawTickets
from bwatakado.src.application.interfaces.iticket_repository import ITicketRepository
from bwatakado.src.domain.exceptions.customer_not_found_error import (
    CustomerNotFoundError,
)
from bwatakado.src.domain.exceptions.invalid_pin_code_error import InvalidPinCodeError
from bwatakado.src.domain.exceptions.tickets_not_found_error import TicketsNotFoundError


class DrawTickets(IDrawTickets):
    """Tickets drawing use case."""

    def __init__(
        self,
        customer_repository: ICustomerRepository,
        ticket_repository: ITicketRepository,
    ) -> None:
        self.customer_repository = customer_repository
        self.ticket_repository = ticket_repository

    def execute(
        self,
        customer_phone_number: str,
        customer_pin_code: str,
        customer_tickets_codes: set[str],
    ) -> None:
        customer = self.customer_repository.find_by_phone_number(customer_phone_number)

        if customer is None:
            raise CustomerNotFoundError(customer_phone_number)

        if customer.pin_code != customer_pin_code:
            raise InvalidPinCodeError(customer_pin_code)

        tickets_codes_diff = customer_tickets_codes.difference(
            map(lambda ticket: ticket.code, customer.tickets)
        )
        if len(tickets_codes_diff) > 0:
            raise TicketsNotFoundError(list(tickets_codes_diff))

        customer.claim_tickets(list(customer_tickets_codes))

        self.ticket_repository.update_tickets(customer.tickets)
