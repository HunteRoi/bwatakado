import pytest
from bwatakado.src.domain.entities.province import Province


class TestProvince:
    """Test suite for the Province entity."""

    def test_province_has_an_identifier(self):
        """Test that a Province has an identifier."""
        province = Province(1, "Province")

        assert province.identifier == 1

    def test_province_has_a_name(self):
        """Test that a Province has a name."""
        province = Province(1, "Province")

        assert province.name == "Province"

    def test_province_cannot_have_no_identifier(self):
        """Test that a Province cannot have an identifier of None."""
        with pytest.raises(ValueError):
            Province(None, "Province")

    def test_province_cannot_have_no_name(self):
        """Test that a Province cannot have a name of None."""
        with pytest.raises(ValueError):
            Province(1, None)
