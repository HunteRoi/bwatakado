class PrizeLockedError(Exception):
    """Exception raised when trying to update a prize that has already-generated tickets."""

    def __init__(self):
        super().__init__("Prize tickets already generated.")
