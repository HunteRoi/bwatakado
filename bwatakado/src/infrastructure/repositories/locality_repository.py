from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from bwatakado.src.application.interfaces.ilocality_repository import (
    ILocalityRepository,
)
from bwatakado.src.domain.entities.locality import Locality
from bwatakado.src.infrastructure.models.locality_model import LocalityModel


class LocalityRepository(ILocalityRepository):
    """Locality repository implementation."""

    def __init__(
        self, db_path: str = f"{Path.home()}/.bwatakado/bwatakado.sqlite"
    ) -> None:
        self.engine = create_engine(f"sqlite:///{db_path}")

    def insert_data(self):
        """Inserts data into the database."""

        with self.engine.connect() as connection:

            def insert_sql_file(file_path: str):
                with open(file_path) as file:
                    connection.connection.executescript(file.read())

            insert_sql_file("./bwatakado/src/infrastructure/insert_provinces.sql")
            insert_sql_file("./bwatakado/src/infrastructure/insert_localities.sql")

    def get_by_id(self, identifier: int) -> Locality | None:
        with Session(self.engine) as session:
            model: LocalityModel | None = (
                session.query(LocalityModel)
                .where(LocalityModel.id == identifier)
                .first()
            )

            if model is None:
                return None

            return model.to_locality()
