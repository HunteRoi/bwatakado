class PrizeNotFoundError(Exception):
    """Raised when the prize is not found in the database."""

    def __init__(self, prize_id: int):
        self.message = f"Prize with id {prize_id} does not exist."
        super().__init__(self.message)
