from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from bwatakado.src.application.interfaces.iticket_repository import ITicketRepository
from bwatakado.src.domain.entities.ticket import Ticket
from bwatakado.src.infrastructure.models.ticket_model import TicketModel


class TicketRepository(ITicketRepository):
    """Ticket repository implementation."""

    def __init__(
        self, db_path: str = f"{Path.home()}/.bwatakado/bwatakado.sqlite"
    ) -> None:
        self.engine = create_engine(f"sqlite:///{db_path}")

    def find_by_code(self, code: str) -> Ticket | None:
        with Session(self.engine) as session:
            ticket: TicketModel | None = (
                session.query(TicketModel)
                .filter(TicketModel.code == code)
                .one_or_none()
            )

            if ticket is None:
                return None

            return ticket.to_ticket()
