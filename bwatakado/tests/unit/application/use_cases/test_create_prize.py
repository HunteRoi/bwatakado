from unittest import mock
from unittest.mock import MagicMock

import pytest

from bwatakado.src.application.use_cases.create_prize.create_prize import CreatePrize
from bwatakado.src.domain.entities.prize import Prize


class TestCreatePrize:
    """CreatePrize test cases."""

    @pytest.mark.parametrize(
        "name, prize_type, description, quantity_max",
        [
            (
                "test_name_1",
                "test_type_1",
                "test_description_1",
                1,
            ),
            (
                "test_name_2",
                "test_type_2",
                "test_description_2",
                10,
            ),
            (
                "test_name_3",
                "test_type_3",
                "test_description_3",
                20,
            ),
        ],
    )
    @mock.patch("bwatakado.src.application.interfaces.iprize_repository")
    def test_create_prize(
        self,
        create_prize_repository: MagicMock,
        name: str,
        prize_type: str,
        description: str,
        quantity_max: int,
    ):
        """Test prize creation ability."""

        prize = Prize(name, description, prize_type, quantity_max)
        create_prize_repository.create_prize.return_value = prize
        use_case = CreatePrize(create_prize_repository)

        received_prize = use_case.execute(prize)

        create_prize_repository.create_prize.assert_called_once_with(prize)
        assert received_prize == prize
