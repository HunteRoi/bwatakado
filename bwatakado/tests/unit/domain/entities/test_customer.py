import pytest

from bwatakado.src.domain.entities.customer import Customer
from bwatakado.src.domain.entities.locality import Locality
from bwatakado.src.domain.entities.province import Province
from bwatakado.src.domain.entities.ticket import Ticket
from bwatakado.src.domain.exceptions.ticket_already_claimed_error import (
    TicketAlreadyClaimedError,
)
from bwatakado.src.domain.value_objects.address import Address


class TestCustomer:
    """Test suite on a customer entity"""

    @pytest.mark.parametrize("firstname", ["", None, "1234"])
    def test_create_customer_raises_value_error_when_invalid_firstname(
        self, firstname: str
    ):
        """Test that a value error is raised when an invalid firstname is provided"""
        with pytest.raises(ValueError):
            Customer(
                firstname,
                "lastname",
                "0000000000",
                "e@e.c",
                "address",
                "0000",
                Locality(1, 1000, "Bruxelles", Province(1, "Bruxelles")),
            )

    @pytest.mark.parametrize("lastname", ["", None, "1234"])
    def test_create_customer_raises_value_error_when_invalid_lastname(
        self, lastname: str
    ):
        """Test that a value error is raised when an invalid lastname is provided"""
        with pytest.raises(ValueError):
            Customer(
                "firstname",
                lastname,
                "0000000000",
                "e@e.c",
                "address",
                "0000",
                Locality(1, 1000, "Bruxelles", Province(1, "Bruxelles")),
            )

    @pytest.mark.parametrize("phone_number", ["", None, "1234"])
    def test_create_customer_raises_value_error_when_invalid_phone_number(
        self, phone_number: str
    ):
        """Test that a value error is raised when an invalid phone number is provided"""
        with pytest.raises(ValueError):
            Customer(
                "firstname",
                "lastname",
                phone_number,
                "e@e.c",
                "address",
                "0000",
                Locality(1, 1000, "Bruxelles", Province(1, "Bruxelles")),
            )

    @pytest.mark.parametrize("email", ["", None, "abc", "abc@com"])
    def test_create_customer_raises_value_error_when_invalid_email(self, email: str):
        """Test that a value error is raised when an invalid email is provided"""
        with pytest.raises(ValueError):
            Customer(
                "firstname",
                "lastname",
                "0000000000",
                email,
                "address",
                "0000",
                Locality(1, 1000, "Bruxelles", Province(1, "Bruxelles")),
            )

    @pytest.mark.parametrize("address", [None, ""])
    def test_create_customer_raises_value_error_when_invalid_address(
        self, address: str
    ):
        """Test that a value error is raised when an invalid address is provided"""
        with pytest.raises(ValueError):
            Customer(
                "firstname",
                "lastname",
                "0000000000",
                "e@e.c",
                address,
                "0000",
                Locality(1, 1000, "Bruxelles", Province(1, "Bruxelles")),
            )

    @pytest.mark.parametrize("pin_code", ["", None, "abc"])
    def test_create_customer_raises_value_error_when_invalid_pin_code(
        self, pin_code: str
    ):
        """Test that a value error is raised when an invalid pin code is provided"""
        with pytest.raises(ValueError):
            Customer(
                "firstname",
                "lastname",
                "0000000000",
                "e@e.c",
                Address("city", "state", "country", "0000"),
                pin_code,
                Locality(1, 1000, "Bruxelles", Province(1, "Bruxelles")),
            )

    @pytest.mark.parametrize("locality", [None, ""])
    def test_create_customer_raises_value_error_when_invalid_locality(
        self, locality: Locality
    ):
        """Test that a value error is raised when an invalid locality is provided"""
        with pytest.raises(ValueError):
            Customer(
                "firstname",
                "lastname",
                "0000000000",
                "e@e.c",
                Address("city", "state", "country", "0000"),
                "0000",
                locality,
            )

    @pytest.mark.parametrize(
        "firstname, lastname, phone_number, email, address, pin_code, locality",
        [
            (
                "firstname",
                "lastname",
                "0000000000",
                "email@example.com",
                Address("city", "state", "country", "0000"),
                "0000",
                Locality(1, 1000, "Bruxelles", Province(1, "Bruxelles")),
            ),
            (
                "f",
                "l",
                "0000000000",
                "e@e.c",
                Address("city", "state", "country", "0000"),
                "1234",
                Locality(1, 1000, "Bruxelles", Province(1, "Bruxelles")),
            ),
        ],
    )
    def test_initialize_customer(
        self,
        firstname: str,
        lastname: str,
        phone_number: str,
        email: str,
        address: str,
        pin_code: str,
        locality: Locality,
    ):
        """Validates that initializing a customer with the provided values does so properly."""
        customer = Customer(
            firstname, lastname, phone_number, email, address, pin_code, locality
        )

        assert customer is not None
        assert customer.firstname == firstname
        assert customer.lastname == lastname
        assert customer.phone_number == phone_number
        assert customer.email == email
        assert customer.address == address
        assert customer.pin_code == pin_code
        assert customer.locality == locality

    @pytest.mark.parametrize("is_winning_ticket", [True, False])
    def test_add_ticket(self, is_winning_ticket: bool):
        """Validates that a ticket can be added to a customer's list of tickets"""
        customer = Customer(
            "firstname",
            "lastname",
            "0000000000",
            "e@e.c",
            Address("city", "state", "country", "0000"),
            "0000",
            Locality(1, 1000, "Bruxelles", Province(1, "Bruxelles")),
        )
        ticket = Ticket(is_winning_ticket)

        customer.add_ticket(ticket)

        assert ticket in customer.tickets

    @pytest.mark.parametrize("is_winning_ticket", [True, False])
    def test_add_ticket_fails_if_ticket_is_already_claimed(
        self, is_winning_ticket: bool
    ):
        """Validates that adding an already claimed ticket to a customer's list
        of tickets is not possible"""
        customer = Customer(
            "firstname",
            "lastname",
            "0000000000",
            "e@e.c",
            Address("city", "state", "country", "0000"),
            "0000",
            Locality(1, 1000, "Bruxelles", Province(1, "Bruxelles")),
        )
        ticket = Ticket(is_winning_ticket, has_been_claimed=True)

        with pytest.raises(TicketAlreadyClaimedError):
            customer.add_ticket(ticket)

    def test_equality_comparison(self):
        """Validates that two instances of the same customer are equal"""
        customer = Customer(
            "firstname",
            "lastname",
            "0000000000",
            "e@e.c",
            Address("city", "state", "country", "0000"),
            "0000",
            Locality(1, 1000, "Bruxelles", Province(1, "Bruxelles")),
        )
        customer_two = customer

        assert customer == customer_two

    def test_equality_comparison_with_another_customer(self):
        """Validates the comparison of a customer with another object"""
        customer = Customer(
            "firstname",
            "lastname",
            "0000000000",
            "e@e.c",
            Address("city", "state", "country", "0000"),
            "0000",
            Locality(1, 1000, "Bruxelles", Province(1, "Bruxelles")),
        )
        customer_two = Customer(
            "firstnametwo",
            "lastnametwo",
            "0000000000",
            "e@e.c",
            Address("city", "state", "country", "0000"),
            "0000",
            Locality(1, 1000, "Bruxelles", Province(1, "Bruxelles")),
        )

        assert customer == customer_two

    def test_inequality_comparison(self):
        """Validates inequality comparison between a customer instance and a string"""
        customer = Customer(
            "firstname",
            "lastname",
            "0000000000",
            "e@e.c",
            Address("city", "state", "country", "0000"),
            "0000",
            Locality(1, 1000, "Bruxelles", Province(1, "Bruxelles")),
        )

        assert customer != "customer"
