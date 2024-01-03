from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from bwatakado.src.domain.entities.province import Province
from bwatakado.src.infrastructure.models.base import Base


class ProvinceModel(Base):
    """Province model."""

    __tablename__ = "province"

    id: Mapped[int] = mapped_column("id", Integer, primary_key=True, nullable=False)
    name: Mapped[str] = mapped_column("name", String, nullable=False)
    localities: Mapped["LocalityModel"] = relationship(
        back_populates="province", lazy="select"
    )

    @classmethod
    def from_province(cls, province: Province) -> "ProvinceModel":
        """Converts a Province entity to a Province model."""

        return cls(
            id=province.identifier,
            name=province.name,
        )

    def to_province(self) -> Province:
        """Convert the model to a Customer entity."""

        return Province(
            identifier=self.id,
            name=self.name,
        )
