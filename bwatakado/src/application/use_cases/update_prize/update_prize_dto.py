class UpdatePrizeDto:
    """Data transfer object for updating prizes."""

    def __init__(
        self,
        name: str = None,
        description: str = None,
        prize_type: str = None,
        quantity_max: int = None,
    ):
        self.name = name
        self.description = description
        self.prize_type = prize_type
        self.quantity_max = quantity_max
