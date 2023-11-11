from typing import List

from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from bwatakado.src.domain.entities.prize import Prize
from bwatakado.src.infrastructure.models.base import Base
from bwatakado.src.infrastructure.models.ticket_model import TicketModel


class PrizeModel(Base):
    """Prize model."""

    __tablename__ = "prize"

    id: Mapped[int] = mapped_column("id", Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column("name", String, nullable=False)
    type: Mapped[str] = mapped_column("type", String, nullable=False)
    description: Mapped[str] = mapped_column("description", String, nullable=False)
    quantity_max: Mapped[int] = mapped_column("quantity_max", Integer, nullable=False)
    all_tickets_generated: Mapped[bool] = mapped_column(
        "all_tickets_generated", Boolean, nullable=False
    )
    tickets: Mapped[List["TicketModel"]] = relationship(
        back_populates="prize", cascade="all, delete-orphan", lazy="select"
    )

    @classmethod
    def from_prize(cls, prize: Prize) -> "PrizeModel":
        """Converts a Prize entity to a Prize model."""

        return cls(
            id=prize.id,
            name=prize.name,
            type=prize.type,
            description=prize.description,
            quantity_max=prize.quantity_max,
            all_tickets_generated=prize.all_tickets_generated,
            tickets=[TicketModel.from_ticket(ticket) for ticket in prize.tickets],
        )

    def to_prize(self) -> Prize:
        """Convert the model to a Prize entity."""

        return Prize(
            name=self.name,
            description=self.description,
            prize_type=self.type,
            quantity_max=self.quantity_max,
            prize_id=self.id,
            tickets=[ticket.to_ticket() for ticket in self.tickets],
            all_tickets_generated=self.all_tickets_generated,
        )
