import pytest

from bwatakado.src.domain.entities.prize import Prize
from bwatakado.src.infrastructure.models.base import Base
from bwatakado.src.infrastructure.repositories.customer_repository import (
    CustomerRepository,
)
from bwatakado.src.infrastructure.repositories.prize_repository import PrizeRepository
from bwatakado.src.infrastructure.repositories.ticket_repository import TicketRepository


class TestTicketRepository:
    """Test suite for the ticket repository."""

    @pytest.fixture(scope="function", autouse=True, name="repositories")
    def generate_repositories(
        self,
    ) -> tuple[PrizeRepository, TicketRepository, CustomerRepository]:
        """Generate the prize repository."""
        customer_repository = CustomerRepository(":memory:")
        prize_repository = PrizeRepository(":memory:")
        ticket_repository = TicketRepository(":memory:")

        ticket_repository.engine = prize_repository.engine
        Base().metadata.create_all(prize_repository.engine)

        return prize_repository, ticket_repository, customer_repository

    def test_find_by_code_returns_none_when_ticket_does_not_exist(
        self, repositories: tuple[PrizeRepository, TicketRepository, CustomerRepository]
    ):
        """Test that the repository returns None when the ticket does not exist."""
        _, ticket_repository, _ = repositories

        actual = ticket_repository.find_by_code("0000")

        assert actual is None

    def test_find_by_code_returns_ticket_when_ticket_exists(
        self, repositories: tuple[PrizeRepository, TicketRepository, CustomerRepository]
    ):
        """Test that the repository returns the ticket when the ticket exists."""
        prize_repository, ticket_repository, _ = repositories
        prize = Prize("name", "desc", "type", 1)
        prize.generate_tickets(1)
        ticket_code = prize.tickets[prize.tickets_nbr - 1].code
        prize_repository.create_prize(prize)

        actual = ticket_repository.find_by_code(ticket_code)

        assert actual is not None
        assert actual.code == ticket_code

    def test_update_tickets_saves_drawn_date(
        self, repositories: tuple[PrizeRepository, TicketRepository, CustomerRepository]
    ):
        """Test that the repository updates the tickets."""
        prize_repository, ticket_repository, _ = repositories
        prize = Prize("name", "desc", "type", 1)
        prize.generate_tickets(1)
        prize = prize_repository.create_prize(prize)
        ticket = prize.tickets[prize.tickets_nbr - 1]

        ticket.draw()
        ticket_repository.update_tickets([ticket])
        received_ticket = ticket_repository.find_by_code(ticket.code)

        assert received_ticket.drawn_at is not None
