from bwatakado.src.application.interfaces.icreate_account import ICreateAccount
from bwatakado.src.application.interfaces.icustomer_repository import (
    ICustomerRepository,
)
from bwatakado.src.application.interfaces.ilocality_repository import (
    ILocalityRepository,
)
from bwatakado.src.application.use_cases.create_account.account_data import AccountData
from bwatakado.src.domain.entities.customer import Customer
from bwatakado.src.domain.value_objects.address import Address


class CreateAccount(ICreateAccount):
    """Create account use case."""

    def __init__(
        self,
        customer_repository: ICustomerRepository,
        locality_repository: ILocalityRepository,
    ) -> None:
        self.customer_repository = customer_repository
        self.locality_repository = locality_repository

    def execute(self, data: AccountData) -> Customer:
        """Create a customer account"""

        if data.address is None or not isinstance(data.address, Address):
            raise ValueError("Invalid address")
        if (
            data.locality_id is None
            or not isinstance(data.locality_id, int)
            or data.locality_id < 1
        ):
            raise ValueError("Invalid locality id")

        locality = self.locality_repository.get_by_id(data.locality_id)
        if locality is None:
            raise ValueError("Invalid locality id")

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
            locality,
        )

        return self.customer_repository.create_or_update_customer(customer)
