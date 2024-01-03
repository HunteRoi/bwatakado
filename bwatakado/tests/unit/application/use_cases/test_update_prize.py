from unittest import mock
from unittest.mock import MagicMock

import pytest

from bwatakado.src.application.use_cases.update_prize.update_prize import UpdatePrize
from bwatakado.src.application.use_cases.update_prize.update_prize_dto import (
    UpdatePrizeDto,
)
from bwatakado.src.domain.entities.prize import Prize
from bwatakado.src.domain.exceptions.prize_locked_error import PrizeLockedError
from bwatakado.src.domain.exceptions.prize_not_found_error import PrizeNotFoundError


class TestUpdatePrize:
    """UpdatePrize use case test cases."""

    @pytest.fixture(scope="function", autouse=True, name="base_prize")
    def generate_base_prize(self):
        """Generate a base prize."""

        return Prize("test_name", "test_description", "test_type", 1, 1)

    @pytest.mark.parametrize(
        "new_name, new_description, new_type, quantity_max",
        [
            ("new_name", "new_description", "new_type", 2),
            ("new_name_2", "new_description_2", "new_type_2", 3),
            ("new_name_3", "new_description_3", "new_type_3", 4),
        ],
    )
    @mock.patch("bwatakado.src.application.interfaces.iprize_repository")
    def test_update_prize_with_no_generated_tickets(
        self,
        prize_repo: MagicMock,
        base_prize: Prize,
        new_name: str,
        new_description: str,
        new_type: str,
        quantity_max: int,
    ):
        """Test prize update ability."""

        prize_repo.get_prize.return_value = base_prize
        prize_repo.update_prize.return_value = Prize(
            new_name, new_description, new_type, quantity_max, base_prize.id
        )
        use_case = UpdatePrize(prize_repo)

        received_prize = use_case.execute(
            base_prize.id,
            UpdatePrizeDto(
                name=new_name,
                description=new_description,
                prize_type=new_type,
                quantity_max=quantity_max,
            ),
        )

        prize_repo.update_prize.assert_called_once_with(base_prize)
        assert received_prize == prize_repo.update_prize.return_value

    @mock.patch("bwatakado.src.application.interfaces.iprize_repository")
    def test_update_prize_with_generated_tickets(
        self, prize_repo: MagicMock, base_prize: Prize
    ):
        """Test that it is impossible to update a prize when its tickets are generated."""

        base_prize.generate_tickets(5)
        prize_repo.get_prize.return_value = base_prize
        use_case = UpdatePrize(prize_repo)

        with pytest.raises(PrizeLockedError):
            use_case.execute(
                base_prize.id,
                UpdatePrizeDto(
                    name="new_name",
                    description="new_description",
                    prize_type="new_type",
                    quantity_max=2,
                ),
            )

        prize_repo.update_prize.assert_not_called()

    @mock.patch("bwatakado.src.application.interfaces.iprize_repository")
    def test_update_prize_with_invalid_prize_id(self, prize_repo: MagicMock):
        """Test that a user cannot update an unknown prize"""

        prize_repo.get_prize.return_value = None
        use_case = UpdatePrize(prize_repo)

        with pytest.raises(PrizeNotFoundError):
            use_case.execute(
                1,
                UpdatePrizeDto(
                    name="new_name",
                    description="new_description",
                    prize_type="new_type",
                    quantity_max=2,
                ),
            )

        prize_repo.update_prize.assert_not_called()

    @pytest.mark.parametrize(
        "new_name, description, new_type, quantity_max",
        [
            ("new_name", "new_description", "new_type", 2),
            ("new_name_2", "new_description_2", "new_type_2", 3),
            ("new_name_3", "new_description_3", "new_type_3", 4),
        ],
    )
    @mock.patch("bwatakado.src.application.interfaces.iprize_repository")
    def test_update_prize_with_missing_values_in_dto(
        self,
        prize_repo: MagicMock,
        base_prize: Prize,
        new_name: str,
        description: str,
        new_type: str,
        quantity_max: int,
    ):
        """Test prize update with missing values in dto."""

        prize_repo.get_prize.return_value = base_prize
        prize_repo.update_prize.return_value = Prize(
            new_name, description, new_type, quantity_max, base_prize.id
        )
        use_case = UpdatePrize(prize_repo)

        received_prize = use_case.execute(
            base_prize.id,
            UpdatePrizeDto(
                name=new_name,
                description=description,
                prize_type=new_type,
            ),
        )

        prize_repo.update_prize.assert_called_once_with(base_prize)
        assert received_prize == prize_repo.update_prize.return_value
