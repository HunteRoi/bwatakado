import pytest

from bwatakado.src.domain.entities.terminal import Terminal
from bwatakado.src.infrastructure.services.terminal_json_configuration_service import (
    TerminalJsonConfigurationService,
)


class TestTerminalJsonConfigurationService:
    """Integration tests for TerminalJsonConfigurationService."""

    @pytest.fixture(scope="class")
    def temp_folder(self, tmp_path_factory):
        """Create a temporary folder for the test."""

        base_path = "test_json_config_service"
        complete_path = tmp_path_factory.getbasetemp().joinpath(base_path)

        if complete_path.exists():
            return complete_path

        return str(tmp_path_factory.mktemp(base_path, False))

    def test_write(self, temp_folder):
        """Ensure that the terminal configuration is correctly written to file."""

        service = TerminalJsonConfigurationService()
        path = f"{temp_folder}/test_write"

        service.write(path, Terminal(admin_password="password"))
        terminal = service.read(path)

        assert terminal.admin_password == "password"
