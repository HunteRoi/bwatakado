from unittest import mock

import pytest

from bwatakado.src.domain.entities.terminal import Terminal
from bwatakado.src.infrastructure.services.terminal_json_configuration_service import (
    TerminalJsonConfigurationService,
)


class TestTerminalJsonConfigurationService:
    """Unit tests for TerminalJsonConfigurationService."""

    def test_init(self):
        """Ensure that the TerminalJsonConfigurationService instance is initialized correctly."""

        assert TerminalJsonConfigurationService() is not None

    @pytest.mark.parametrize(
        "path, password",
        [
            ("path/to/file", "admin"),
            ("path/to/other_file", "test"),
        ],
    )
    @mock.patch("builtins.open")
    def test_read(self, open_mock, path, password):
        """Ensure that the terminal configuration is correctly loaded from file."""

        mock.mock_open(
            open_mock, read_data=f'{{ "admin_password": "{password}" }}')
        service = TerminalJsonConfigurationService()

        actual = service.read(path)

        assert actual == Terminal(admin_password=password)
