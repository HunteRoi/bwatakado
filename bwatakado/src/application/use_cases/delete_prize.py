from bwatakado.src.application.interfaces.idelete_prize import IDeletePrize
from bwatakado.src.domain.exceptions.prize_not_found_error import PrizeNotFoundError


class DeletePrize(IDeletePrize):
    """Delete prize use case."""

    def __init__(self, prize_repository):
        self.prize_repository = prize_repository

    def execute(self, prize_id: int):
        prize = self.prize_repository.get_prize(prize_id)

        if prize is None:
            raise PrizeNotFoundError(prize_id)

        self.prize_repository.delete_prize(prize)
