from bwatakado.src.application.interfaces.iduplicate_prize import IDuplicatePrize
from bwatakado.src.application.interfaces.iprize_repository import IPrizeRepository
from bwatakado.src.domain.entities.prize import Prize
from bwatakado.src.domain.exceptions.prize_not_found_error import PrizeNotFoundError


class DuplicatePrize(IDuplicatePrize):
    """The duplication prize use case"""

    def __init__(self, prize_repository: IPrizeRepository):
        self.prize_repository = prize_repository

    def execute(self, prize_id: int) -> Prize:
        prize_to_duplicate = self.prize_repository.get_prize(prize_id)

        if prize_to_duplicate is None:
            raise PrizeNotFoundError(prize_id)

        clone_prize = Prize(
            prize_to_duplicate.name,
            prize_to_duplicate.description,
            prize_to_duplicate.type,
            prize_to_duplicate.quantity_max
        )
        return self.prize_repository.create_prize(clone_prize)
