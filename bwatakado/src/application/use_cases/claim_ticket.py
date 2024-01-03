from bwatakado.src.application.interfaces.icustomer_repository import (
    ICustomerRepository,
)
from bwatakado.src.application.interfaces.iclaim_ticket import (
    IClaimTicket,
)
from bwatakado.src.application.interfaces.iticket_repository import ITicketRepository
from bwatakado.src.domain.exceptions.customer_not_found_error import (
    CustomerNotFoundError,
)
from bwatakado.src.domain.exceptions.ticket_not_found_error import TicketNotFoundError


class ClaimTicket(IClaimTicket):
    """Usecase to claim a ticket for a customer"""

    def __init__(
        self,
        customer_repository: ICustomerRepository,
        ticket_repository: ITicketRepository,
    ):
        self.customer_repository = customer_repository
        self.ticket_repository = ticket_repository

    def execute(self, customer_phone_number: str, ticket_code: str) -> None:
        customer = self.customer_repository.find_by_phone_number(customer_phone_number)
        if not customer:
            raise CustomerNotFoundError(customer_phone_number)

        ticket = self.ticket_repository.find_by_code(ticket_code)
        if not ticket:
            raise TicketNotFoundError(ticket_code)

        customer.add_ticket(ticket)

        self.customer_repository.update_customer(customer)
