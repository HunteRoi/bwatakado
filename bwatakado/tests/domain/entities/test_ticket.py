import unittest
from bwatakado.src.domain.entities.ticket import Ticket

from unittest import mock


class TicketTest(unittest.TestCase):
    @mock.patch('uuid.uuid4', return_value='1')
    def test_winning_ticket_init(self, mock_uuid):
        ticket = Ticket(True)

        self.assertEqual(
            ticket.code,
            mock_uuid.return_value,
            f"Ticket code is not correct, should be {mock_uuid.return_value}, got {ticket.code}"
        )
        self.assertTrue(ticket.is_winning)
        self.assertFalse(ticket.is_printed)

    @mock.patch('uuid.uuid4', return_value='1')
    def test_non_winning_ticket_init(self, mock_uuid):
        ticket = Ticket(False)

        self.assertEqual(
            ticket.code,
            mock_uuid.return_value,
            f"Ticket code is not correct, should be {mock_uuid.return_value}, got {ticket.code}"
        )
        self.assertFalse(ticket.is_winning)