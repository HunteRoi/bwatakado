from dataclasses import dataclass


@dataclass
class Address:
    """Address value object."""

    city: str
    state: str
    country: str
    zipcode: str
    street: str | None = None
    number: int | None = None
    complement: str | None = None

    def to_str(self):
        """Convert the address to a string."""
        return "|".join(
            [
                self.city,
                self.state,
                self.country,
                self.zipcode,
                self.street or "",
                str(self.number or ""),
                self.complement or "",
            ]
        )

    @classmethod
    def from_str(cls, address: str):
        """Convert the string to an address."""
        address_list = address.split("|")

        return cls(
            city=address_list[0],
            state=address_list[1],
            country=address_list[2],
            zipcode=address_list[3],
            street=address_list[4] or None,
            number=int(address_list[5])
            if (
                address_list[5]
                and len(address_list[5]) > 0
                and address_list[5].isnumeric()
            )
            else None,
            complement=address_list[6] or None,
        )

    def __post_init__(self):
        if not self.city or not isinstance(self.city, str) or not self.city.isalpha():
            raise ValueError("Address must have a city")

        if (
            not self.state
            or not isinstance(self.state, str)
            or not self.state.isalpha()
        ):
            raise ValueError("Address must have a state")

        if (
            not self.country
            or not isinstance(self.country, str)
            or not self.country.isalpha()
        ):
            raise ValueError("Address must have a country")

        if (
            not self.zipcode
            or not isinstance(self.zipcode, str)
            or not self.zipcode.isnumeric()
        ):
            raise ValueError("Address must have a zipcode")

        if self.street is not None and (
            not isinstance(self.street, str) or not self.street.isalpha() or len(
                self.street) == 0
        ):
            raise ValueError(
                "Street must be a non-empty string of alphabetic characters"
            )

        if self.number is not None and not isinstance(self.number, int):
            raise ValueError("Number must be a non-empty integer")

        if self.complement is not None and (
            not isinstance(self.complement, str) or len(self.complement) == 0
        ):
            raise ValueError(
                "Complement must be a non-empty string"
            )
