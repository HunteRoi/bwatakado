from bwatakado.src.application.interfaces.icustomer_repository import (
    ICustomerRepository,
)
from bwatakado.src.application.interfaces.iget_customer_tickets import (
    IGetCustomerTickets,
)
from bwatakado.src.domain.entities.ticket import Ticket
from bwatakado.src.domain.exceptions.invalid_pin_code_error import InvalidPinCodeError


class GetCustomerTickets(IGetCustomerTickets):
    """Use case to get tickets from a customer."""

    def __init__(self, customer_repository: ICustomerRepository):
        self.customer_repository = customer_repository

    def execute(
        self, customer_phone_number: str, customer_pin_code: str
    ) -> list[Ticket]:
        customer = self.customer_repository.find_by_phone_number(customer_phone_number)

        if customer.pin_code != customer_pin_code:
            raise InvalidPinCodeError(customer_pin_code)

        return customer.tickets
