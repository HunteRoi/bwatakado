import pytest

from bwatakado.src.application.interfaces.ilocality_repository import (
    ILocalityRepository,
)
from bwatakado.src.infrastructure.models.base import Base
from bwatakado.src.infrastructure.repositories.locality_repository import (
    LocalityRepository,
)


class TestLocalityRepository:
    """LocalityRepository test cases."""

    @pytest.fixture(autouse=True, name="repository")
    def generate_repository(self) -> ILocalityRepository:
        """Initialize the repository."""

        repository: ILocalityRepository = LocalityRepository(":memory:")
        Base().metadata.create_all(repository.engine)
        repository.insert_data()

        return repository

    def test_get_locality_by_identifier(self, repository: ILocalityRepository):
        """Test that a locality is returned when there's a match on the identifier."""
        locality = repository.get_by_id(1)

        assert locality.postcode == 1000
        assert locality.name == "Bruxelles"

    def test_get_locality_by_identifier_returns_none_when_not_existing(
        self, repository: ILocalityRepository
    ):
        """Test that a locality is not returned when the identifier does not match."""

        locality = repository.get_by_id(180000)

        assert locality is None
