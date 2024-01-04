from typing import List

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from bwatakado.src.domain.entities.customer import Customer
from bwatakado.src.domain.value_objects.address import Address
from bwatakado.src.infrastructure.models.base import Base
from bwatakado.src.infrastructure.models.locality_model import LocalityModel
from bwatakado.src.infrastructure.models.ticket_model import TicketModel


class CustomerModel(Base):
    """Customer model."""

    __tablename__ = "customer"

    id: Mapped[int] = mapped_column("id", Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column("email", String, nullable=False)
    firstname: Mapped[str] = mapped_column("firstname", String, nullable=False)
    lastname: Mapped[str] = mapped_column("lastname", String, nullable=False)
    phone_number: Mapped[str] = mapped_column("phone_number", String, nullable=False)
    address: Mapped[str] = mapped_column("address", String, nullable=False)
    pin_code: Mapped[str] = mapped_column("pin_code", String, nullable=False)
    locality_id: Mapped[int] = mapped_column(ForeignKey("locality.id"), nullable=False)
    locality: Mapped[LocalityModel] = relationship(back_populates="customers")
    tickets: Mapped[List[TicketModel]] = relationship(
        back_populates="customer", lazy="select"
    )

    @classmethod
    def from_customer(cls, customer: Customer) -> "CustomerModel":
        """Converts a Customer entity to a Customer model."""

        return cls(
            firstname=customer.firstname,
            lastname=customer.lastname,
            phone_number=customer.phone_number,
            email=customer.email,
            address=customer.address.to_str(),
            pin_code=customer.pin_code,
            locality_id=customer.locality.identifier,
            locality=LocalityModel.from_locality(customer.locality),
            tickets=[TicketModel.from_ticket(ticket) for ticket in customer.tickets],
            id=customer.id,
        )

    def to_customer(self) -> Customer:
        """Convert the model to a Customer entity."""

        return Customer(
            firstname=self.firstname,
            lastname=self.lastname,
            phone_number=self.phone_number,
            email=self.email,
            address=Address.from_str(self.address),
            pin_code=self.pin_code,
            locality=self.locality.to_locality(),
            tickets=[ticket.to_ticket() for ticket in self.tickets],
            customer_id=self.id,
        )
