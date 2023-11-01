class PrizeLockedError(Exception):
    def __init__(self):
        super().__init__("Prize tickets already generated.")
