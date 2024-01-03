from unittest import mock
from unittest.mock import MagicMock

import pytest

from bwatakado.src.application.use_cases.create_account.account_data import AccountData
from bwatakado.src.application.use_cases.create_account.create_account import (
    CreateAccount,
)
from bwatakado.src.domain.entities.locality import Locality
from bwatakado.src.domain.entities.province import Province
from bwatakado.src.domain.value_objects.address import Address


class TestCreateAccount:
    """Test suite to validate an account creation"""

    @pytest.fixture(scope="function", autouse=True, name="usecase")
    @mock.patch(
        "bwatakado.src.application.interfaces.ilocality_repository",
        name="locality_repo_mock",
    )
    @mock.patch(
        "bwatakado.src.application.interfaces.icustomer_repository",
        name="customer_repo_mock",
    )
    def create_usecase(
        self, customer_repo_mock: MagicMock, locality_repo_mock: MagicMock
    ):
        """Create a use case instance"""
        locality_repo_mock.get_by_id.return_value = Locality(
            1, 1000, "Bruxelles", Province(1, "Bruxelles")
        )
        return CreateAccount(customer_repo_mock, locality_repo_mock)

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
            1,
        )

    @pytest.mark.parametrize(
        "data",
        [
            AccountData(
                "",
                "lastname",
                "0000000000",
                "e@e.c",
                Address("city", "state", "country", "0000"),
                "0000",
                1,
            ),
            AccountData(
                None,
                "lastname",
                "0000000000",
                "e@e.c",
                Address("city", "state", "country", "0000"),
                "0000",
                1,
            ),
            AccountData(
                "1234",
                "lastname",
                "0000000000",
                "e@e.c",
                Address("city", "state", "country", "0000"),
                "0000",
                1,
            ),
            AccountData(
                "firstname",
                "",
                "0000000000",
                "e@e.c",
                Address("city", "state", "country", "0000"),
                "0000",
                1,
            ),
            AccountData(
                "firstname",
                None,
                "0000000000",
                "e@e.c",
                Address("city", "state", "country", "0000"),
                "0000",
                1,
            ),
            AccountData(
                "firstname",
                "1234",
                "0000000000",
                "e@e.c",
                Address("city", "state", "country", "0000"),
                "0000",
                1,
            ),
            AccountData(
                "firstname",
                "lastname",
                "",
                "e@e.c",
                Address("city", "state", "country", "0000"),
                "0000",
                1,
            ),
            AccountData(
                "firstname",
                "lastname",
                None,
                "e@e.c",
                Address("city", "state", "country", "0000"),
                "0000",
                1,
            ),
            AccountData(
                "firstname",
                "lastname",
                "0000000000",
                "email",
                Address("city", "state", "country", "0000"),
                "0000",
                1,
            ),
            AccountData(
                "firstname",
                "lastname",
                "0000000000",
                "",
                Address("city", "state", "country", "0000"),
                "0000",
                1,
            ),
            AccountData(
                "firstname",
                "lastname",
                "0000000000",
                None,
                Address("city", "state", "country", "0000"),
                "0000",
                1,
            ),
            AccountData(
                "firstname",
                "lastname",
                "0000000000",
                "abc",
                Address("city", "state", "country", "0000"),
                "0000",
                1,
            ),
            AccountData(
                "firstname",
                "lastname",
                "0000000000",
                "abc@com",
                Address("city", "state", "country", "0000"),
                "0000",
                1,
            ),
            AccountData(
                "firstname",
                "lastname",
                "0000000000",
                "e@e.c",
                Address("city", "state", "country", "0000"),
                None,
                1,
            ),
            AccountData(
                "firstname",
                "lastname",
                "0000000000",
                "e@e.c",
                Address("city", "state", "country", "0000"),
                "abc",
                1,
            ),
            AccountData(
                "firstname",
                "lastname",
                "0000000000",
                "e@e.c",
                None,
                "0000",
                1,
            ),
            AccountData(
                "firstname",
                "lastname",
                "0000000000",
                "e@e.c",
                "",
                "0000",
                1,
            ),
            AccountData(
                "firstname",
                "lastname",
                "0000000000",
                "e@e.c",
                Address("city", "state", "country", "0000"),
                "0000",
                -1,
            ),
            AccountData(
                "firstname",
                "lastname",
                "0000000000",
                "e@e.c",
                Address("city", "state", "country", "0000"),
                "0000",
                "",
            ),
            AccountData(
                "firstname",
                "lastname",
                "0000000000",
                "e@e.c",
                Address("city", "state", "country", "0000"),
                "0000",
                None,
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
        usecase.customer_repository.create_or_update_customer.return_value = data
        customer = usecase.execute(data)

        assert customer.firstname == data.firstname
        assert customer.lastname == data.lastname
        assert customer.phone_number == data.phone_number
        assert customer.email == data.email
        assert customer.address == data.address
        assert customer.pin_code == data.pin_code

    def test_create_account_saves_customer(
        self, usecase: CreateAccount, data: AccountData
    ):
        """Validates that the account data is saved as a customer into the repository"""
        usecase.execute(data)

        usecase.locality_repository.get_by_id.assert_called_once()
        usecase.customer_repository.create_or_update_customer.assert_called_once()

    def test_create_account_raises_error_when_locality_does_not_exist(
        self, usecase: CreateAccount, data: AccountData
    ):
        """Test that an error is raised when the locality does not exist"""
        usecase.locality_repository.get_by_id.return_value = None

        with pytest.raises(ValueError):
            usecase.execute(data)
