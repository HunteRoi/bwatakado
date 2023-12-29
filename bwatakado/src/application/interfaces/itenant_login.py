from abc import ABC, abstractmethod


class ITenantLogin(ABC):
    """Interface that provides establishment owner login functionalities."""

    @abstractmethod
    def login(self, password: str) -> bool:
        """Logs in the establishment owner."""
