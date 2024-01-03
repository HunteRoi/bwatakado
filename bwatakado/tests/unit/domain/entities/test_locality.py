import pytest
from bwatakado.src.domain.entities.locality import Locality
from bwatakado.src.domain.entities.province import Province


class TestLocality:
    """Test suite for the Locality entity."""

    def test_locality_has_an_identifier(self):
        """Test that a Locality has an identifier."""
        locality = Locality(1, 1000, "Locality", Province(1, "Province"))

        assert locality.identifier == 1

    def test_locality_has_a_postcode(self):
        """Test that a Locality has a postcode."""
        locality = Locality(1, 1000, "Locality", Province(1, "Province"))

        assert locality.postcode == 1000

    def test_locality_has_a_name(self):
        """Test that a Locality has a name."""
        locality = Locality(1, 1000, "Locality", Province(1, "Province"))

        assert locality.name == "Locality"

    def test_locality_has_a_province(self):
        """Test that a Locality has a province."""
        province = Province(1, "Province")

        locality = Locality(1, 1000, "Locality", province)

        assert locality.province == province

    def test_locality_cannot_have_no_identifier(self):
        """Test that a Locality cannot have an identifier of None."""
        with pytest.raises(ValueError):
            Locality(None, 1000, "Locality", Province(1, "Province"))

    def test_locality_cannot_have_no_province(self):
        """Test that a Locality cannot have no province."""
        with pytest.raises(ValueError):
            Locality(1, 1000, "Locality", None)

    def test_locality_cannot_have_no_postcode(self):
        """Test that a Locality cannot have a postcode of None."""
        with pytest.raises(ValueError):
            Locality(1, None, "Locality", Province(1, "Province"))

    @pytest.mark.parametrize("postcode", [1, 20, 300])
    def test_locality_cannot_have_postcode_smaller_than_4_characters(self, postcode):
        """Test that a Locality cannot have a postcode smaller than 4 characters."""
        with pytest.raises(ValueError):
            Locality(1, postcode, "Locality", Province(1, "Province"))

    def test_locality_cannot_have_no_name(self):
        """Test that a Locality cannot have a name of None."""
        with pytest.raises(ValueError):
            Locality(1, 1000, None, Province(1, "Province"))

    def test_locality_cannot_have_empty_name(self):
        """Test that a Locality cannot have an empty name."""
        with pytest.raises(ValueError):
            Locality(1, 1000, "", Province(1, "Province"))
