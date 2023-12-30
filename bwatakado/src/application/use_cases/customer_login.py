from bwatakado.src.application.interfaces.icustomer_login import ICustomerLogin
from bwatakado.src.application.interfaces.icustomer_repository import ICustomerRepository
from bwatakado.src.domain.entities.customer import Customer
from bwatakado.src.domain.exceptions.customer_not_found_error import CustomerNotFoundError


class CustomerLogin(ICustomerLogin):
    """Customer login use case"""

    def __init__(self, customer_repository: ICustomerRepository):
        self.customer_repository = customer_repository

    def execute(self, phone_number: str) -> Customer:
        """Logs in to a customer account"""
        customer = self.customer_repository.find_by_phone_number(phone_number)
        if customer is None:
            raise CustomerNotFoundError(phone_number)
        return customer
