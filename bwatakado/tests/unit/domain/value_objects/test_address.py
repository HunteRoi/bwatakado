import pytest

from bwatakado.src.domain.value_objects.address import Address


class TestAddress:
    """Test suite for the value object Address"""

    @pytest.mark.parametrize("street", ["", "1234"])
    def test_create_an_address_should_raise_value_error_when_street_is_invalid(
        self, street: str
    ):
        """Test that a value error is raised when an invalid street is provided"""
        with pytest.raises(ValueError):
            Address(
                "city",
                "state",
                "country",
                "0000",
                street,
                1,
                "complement",
            )

    @pytest.mark.parametrize("number", ["", "abc"])
    def test_create_an_address_should_raise_value_error_when_number_is_invalid(
        self, number: str
    ):
        """Test that a value error is raised when an invalid number is provided"""
        with pytest.raises(ValueError):
            Address(
                "city",
                "state",
                "country",
                "0000",
                "street",
                number,
                "complement",
            )

    @pytest.mark.parametrize("city", ["", None, "1234"])
    def test_create_an_address_should_raise_value_error_when_city_is_invalid(
        self, city: str
    ):
        """Test that a value error is raised when an invalid city is provided"""
        with pytest.raises(ValueError):
            Address(
                city,
                "state",
                "country",
                "0000",
                "street",
                1,
                "complement",
            )

    @pytest.mark.parametrize("state", ["", None, "1234"])
    def test_create_an_address_should_raise_value_error_when_state_is_invalid(
        self, state: str
    ):
        """Test that a value error is raised when an invalid state is provided"""
        with pytest.raises(ValueError):
            Address(
                "city",
                state,
                "country",
                "0000",
                "street",
                1,
                "complement",
            )

    @pytest.mark.parametrize("country", ["", None, "1234"])
    def test_create_an_address_should_raise_value_error_when_country_is_invalid(
        self, country: str
    ):
        """Test that a value error is raised when an invalid country is provided"""
        with pytest.raises(ValueError):
            Address(
                "city",
                "state",
                country,
                "0000",
                "street",
                1,
                "complement",
            )

    @pytest.mark.parametrize("zipcode", ["", None, "abc"])
    def test_create_an_address_should_raise_value_error_when_zipcode_is_invalid(
        self, zipcode: str
    ):
        """Test that a value error is raised when an invalid zipcode is provided"""
        with pytest.raises(ValueError):
            Address(
                "city",
                "state",
                "country",
                zipcode,
                "street",
                1,
                "complement",
            )

    @pytest.mark.parametrize("complement", [""])
    def test_create_an_address_should_raise_value_error_when_complement_is_invalid(
        self, complement: str
    ):
        """Test that a value error is raised when an invalid complement is provided"""
        with pytest.raises(ValueError):
            Address(
                "city",
                "state",
                "country",
                "0000",
                "street",
                1,
                complement,
            )

    @pytest.mark.parametrize(
        "street, number, complement, city, state, country, zipcode",
        [
            ("street", 1, None, "city", "state", "country", "00000"),
            ("street", 1, "complement", "city", "state", "country", "00000"),
        ],
    )
    def test_create_an_address_should_return_an_address_object_when_all_parameters_are_valid(
        self,
        street: str,
        number: int,
        complement: str,
        city: str,
        state: str,
        country: str,
        zipcode: str,
    ):
        """Test that an address object is returned when all parameters are valid"""
        address = Address(
            city,
            state,
            country,
            zipcode,
            street,
            number,
            complement,
        )

        assert address.street == street
        assert address.number == number
        assert address.complement == complement
        assert address.city == city
        assert address.state == state
        assert address.country == country
        assert address.zipcode == zipcode

    @pytest.mark.parametrize(
        "city, state, country, zipcode, street, number, complement",
        [
            ("city", "state", "country", "00000", "street", 1, None),
            ("city", "state", "country", "00000", "street", 1, "complement"),
        ],
    )
    def test_convert_an_address_to_a_string(
        self,
        city: str,
        state: str,
        country: str,
        zipcode: str,
        street: str,
        number: int,
        complement: str,
    ):
        """Test that an address object is returned when all parameters are valid"""
        address = Address(
            city,
            state,
            country,
            zipcode,
            street,
            number,
            complement,
        )

        address_str = address.to_str()
        address_from_str = Address.from_str(address_str)

        assert address == address_from_str

    @pytest.mark.parametrize(
        "address_str",
        [
            "city|state|country|00000|street|1|complement",
            "city|state|country|00000|street|1|",
            "city|state|country|00000|street||",
            "city|state|country|00000|||",
        ],
    )
    def test_convert_back_to_an_address_should_return_the_same_address(
        self, address_str: str
    ):
        """Test that an address object is returned when all parameters are valid"""
        address = Address.from_str(address_str)

        assert address.to_str() == address_str
