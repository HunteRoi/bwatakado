from sqlalchemy import create_engine, delete
from sqlalchemy.orm import Session

from bwatakado.src.application.interfaces.iprize_repository import IPrizeRepository
from bwatakado.src.domain.entities.prize import Prize
from bwatakado.src.infrastructure.models.prize_model import PrizeModel


class PrizeRepository(IPrizeRepository):
    """Prize SQLite repository that provides prize CRUD functionalities."""

    def __init__(self, db_path: str = "~/.bwatakado/bwatakado.sqlite") -> None:
        self.engine = create_engine(f"sqlite:///{db_path}")

    def create_prize(self, prize: Prize) -> Prize:
        with Session(self.engine) as session:
            model = PrizeModel.from_prize(prize)
            session.add(model)
            session.commit()

            return model.to_prize()

    def get_prize(self, prize_id: int) -> Prize | None:
        with Session(self.engine) as session:
            model: PrizeModel | None = session.get(PrizeModel, prize_id)

            if model is None:
                return None

            return model.to_prize()

    def update_prize(self, prize: Prize) -> Prize:
        with Session(self.engine) as session:
            model = PrizeModel.from_prize(prize)
            session.merge(model)
            session.commit()

            return model.to_prize()

    def delete_prize(self, prize_id: int) -> None:
        with Session(self.engine) as session:
            session.execute(delete(PrizeModel).where(PrizeModel.id == prize_id))
            session.commit()
