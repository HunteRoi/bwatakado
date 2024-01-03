from unittest import mock
from unittest.mock import MagicMock

import pytest

from bwatakado.src.application.interfaces.igenerate_tickets import IGenerateTickets
from bwatakado.src.application.use_cases.generate_tickets import GenerateTickets
from bwatakado.src.domain.entities.prize import Prize
from bwatakado.src.domain.exceptions.prize_not_found_error import PrizeNotFoundError


class TestGenerateTickets:
    """Generate one prize's tickets use case test cases."""

    @pytest.fixture(scope="function", autouse=True, name="prize")
    def generate_prize(self) -> Prize:
        """Generate a prize."""

        return Prize(
            prize_id=1,
            name="Test Prize",
            prize_type="Test Type",
            description="Test Description",
            quantity_max=5,
        )

    @mock.patch("bwatakado.src.application.interfaces.iprize_repository")
    def test_generate_tickets_on_already_present_prize(
        self, prize_repository: MagicMock, prize: Prize
    ):
        """Test ticket generation."""

        prize_repository.get_prize.return_value = prize
        use_case: IGenerateTickets = GenerateTickets(prize_repository)

        use_case.execute(prize.id, 20)

        prize_repository.get_prize.assert_called_once_with(prize.id)
        prize_repository.update_prize.assert_called_once_with(prize)

    @mock.patch("bwatakado.src.application.interfaces.iprize_repository")
    def test_generate_tickets_on_not_present_prize(
        self, prize_repository: MagicMock, prize: Prize
    ):
        """Test ticket generation on a non-existent prize."""

        prize_repository.get_prize.return_value = None
        use_case: IGenerateTickets = GenerateTickets(prize_repository)

        with pytest.raises(PrizeNotFoundError):
            use_case.execute(prize.id, 20)

        prize_repository.get_prize.assert_called_once_with(prize.id)
        prize_repository.update_prize.assert_not_called()
