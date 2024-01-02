from unittest import mock
from unittest.mock import MagicMock

import pytest

from bwatakado.src.application.use_cases.customer_login import CustomerLogin
from bwatakado.src.domain.entities.customer import Customer
from bwatakado.src.domain.exceptions.customer_not_found_error import (
    CustomerNotFoundError,
)
from bwatakado.src.domain.value_objects.address import Address


class TestCustomerLogin:
    """Customer login use case test cases"""

    @mock.patch(
        "bwatakado.src.application.interfaces.icustomer_repository",
        name="customer_repository_mock",
    )
    def test_customer_login_raises_error_when_customer_does_not_exist(
        self, customer_repository_mock: MagicMock
    ):
        """Test customer login ability"""
        phone_number = "0000000000"
        customer_repository_mock.find_by_phone_number.return_value = None
        usecase = CustomerLogin(customer_repository_mock)

        with pytest.raises(CustomerNotFoundError):
            usecase.execute(phone_number)

        customer_repository_mock.find_by_phone_number.assert_called_once_with(
            phone_number
        )

    @mock.patch(
        "bwatakado.src.application.interfaces.icustomer_repository",
        name="customer_repository_mock",
    )
    def test_customer_login(self, customer_repository_mock: MagicMock):
        """Test customer login ability"""
        phone_number = "0000000000"
        customer_repository_mock.find_by_phone_number.return_value = Customer(
            "firstname",
            "lastname",
            phone_number,
            "e@e.c",
            Address("city", "state", "country", "0000"),
            "0000",
        )
        usecase = CustomerLogin(customer_repository_mock)

        customer = usecase.execute(phone_number)

        customer_repository_mock.find_by_phone_number.assert_called_once_with(
            phone_number
        )
        assert customer.phone_number == phone_number
        assert (
            customer.firstname
            == customer_repository_mock.find_by_phone_number.return_value.firstname
        )
