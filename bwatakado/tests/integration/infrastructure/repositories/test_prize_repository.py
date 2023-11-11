import pytest

from bwatakado.src.application.interfaces.iprize_repository import IPrizeRepository
from bwatakado.src.domain.entities.prize import Prize
from bwatakado.src.infrastructure.models.base import Base
from bwatakado.src.infrastructure.repositories.prize_repository import PrizeRepository


class TestPrizeRepository:
    """PrizeRepository test cases."""

    def verify_values(
        self,
        prize: Prize,
        name: str,
        prize_type: str,
        description: str,
        quantity_max: int,
        to_generate: int,
    ):
        """Verify that the values contained in the prize are correct."""

        assert prize is not None
        assert prize.name == name
        assert prize.type == prize_type
        assert prize.description == description
        assert prize.quantity_max == quantity_max
        assert prize.tickets_nbr == to_generate
        assert (
            len([ticket for ticket in prize.tickets if ticket.is_winning])
            == quantity_max
        )
        assert prize.all_tickets_generated

    @pytest.fixture(autouse=True, name="repository")
    def generate_repository(self):
        """Initialize the repository."""

        repository: IPrizeRepository = PrizeRepository(":memory:")
        Base().metadata.create_all(repository.engine)

        return repository

    @pytest.mark.parametrize(
        "name, prize_type, description, quantity_max, to_generate",
        [
            ("test_prize", "test_type", "test_description", 5, 15),
            ("test_prize_2", "test_type_2", "test_description_2", 2, 10),
            ("test_prize_3", "test_type_3", "test_description_3", 30, 30),
        ],
    )
    def test_create_prize(
        self,
        repository,
        name,
        prize_type,
        description,
        quantity_max,
        to_generate,
    ):
        """Ensure that the prize is created correctly."""

        prize = Prize(name, description, prize_type, quantity_max)
        prize.generate_tickets(to_generate)

        created_prize = repository.create_prize(prize)

        self.verify_values(
            created_prize,
            name,
            prize_type,
            description,
            quantity_max,
            to_generate,
        )

    @pytest.mark.parametrize(
        "name, prize_type, description, quantity_max, to_generate",
        [
            ("test_prize", "test_type", "test_description", 5, 15),
            ("test_prize_2", "test_type_2", "test_description_2", 2, 10),
            ("test_prize_3", "test_type_3", "test_description_3", 30, 30),
        ],
    )
    def test_get_prize(
        self,
        repository,
        name,
        prize_type,
        description,
        quantity_max,
        to_generate,
    ):
        """Ensure that a created prize can be retrieved correctly."""

        prize = Prize(name, description, prize_type, quantity_max)
        prize.generate_tickets(to_generate)
        created_prize = repository.create_prize(prize)

        retrieved_prize = repository.get_prize(created_prize.id)

        self.verify_values(
            retrieved_prize, name, prize_type, description, quantity_max, to_generate
        )

    def test_get_unknown_prize(self, repository):
        """Ensure that nothing is returned when no prize is found."""

        retrieved_prize = repository.get_prize(1)

        assert retrieved_prize is None
