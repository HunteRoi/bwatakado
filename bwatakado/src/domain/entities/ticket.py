import uuid

from datetime import datetime
from dataclasses import dataclass, field


@dataclass
class Ticket:
    code: str = field(default_factory=lambda: str(uuid.uuid4()), repr=True, init=False)
    is_winning: bool = field(repr=True, init=True)
    created_at: datetime = field(default_factory=datetime.now, repr=True)
    is_printed: bool = field(default=False, repr=True, init=False)
    has_been_claimed: bool = field(default=False, repr=True, init=False)
