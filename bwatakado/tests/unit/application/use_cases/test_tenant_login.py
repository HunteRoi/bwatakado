from unittest import mock
from unittest.mock import MagicMock

from bwatakado.src.application.interfaces.itenant_login import ITenantLogin
from bwatakado.src.application.use_cases.tenant_login import TenantLogin
from bwatakado.src.domain.entities.terminal import Terminal


class TestTenantLogin:
    """Tenant login use case test cases."""

    @mock.patch(
        "bwatakado.src.infrastructure.services.terminal_json_configuration_service"
        ".TerminalJsonConfigurationService"
    )
    @mock.patch("bwatakado.src.application.interfaces.ipassword_service")
    def test_tenant_login(
        self,
        password_service_mock: MagicMock,
        terminal_json_configuration_service_mock: MagicMock,
    ):
        """Test tenant login ability."""

        use_case: ITenantLogin = TenantLogin(
            terminal_json_configuration_service_mock, password_service_mock
        )
        terminal_json_configuration_service_mock.read.return_value = Terminal(
            "password"
        )
        password_service_mock.compare.return_value = True

        use_case.login("password")

        terminal_json_configuration_service_mock.read.assert_called_once()
        password_service_mock.compare.assert_called_once_with("password", "password")
