import pytest

from bwatakado.src.domain.entities.prize import Prize
from bwatakado.src.domain.exceptions.prize_locked_error import PrizeLockedError


class TestPrize:
    """Unit tests for Prize."""

    @pytest.fixture(autouse=True, name="prize")
    def setup_before_each(self):
        """Setup before each test."""

        return Prize("test name", "description test", "test type", 0, 1)

    def test_init(self, prize):
        """Test that Prizes are initialized correctly."""

        assert prize.id == 1
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

    def test_prize_equality(self):
        """Test that two prizes are equal."""

        prize_1 = Prize("test name", "description test", "test type", 0)
        prize_2 = Prize("test name", "description test",
                        "test type", 0, prize_1.id)

        assert prize_1 == prize_2

    @pytest.mark.parametrize(
        "other_value",
        [
            0,
            "other value",
            0.4,
            Prize("test name", "description test", "test type", 0),
            Prize("test name", "description test", "test type", 2),
        ],
    )
    def test_prize_inequality(self, other_value):
        """Test that a prize is not equal to other objects."""

        assert Prize("test name", "description test",
                     "test type", 2, 1) != other_value
