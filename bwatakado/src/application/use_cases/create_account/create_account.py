from bwatakado.src.application.interfaces.icreate_account import ICreateAccount
from bwatakado.src.application.interfaces.icustomer_repository import ICustomerRepository
from bwatakado.src.application.use_cases.create_account.account_data import AccountData
from bwatakado.src.domain.entities.customer import Customer
from bwatakado.src.domain.value_objects.address import Address


class CreateAccount(ICreateAccount):
    """Create account use case."""

    def __init__(self, customer_repository: ICustomerRepository) -> None:
        self.customer_repository = customer_repository

    def execute(self, data: AccountData) -> Customer:
        """Create a customer account"""
        customer = Customer(
            data.firstname,
            data.lastname,
            data.phone_number,
            data.email,
            Address(
                data.address.city,
                data.address.state,
                data.address.country,
                data.address.zipcode,
                data.address.street,
                data.address.number,
                data.address.complement,
            ),
            data.pin_code,
        )
        return self.customer_repository.create_customer(customer)
