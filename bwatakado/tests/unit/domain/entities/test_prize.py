import pytest

from bwatakado.src.domain.entities.prize import Prize
from bwatakado.src.domain.exceptions.prize_locked_error import PrizeLockedError


class TestPrize:
    """Unit tests for Prize."""

    @pytest.fixture(autouse=True, name="prize")
    def setup_before_each(self):
        """Setup before each test."""

        return Prize("test name", "description test", "test type", 0)

    def test_init(self, prize):
        """Test that Prizes are initialized correctly."""

        assert prize.name == "test name"
        assert prize.description == "description test"
        assert prize.type == "test type"
        assert prize.quantity_max == 0
        assert prize.tickets == []

        assert prize.tickets_nbr == 0
        assert prize.quantity_redeemed == 0
        assert not prize.all_tickets_generated

    def test_generate_tickets(self, prize):
        """Test that tickets are generated."""

        prize.generate_tickets(5)

        assert prize.tickets_nbr == 5
        assert prize.all_tickets_generated

    @pytest.mark.parametrize("number", [0, -1, -2, -3, -4, -5])
    def test_generate_negative_or_zero_number_of_tickets(self, prize, number):
        """Test that negative (0 included) number of tickets cannot be generated."""

        with pytest.raises(ValueError):
            prize.generate_tickets(number)

    @pytest.mark.parametrize(
        "quantity_max, to_generate",
        [(1, 1), (1, 2), (2, 2), (2, 3), (3, 8)],
    )
    def test_generate_one_winning_ticket(self, prize, quantity_max, to_generate):
        """Test that one winning ticket is generated."""

        prize.quantity_max = quantity_max
        prize.generate_tickets(to_generate)

        assert (
            len([ticket for ticket in prize.tickets if ticket.is_winning])
            == quantity_max
        )

    def test_generate_no_winning_ticket(self, prize):
        """Test that we cannot generate other tickets after a first pass."""

        prize.generate_tickets(5)

        with pytest.raises(PrizeLockedError):
            prize.generate_tickets(5)

        assert prize.tickets_nbr == 5
