from bwatakado.src.application.interfaces.iprize_repository import IPrizeRepository
from bwatakado.src.application.interfaces.iupdate_prize import IUpdatePrize
from bwatakado.src.application.use_cases.update_prize.update_prize_dto import (
    UpdatePrizeDto,
)
from bwatakado.src.domain.entities.prize import Prize
from bwatakado.src.domain.exceptions.prize_locked_error import PrizeLockedError
from bwatakado.src.domain.exceptions.prize_not_found_error import PrizeNotFoundError


class UpdatePrize(IUpdatePrize):
    """Update prize use case implementation."""

    def __init__(self, prize_repository: IPrizeRepository) -> None:
        self.prize_repository = prize_repository

    def execute(self, prize_id: int, changes: UpdatePrizeDto) -> Prize:
        prize = self.prize_repository.get_prize(prize_id)

        if prize is None:
            raise PrizeNotFoundError(prize_id)

        if prize.all_tickets_generated:
            raise PrizeLockedError()

        if changes.name is not None:
            prize.name = changes.name
        if changes.description is not None:
            prize.description = changes.description
        if changes.prize_type is not None:
            prize.type = changes.prize_type
        if changes.quantity_max is not None:
            prize.quantity_max = changes.quantity_max

        return self.prize_repository.update_prize(prize)
