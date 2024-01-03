from bwatakado.src.domain.entities.province import Province


class Locality:
    """The entity representing a locality"""

    def __init__(
        self,
        identifier: int,
        postcode: int,
        name: str,
        province: Province,
    ):
        if identifier is None:
            raise ValueError("Locality identifier cannot be None")
        self.identifier = identifier

        if province is None:
            raise ValueError("Locality province cannot be None")
        self.province = province

        if postcode is None or len(str(postcode)) < 4:
            raise ValueError(
                "Locality postcode cannot be None or smaller than 4 characters"
            )
        self.postcode = postcode

        if name is None or len(name) == 0:
            raise ValueError("Locality name cannot be None or empty")
        self.name = name
