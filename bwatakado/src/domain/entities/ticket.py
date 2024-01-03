import uuid
from datetime import datetime

from bwatakado.src.domain.exceptions.ticket_already_drawn_error import (
    TicketAlreadyDrawnError,
)


class Ticket:
    """Ticket entity which represents a single ticket in the system."""

    def __init__(
        self,
        is_winning: bool,
        ticket_id: int = None,
        code: str = None,
        created_at: datetime = None,
        is_printed: bool = False,
        has_been_claimed: bool = False,
        drawn_at: datetime = None,
    ):
        self.id = ticket_id
        self.code = code or str(uuid.uuid4())
        self.is_winning = is_winning
        self.created_at = created_at or datetime.now()
        self.is_printed = is_printed
        self.has_been_claimed = has_been_claimed
        self.drawn_at = drawn_at

    def __eq__(self, other: object) -> bool:
        """Compare two Ticket instances."""

        if not isinstance(other, Ticket):
            return False

        return self.code == other.code

    def draw(self) -> None:
        """Draw the ticket."""

        if self.drawn_at is not None:
            raise TicketAlreadyDrawnError(self.code)

        self.drawn_at = datetime.now()
