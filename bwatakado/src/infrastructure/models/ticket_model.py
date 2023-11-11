from datetime import datetime

from sqlalchemy import ForeignKey, Boolean, Integer, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from bwatakado.src.domain.entities.ticket import Ticket
from bwatakado.src.infrastructure.models.base import Base


class TicketModel(Base):
    """Ticket model."""

    __tablename__ = "ticket"

    id: Mapped[int] = mapped_column("id", Integer, primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column("code", String, nullable=False)
    is_winning: Mapped[bool] = mapped_column("is_winning", Boolean, nullable=False)
    created_at: Mapped[datetime] = mapped_column("created_at", DateTime, nullable=False)
    is_printed: Mapped[bool] = mapped_column("is_printed", Boolean, nullable=False)
    has_been_claimed: Mapped[bool] = mapped_column(
        "has_been_claimed", Boolean, nullable=False
    )
    prize_id: Mapped[int] = mapped_column(ForeignKey("prize.id"), nullable=False)
    prize: Mapped["PrizeModel"] = relationship(back_populates="tickets")

    @classmethod
    def from_ticket(cls, ticket: Ticket) -> "TicketModel":
        """Converts a ticket entity to a ticket model."""

        return cls(
            id=ticket.id,
            code=ticket.code,
            is_winning=ticket.is_winning,
            created_at=ticket.created_at,
            is_printed=ticket.is_printed,
            has_been_claimed=ticket.has_been_claimed,
        )

    def to_ticket(self) -> Ticket:
        """Converts the model to a ticket entity."""

        return Ticket(
            ticket_id=self.id,
            code=self.code,
            is_winning=self.is_winning,
            created_at=self.created_at,
            is_printed=self.is_printed,
            has_been_claimed=self.has_been_claimed,
        )
