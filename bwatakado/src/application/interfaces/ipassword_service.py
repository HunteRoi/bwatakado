from abc import ABC, abstractmethod


class IPasswordService(ABC):
    """Interface that provides password-based hashing and comparison functionality."""

    @abstractmethod
    def hash(self, password: str) -> str:
        """Hash a password."""

    @abstractmethod
    def compare(self, password: str, hashed_password: str) -> bool:
        """Compare a password with a hashed password."""
