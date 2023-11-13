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
        expected_tickets_nbr: int,
    ):
        """Verify that the values contained in the prize are correct."""

        assert prize is not None
        assert prize.name == name
        assert prize.type == prize_type
        assert prize.description == description
        assert prize.quantity_max == quantity_max
        assert prize.tickets_nbr == expected_tickets_nbr

        if expected_tickets_nbr == 0:
            assert not prize.all_tickets_generated

    @pytest.fixture(autouse=True, name="repository")
    def generate_repository(self) -> IPrizeRepository:
        """Initialize the repository."""

        repository: IPrizeRepository = PrizeRepository(":memory:")
        Base().metadata.create_all(repository.engine)

        return repository

    @pytest.mark.parametrize(
        "name, prize_type, description, quantity_max, tickets_to_generate_nbr",
        [
            ("test_prize", "test_type", "test_description", 5, 15),
            ("test_prize_2", "test_type_2", "test_description_2", 2, 10),
            ("test_prize_3", "test_type_3", "test_description_3", 30, 30),
        ],
    )
    def test_create_prize(
        self,
        repository: IPrizeRepository,
        name: str,
        prize_type: str,
        description: str,
        quantity_max: int,
        tickets_to_generate_nbr: int,
    ):
        """Ensure that the prize is created correctly."""

        prize = Prize(name, description, prize_type, quantity_max)
        prize.generate_tickets(tickets_to_generate_nbr)

        created_prize = repository.create_prize(prize)

        self.verify_values(
            created_prize,
            name,
            prize_type,
            description,
            quantity_max,
            tickets_to_generate_nbr,
        )
        assert (
            len([ticket for ticket in created_prize.tickets if ticket.is_winning])
            == quantity_max
        )

    @pytest.mark.parametrize(
        "name, prize_type, description, quantity_max, tickets_to_generate_nbr",
        [
            ("test_prize", "test_type", "test_description", 5, 15),
            ("test_prize_2", "test_type_2", "test_description_2", 2, 10),
            ("test_prize_3", "test_type_3", "test_description_3", 30, 30),
        ],
    )
    def test_get_prize(
        self,
        repository: IPrizeRepository,
        name: str,
        prize_type: str,
        description: str,
        quantity_max: int,
        tickets_to_generate_nbr: int,
    ):
        """Ensure that a created prize can be retrieved correctly."""

        prize = Prize(name, description, prize_type, quantity_max)
        prize.generate_tickets(tickets_to_generate_nbr)
        created_prize = repository.create_prize(prize)

        retrieved_prize = repository.get_prize(created_prize.id)

        self.verify_values(
            retrieved_prize,
            name,
            prize_type,
            description,
            quantity_max,
            tickets_to_generate_nbr,
        )
        assert (
            len([ticket for ticket in retrieved_prize.tickets if ticket.is_winning])
            == quantity_max
        )

    def test_get_unknown_prize(self, repository: IPrizeRepository):
        """Ensure that nothing is returned when no prize is found."""

        retrieved_prize = repository.get_prize(1)

        assert retrieved_prize is None

    @pytest.mark.parametrize(
        "new_name, new_type, new_description, quantity_max",
        [
            ("test_prize", "test_type", "test_description", 5),
            ("test_prize_2", "test_type_2", "test_description_2", 2),
            ("test_prize_3", "test_type_3", "test_description_3", 30),
        ],
    )
    def test_update_prize(
        self,
        repository: IPrizeRepository,
        new_name: str,
        new_type: str,
        new_description: str,
        quantity_max: int,
    ):
        """Ensure that a prize can be updated correctly."""

        prize = Prize("test_prize", "test_description", "test_type", 5)
        prize = repository.create_prize(prize)

        updated_prize = repository.update_prize(
            Prize(
                new_name,
                new_description,
                new_type,
                quantity_max,
                prize.id,
                prize.tickets,
                prize.all_tickets_generated,
            )
        )

        self.verify_values(
            updated_prize, new_name, new_type, new_description, quantity_max, 0
        )
