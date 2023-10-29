import uuid
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Ticket:
    """Ticket entity which represents a single ticket in the system."""

    code: str = field(default_factory=lambda: str(
        uuid.uuid4()), repr=True, init=False)
    is_winning: bool = field(repr=True, init=True)
    created_at: datetime = field(
        default_factory=datetime.now, repr=True, init=False)
    is_printed: bool = field(default=False, repr=True, init=False)
    has_been_claimed: bool = field(default=False, repr=True, init=False)
