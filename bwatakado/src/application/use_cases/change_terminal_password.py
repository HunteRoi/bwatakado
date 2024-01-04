from pathlib import Path

from bwatakado.src.application.interfaces.ichange_terminal_password import (
    IChangeTerminalPassword,
)
from bwatakado.src.application.interfaces.ipassword_service import IPasswordService
from bwatakado.src.application.interfaces.iterminal_configuration_service import (
    ITerminalConfigurationService,
)


class ChangeTerminalPassword(IChangeTerminalPassword):
    """Change terminal password use case."""

    def __init__(
        self,
        terminal_configuration_service: ITerminalConfigurationService,
        password_service: IPasswordService,
    ):
        self.configuration_service = terminal_configuration_service
        self.password_service = password_service

    def execute(self, current_password: str, new_password: str) -> None:
        configuration_path = f"{Path.home()}/.bwatakado/terminal_configuration.json"
        terminal = self.configuration_service.read(configuration_path)

        if self.password_service.compare(current_password, terminal.admin_password):
            terminal.admin_password = self.password_service.hash(new_password)
            self.configuration_service.write(configuration_path, terminal)
