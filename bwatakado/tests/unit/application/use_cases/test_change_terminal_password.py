from unittest import mock
from unittest.mock import MagicMock

from bwatakado.src.application.use_cases.change_terminal_password import (
    ChangeTerminalPassword,
)
from bwatakado.src.domain.entities.terminal import Terminal


class TestChangeTerminalPassword:
    """ChangeTerminalPassword test cases."""

    @mock.patch("bwatakado.src.application.interfaces.iterminal_configuration_service")
    @mock.patch("bwatakado.src.application.interfaces.ipassword_service")
    def test_change_terminal_password_with_right_current_password(
            self,
            terminal_configuration_service_mock: MagicMock,
            password_service_mock: MagicMock,
    ):
        """Test change terminal password with right current password."""

        current_password = "password"
        new_password = "new_password"
        use_case = ChangeTerminalPassword(
            terminal_configuration_service_mock, password_service_mock
        )
        terminal_configuration_service_mock.read.return_value = Terminal(
            current_password
        )
        password_service_mock.hash.return_value = "hashed_password"
        password_service_mock.compare.return_value = True

        use_case.execute(current_password, new_password)

        terminal_configuration_service_mock.read.assert_called_once()
        password_service_mock.compare.assert_called_once()
        password_service_mock.hash.assert_called_once()
        terminal_configuration_service_mock.write.assert_called_once()

    @mock.patch("bwatakado.src.application.interfaces.iterminal_configuration_service")
    @mock.patch("bwatakado.src.application.interfaces.ipassword_service")
    def test_change_terminal_with_wrong_current_password(
            self,
            terminal_configuration_service_mock: MagicMock,
            password_service_mock: MagicMock,
    ):
        """Test change terminal password with wrong current password."""

        current_password = "password"
        new_password = "new_password"
        use_case = ChangeTerminalPassword(
            terminal_configuration_service_mock, password_service_mock
        )
        terminal_configuration_service_mock.read.return_value = Terminal(
            current_password
        )
        password_service_mock.compare.return_value = False

        use_case.execute(current_password, new_password)

        terminal_configuration_service_mock.read.assert_called_once()
        password_service_mock.compare.assert_called_once()
        password_service_mock.hash.assert_not_called()
        terminal_configuration_service_mock.write.assert_not_called()
