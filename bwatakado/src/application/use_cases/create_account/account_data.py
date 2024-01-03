from dataclasses import dataclass

from bwatakado.src.domain.value_objects.address import Address


@dataclass
class AccountData:
    """Account data class."""

    firstname: str
    lastname: str
    phone_number: str
    email: str
    address: Address
    pin_code: str
    locality_id: int
