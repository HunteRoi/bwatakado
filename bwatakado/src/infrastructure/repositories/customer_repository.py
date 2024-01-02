from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from bwatakado.src.application.interfaces.icustomer_repository import (
    ICustomerRepository,
)
from bwatakado.src.domain.entities.customer import Customer
from bwatakado.src.infrastructure.models.customer_model import CustomerModel


class CustomerRepository(ICustomerRepository):
    """Customer repository implementation."""

    def __init__(
        self, db_path: str = f"{Path.home()}/.bwatakado/bwatakado.sqlite"
    ) -> None:
        self.engine = create_engine(f"sqlite:///{db_path}")

    def create_customer(self, customer: Customer) -> Customer:
        with Session(self.engine) as session:
            model = CustomerModel.from_customer(customer)
            session.add(model)
            session.commit()

            return model.to_customer()

    def find_by_phone_number(self, phone_number: str) -> Customer | None:
        with Session(self.engine) as session:
            model = (
                session.query(CustomerModel)
                .filter(CustomerModel.phone_number == phone_number)
                .first()
            )

            if model is None:
                return None

            return model.to_customer()
