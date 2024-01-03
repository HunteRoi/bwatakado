from typing import Tuple

import pytest

from bwatakado.src.domain.entities.prize import Prize
from bwatakado.src.infrastructure.models.base import Base
from bwatakado.src.infrastructure.repositories.prize_repository import PrizeRepository
from bwatakado.src.infrastructure.repositories.ticket_repository import TicketRepository


class TestTicketRepository:
    """Test suite for the ticket repository."""

    @pytest.fixture(autouse=True, name="repositories")
    def generate_repositories(self) -> tuple[PrizeRepository, TicketRepository]:
        """Generate the prize repository."""
        prize_repository = PrizeRepository(":memory:")
        ticket_repository = TicketRepository(":memory:")

        ticket_repository.engine = prize_repository.engine
        Base().metadata.create_all(prize_repository.engine)

        return prize_repository, ticket_repository

    def test_find_by_code_returns_none_when_ticket_does_not_exist(
        self, repositories: Tuple[PrizeRepository, TicketRepository]
    ):
        """Test that the repository returns None when the ticket does not exist."""
        _, ticket_repository = repositories

        actual = ticket_repository.find_by_code("0000")

        assert actual is None

    def test_find_by_code_returns_ticket_when_ticket_exists(
        self, repositories: Tuple[PrizeRepository, TicketRepository]
    ):
        """Test that the repository returns the ticket when the ticket exists."""
        prize_repository, ticket_repository = repositories
        prize = Prize("name", "desc", "type", 1)
        prize.generate_tickets(1)
        ticket_code = prize.tickets[prize.tickets_nbr - 1].code
        prize_repository.create_prize(prize)

        actual = ticket_repository.find_by_code(ticket_code)

        assert actual is not None
        assert actual.code == ticket_code
