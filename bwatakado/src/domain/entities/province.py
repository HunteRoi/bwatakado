class Province:
    """The entity representing a province"""

    def __init__(self, identifier: int, name: str):
        if identifier is None:
            raise ValueError("Province identifier cannot be None")
        self.identifier = identifier

        if name is None:
            raise ValueError("Province name cannot be None")
        self.name = name
