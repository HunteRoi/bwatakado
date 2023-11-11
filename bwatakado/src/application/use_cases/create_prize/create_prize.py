from bwatakado.src.application.interfaces.icreate_prize import ICreatePrize
from bwatakado.src.application.interfaces.iprize_repository import IPrizeRepository
from bwatakado.src.domain.entities.prize import Prize


class CreatePrize(ICreatePrize):
    """Create prize use case."""

    def __init__(self, prize_repository: IPrizeRepository):
        self.prize_repository = prize_repository

    def execute(self, create_prize_dto: Prize) -> Prize:
        prize = self.prize_repository.create_prize(create_prize_dto)
        return prize
