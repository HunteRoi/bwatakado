from unittest import mock
from unittest.mock import MagicMock

import pytest

from bwatakado.src.domain.exceptions.prize_not_found_error import PrizeNotFoundError
from bwatakado.src.application.use_cases.duplicate_prize import DuplicatePrize
from bwatakado.src.domain.entities.prize import Prize


class TestDuplicatePrize:
    """Test suite around duplicating a prize."""

    @pytest.fixture(scope="function", autouse=True, name="prize")
    def generate_new_prize(self):
        """Generates a prize with no tickets"""
        return Prize("name", "desc", "type", 5)

    @mock.patch("bwatakado.src.application.interfaces.iprize_repository")
    def test_create_use_case(self, mock_prize_repository: MagicMock):
        """Validates that it is possible to create the use case"""
        assert DuplicatePrize(mock_prize_repository) is not None

    @mock.patch("bwatakado.src.application.interfaces.iprize_repository")
    def test_duplicate_prize_raises_error_when_prize_does_not_exist(
        self,
        prize_repository: MagicMock
    ):
        """Validates that it is not possible to duplicate an unexisting prize."""

        prize_id = 1
        prize_repository.get_prize.return_value = None
        use_case = DuplicatePrize(prize_repository)

        with pytest.raises(PrizeNotFoundError):
            use_case.execute(prize_id)
        prize_repository.get_prize.assert_called_once_with(prize_id)
        prize_repository.create_prize.not_assert_called_once()

    @mock.patch("bwatakado.src.application.interfaces.iprize_repository")
    def test_duplicate_prize(
        self,
        prize_repository: MagicMock,
        prize: Prize
    ):
        """Validates that it is possible to duplicate a prize."""

        prize_repository.get_prize.return_value = prize
        use_case = DuplicatePrize(prize_repository)

        received_prize = use_case.execute(prize.id)

        prize_repository.get_prize.assert_called_once_with(prize.id)
        prize_repository.create_prize.assert_called_once()
        assert received_prize != prize
