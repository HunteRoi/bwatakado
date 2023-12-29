from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from bwatakado.src.application.interfaces.icustomer_repository import (
    ICustomerRepository,
)
from bwatakado.src.domain.entities.customer import Customer
from bwatakado.src.infrastructure.models.customer_model import CustomerModel


class CustomerRepository(ICustomerRepository):
    """Customer repository implementation."""

    def __init__(self, db_path: str = "~/.bwatakado/bwatakado.sqlite") -> None:
        self.engine = create_engine(f"sqlite:///{db_path}")

    def create_customer(self, customer: Customer) -> Customer:
        with Session(self.engine) as session:
            model = CustomerModel.from_customer(customer)
            session.add(model)
            session.commit()

            return model.to_customer()
