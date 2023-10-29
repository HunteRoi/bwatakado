from unittest import mock

import pytest

from bwatakado.src.infrastructure.services.bcrypt_password_service import BCryptPasswordService


class TestBCryptPasswordService:
    """BCryptPasswordService test cases."""

    @pytest.mark.parametrize('password, hashed_password', [
        ('password', 'hashed_password'),
        ('other_password', 'hashed_other_password'),
        ('thisisanotherpassword', 'hashed_thisisanotherpassword'),
    ])
    @mock.patch('bcrypt.hashpw')
    def test_hash_password(self, bcrypt_hashpw_mock, password, hashed_password):
        """Ensure that the password is hashed correctly."""

        bcrypt_hashpw_mock.return_value = hashed_password
        service = BCryptPasswordService(b'salt')

        actual = service.hash(password)

        assert actual == hashed_password

    def test_init(self):
        """Ensure that the BCryptPasswordService instance is initialized correctly."""
        service = BCryptPasswordService(salt=b'salt')

        assert service.salt == b'salt'

    @mock.patch('bcrypt.checkpw')
    def test_compare_passwords(self, bcrypt_checkpw_mock):
        """Ensure that the passwords are compared correctly."""
        bcrypt_checkpw_mock.return_value = True
        service = BCryptPasswordService(salt=b'salt')

        passwords_match = service.compare('password', 'hashed_password')

        assert passwords_match
