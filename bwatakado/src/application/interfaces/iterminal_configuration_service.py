from abc import ABC, abstractmethod

from bwatakado.src.domain.entities.terminal import Terminal


class ITerminalConfigurationService(ABC):
    """Interface that provides file-based terminal configuration reading
    and writing functionality."""

    @abstractmethod
    def read(self, path: str) -> Terminal:
        """Reads the terminal configuration from a file and returns the Terminal instance."""

    @abstractmethod
    def write(self, path: str, data: Terminal) -> None:
        """Writes the terminal configuration to a file."""
