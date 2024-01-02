from pathlib import Path

from bwatakado.src.application.interfaces.ipassword_service import IPasswordService
from bwatakado.src.application.interfaces.itenant_login import ITenantLogin
from bwatakado.src.application.interfaces.iterminal_configuration_service import (
    ITerminalConfigurationService,
)


class TenantLogin(ITenantLogin):
    """Tenant login use case."""

    def __init__(
        self,
        terminal_configuration_service: ITerminalConfigurationService,
        password_service: IPasswordService,
    ):
        self.__configuration_service = terminal_configuration_service
        self.__password_service = password_service

    def login(self, password: str) -> bool:
        configuration_path = f"{Path.home()}/.bwatakado/terminal_configuration.json"
        terminal = self.__configuration_service.read(configuration_path)

        return self.__password_service.compare(password, terminal.admin_password)
