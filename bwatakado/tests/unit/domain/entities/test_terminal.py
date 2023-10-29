from bwatakado.src.domain.entities.terminal import Terminal


class TestTerminal:
    """Unit tests for Terminal."""

    def test_init_with_password(self):
        """Test that Terminal is initialized with a password correctly."""
        terminal = Terminal("password")

        assert terminal.admin_password == "password"

    def test_set_admin_password(self):
        """Test that Terminal.admin_password can be set/updated."""
        terminal = Terminal("password")

        terminal.admin_password = "new_password"

        assert terminal.admin_password == "new_password"
