import json

from bwatakado.src.application.interfaces.iterminal_configuration_service import (
    ITerminalConfigurationService,
)
from bwatakado.src.domain.entities.terminal import Terminal


class TerminalJsonConfigurationService(ITerminalConfigurationService):
    """Reads and writes terminal configuration from and to a JSON file."""

    def read(self, path: str) -> Terminal:
        """Reads the terminal configuration from a JSON file and returns the Terminal instance."""

        with open(path, "r") as file:
            configuration = json.load(file)
            return Terminal(admin_password=configuration["admin_password"])

    def write(self, path: str, data: Terminal) -> None:
        """Writes the terminal configuration to a JSON file."""
        with open(path, "w") as file:
            json.dump(data.__dict__, file)
