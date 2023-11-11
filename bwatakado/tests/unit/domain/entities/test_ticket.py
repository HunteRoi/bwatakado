from unittest import mock

import pytest

from bwatakado.src.domain.entities.ticket import Ticket


class TestTicket:
    """Unit tests for Ticket."""

    @mock.patch("uuid.uuid4", return_value="1")
    def test_winning_ticket_init(self, mock_uuid):
        """Test that a winning Ticket is initialized correctly."""
        ticket = Ticket(True)

        assert (
            ticket.code == mock_uuid.return_value
        ), f"Ticket code is not correct, should be {mock_uuid.return_value}, got {ticket.code}"
        assert ticket.is_winning

    @mock.patch("uuid.uuid4", return_value="1")
    def test_non_winning_ticket_init(self, mock_uuid):
        """Test that a non-winning Ticket is initialized correctly."""
        ticket = Ticket(False)

        assert (
            ticket.code == mock_uuid.return_value
        ), f"Ticket code is not correct, should be {mock_uuid.return_value}, got {ticket.code}"

        assert not ticket.is_winning

    def test_ticket_equality(self):
        """Test that two tickets are equal."""
        ticket_1 = Ticket(True)
        ticket_2 = Ticket(
            True,
            code=ticket_1.code,
            created_at=ticket_1.created_at,
            is_printed=ticket_1.is_printed,
            has_been_claimed=ticket_1.has_been_claimed,
        )

        assert ticket_1 == ticket_2

    @pytest.mark.parametrize(
        "other_value", ["test", 0, 0.4, Ticket(False), Ticket(True)]
    )
    def test_ticket_inequality(self, other_value):
        """Test that a ticket is not equal to other objects."""

        assert Ticket(True) != other_value
