from abc import ABC

from bwatakado.src.application.use_cases.update_prize.update_prize_dto import (
    UpdatePrizeDto,
)
from bwatakado.src.domain.entities.prize import Prize


class IUpdatePrize(ABC):
    """Interface that provides prize update functionalities."""

    def execute(self, prize_id: int, changes: UpdatePrizeDto) -> Prize:
        """Updates the prize."""
