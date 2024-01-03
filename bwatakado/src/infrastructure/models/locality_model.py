from typing import List
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from bwatakado.src.domain.entities.locality import Locality
from bwatakado.src.infrastructure.models.base import Base
from bwatakado.src.infrastructure.models.province_model import ProvinceModel


class LocalityModel(Base):
    """Locality model."""

    __tablename__ = "locality"

    id: Mapped[int] = mapped_column("id", Integer, primary_key=True, nullable=False)
    province_id: Mapped[int] = mapped_column(ForeignKey("province.id"), nullable=False)
    province: Mapped[ProvinceModel] = relationship(back_populates="localities")
    postcode: Mapped[int] = mapped_column("postcode", Integer, nullable=False)
    name: Mapped[str] = mapped_column("name", String, nullable=False)
    customers: Mapped[List["CustomerModel"]] = relationship(
        back_populates="locality", lazy="select"
    )

    @classmethod
    def from_locality(cls, locality: Locality) -> "LocalityModel":
        """Converts a Locality entity to a Locality model."""

        return cls(
            id=locality.identifier,
            postcode=locality.postcode,
            name=locality.name,
            province_id=locality.province.identifier,
            province=ProvinceModel.from_province(locality.province),
        )

    def to_locality(self) -> Locality:
        """Convert the model to a Customer entity."""

        return Locality(
            identifier=self.id,
            postcode=self.postcode,
            name=self.name,
            province=self.province.to_province(),
        )
