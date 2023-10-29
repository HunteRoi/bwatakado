from unittest import mock

from bwatakado.src.domain.entities.ticket import Ticket


class TestTicket:
    """Unit tests for Ticket."""

    @mock.patch('uuid.uuid4', return_value='1')
    def test_winning_ticket_init(self, mock_uuid):
        """Test that a winning Ticket is initialized correctly."""
        ticket = Ticket(True)

        assert ticket.code == mock_uuid.return_value, \
            f"Ticket code is not correct, should be {
                mock_uuid.return_value}, got {ticket.code}"
        assert ticket.is_winning

    @mock.patch('uuid.uuid4', return_value='1')
    def test_non_winning_ticket_init(self, mock_uuid):
        """Test that a non-winning Ticket is initialized correctly."""
        ticket = Ticket(False)

        assert ticket.code == mock_uuid.return_value, \
            f"Ticket code is not correct, should be {
                mock_uuid.return_value}, got {ticket.code}"

        assert not ticket.is_winning
