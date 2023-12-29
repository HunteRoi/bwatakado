from bwatakado.src.application.interfaces.igenerate_tickets import IGenerateTickets
from bwatakado.src.application.interfaces.iprize_repository import IPrizeRepository
from bwatakado.src.domain.exceptions.prize_not_found_error import PrizeNotFoundError


class GenerateTickets(IGenerateTickets):
    """GenerateTickets use case"""

    def __init__(self, prize_repository: IPrizeRepository):
        self.prize_repository = prize_repository

    def execute(self, prize_id: int, tickets_to_generate: int):
        prize_for_generation = self.prize_repository.get_prize(prize_id)

        if prize_for_generation is None:
            raise PrizeNotFoundError(prize_id)

        prize_for_generation.generate_tickets(tickets_to_generate)
        self.prize_repository.update_prize(prize_for_generation)
