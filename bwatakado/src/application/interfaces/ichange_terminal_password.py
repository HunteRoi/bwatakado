from abc import ABC, abstractmethod


class IChangeTerminalPassword(ABC):
    """Interface that provides terminal password changing functionality."""

    @abstractmethod
    def execute(self, current_password: str, new_password: str) -> None:
        """Changes the terminal password."""
