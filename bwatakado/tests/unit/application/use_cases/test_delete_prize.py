from unittest import mock
from unittest.mock import MagicMock

import pytest

from bwatakado.src.application.use_cases.delete_prize import DeletePrize
from bwatakado.src.domain.entities.prize import Prize
from bwatakado.src.domain.exceptions.prize_not_found_error import PrizeNotFoundError


class TestDeletePrize:
    """DeletePrize use case test cases."""

    @mock.patch("bwatakado.src.application.interfaces.iprize_repository")
    def test_delete_prize(self, prize_repository: MagicMock):
        """Test prize deletion."""

        prize = Prize(
            prize_id=1,
            name="Test Prize",
            prize_type="Test Type",
            description="Test Description",
            quantity_max=10,
        )
        prize_repository.get_prize.return_value = prize
        use_case = DeletePrize(prize_repository)

        use_case.execute(prize.id)

        prize_repository.get_prize.assert_called_once_with(prize.id)
        prize_repository.delete_prize.assert_called_once_with(prize)

    @mock.patch("bwatakado.src.application.interfaces.iprize_repository")
    def test_delete_prize_with_invalid_id(self, prize_repository: MagicMock):
        """Test prize deletion with invalid id."""

        id_to_delete = 1
        prize_repository.get_prize.return_value = None
        use_case = DeletePrize(prize_repository)

        with pytest.raises(PrizeNotFoundError):
            use_case.execute(id_to_delete)

        prize_repository.get_prize.assert_called_once_with(id_to_delete)
        prize_repository.delete_prize.assert_not_called()
