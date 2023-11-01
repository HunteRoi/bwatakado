import random

from bwatakado.src.domain.entities.ticket import Ticket
from bwatakado.src.domain.exceptions.prize_locked_error import PrizeLockedError


class Prize:
    """Prize entity which represents a prize in the system."""

    def __init__(self, name: str, description: str, prize_type: str, quantity_max: int):
        self.name = name
        self.description = description
        self.type = prize_type
        self.quantity_max = quantity_max
        self.tickets: list[Ticket] = []
        self.all_tickets_generated = False

    @property
    def tickets_nbr(self) -> int:
        """Return the number of tickets linked to this prize."""

        return len(self.tickets)

    @property
    def quantity_redeemed(self):
        """Return the number of tickets redeemed/claimed for this prize."""

        return len(
            [
                ticket
                for ticket in self.tickets
                if ticket.has_been_claimed and ticket.is_winning
            ]
        )

    def generate_tickets(self, number: int):
        """Generate tickets for this prize."""

        if self.all_tickets_generated:
            raise PrizeLockedError()

        if number <= 0:
            raise ValueError(
                "Number of tickets to generate cannot be negative.")

        winning_values = [True] * self.quantity_max + [False] * (
            number - self.quantity_max
        )

        self.tickets = [
            Ticket(winning)
            for winning in random.sample(winning_values, len(winning_values))
        ]
        self.all_tickets_generated = True
