from unittest import mock
from unittest.mock import MagicMock

import pytest

from bwatakado.src.application.use_cases.create_account.account_data import AccountData
from bwatakado.src.application.use_cases.create_account.create_account import (
    CreateAccount,
)
from bwatakado.src.domain.value_objects.address import Address


class TestCreateAccount:
    """Test suite to validate an account creation"""

    @pytest.fixture(scope="function", autouse=True, name="usecase")
    @mock.patch(
        "bwatakado.src.application.interfaces.icustomer_repository",
        name="customer_repository",
    )
    def create_usecase(self, customer_repository: MagicMock):
        """Create a use case instance"""
        return CreateAccount(customer_repository)

    @pytest.fixture(scope="function", autouse=True, name="data")
    def create_account_data(self):
        """Create an account data instance"""

        return AccountData(
            "Firstname",
            "Lastname",
            "0471111111",
            "email@email_example.com",
            Address("city", "state", "country", "0000"),
            "1234",
        )

    @pytest.mark.parametrize(
        "data",
        [
            AccountData(
                "",
                "lastname",
                "phone_number",
                "email",
                Address("city", "state", "country", "0000"),
                "pin_code",
            ),
            AccountData(
                None,
                "lastname",
                "phone_number",
                "email",
                Address("city", "state", "country", "0000"),
                "pin_code",
            ),
            AccountData(
                "1234",
                "lastname",
                "phone_number",
                "email",
                Address("city", "state", "country", "0000"),
                "pin_code",
            ),
            AccountData(
                "firstname",
                "",
                "phone_number",
                "email",
                Address("city", "state", "country", "0000"),
                "pin_code",
            ),
            AccountData(
                "firstname",
                None,
                "phone_number",
                "email",
                Address("city", "state", "country", "0000"),
                "pin_code",
            ),
            AccountData(
                "firstname",
                "1234",
                "phone_number",
                "email",
                Address("city", "state", "country", "0000"),
                "pin_code",
            ),
            AccountData(
                "firstname",
                "lastname",
                "",
                "email",
                Address("city", "state", "country", "0000"),
                "pin_code",
            ),
            AccountData(
                "firstname",
                "lastname",
                None,
                "email",
                Address("city", "state", "country", "0000"),
                "pin_code",
            ),
            AccountData(
                "firstname",
                "lastname",
                "abc",
                "email",
                Address("city", "state", "country", "0000"),
                "pin_code",
            ),
            AccountData(
                "firstname",
                "lastname",
                "phone_number",
                "",
                Address("city", "state", "country", "0000"),
                "pin_code",
            ),
            AccountData(
                "firstname",
                "lastname",
                "phone_number",
                None,
                Address("city", "state", "country", "0000"),
                "pin_code",
            ),
            AccountData(
                "firstname",
                "lastname",
                "phone_number",
                "abc",
                Address("city", "state", "country", "0000"),
                "pin_code",
            ),
            AccountData(
                "firstname",
                "lastname",
                "phone_number",
                "abc@com",
                Address("city", "state", "country", "0000"),
                "pin_code",
            ),
            AccountData(
                "firstname",
                "lastname",
                "phone_number",
                "email",
                Address("city", "state", "country", "0000"),
                None,
            ),
            AccountData(
                "firstname",
                "lastname",
                "phone_number",
                "email",
                Address("city", "state", "country", "0000"),
                "abc",
            ),
        ],
    )
    def test_create_account_raises_error_when_invalid_data(
        self, usecase: CreateAccount, data: AccountData
    ):
        """Test that an error is raised when invalid data is provided"""
        with pytest.raises(ValueError):
            usecase.execute(data)

    def test_create_account_returns_account_data_when_valid_data(
        self, usecase: CreateAccount, data: AccountData
    ):
        """Test that an account data is returned when valid data is provided"""
        usecase.customer_repository.create_customer.return_value = data
        account_data = usecase.execute(data)

        assert account_data.firstname == data.firstname
        assert account_data.lastname == data.lastname
        assert account_data.phone_number == data.phone_number
        assert account_data.email == data.email
        assert account_data.address == data.address
        assert account_data.pin_code == data.pin_code

    def test_create_account_saves_customer(
        self, usecase: CreateAccount, data: AccountData
    ):
        """Validates that the account data is saved as a customer into the repository"""
        usecase.execute(data)

        usecase.customer_repository.create_customer.assert_called_once()
