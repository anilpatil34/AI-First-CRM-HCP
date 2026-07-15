"""
Sample SQLAlchemy model.
Represents pharmaceutical product samples distributed to HCPs.
"""

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base, TimestampMixin


class Sample(TimestampMixin, Base):
    """Pharmaceutical product sample model."""

    __tablename__ = "samples"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    product: Mapped[str | None] = mapped_column(String(200), nullable=True)
    quantity: Mapped[int] = mapped_column(Integer, default=0)

    def __repr__(self) -> str:
        return f"<Sample(id={self.id}, name='{self.name}', product='{self.product}')>"

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "product": self.product,
            "quantity": self.quantity,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
