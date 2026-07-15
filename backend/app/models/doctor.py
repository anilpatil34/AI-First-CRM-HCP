"""
Doctor (HCP) SQLAlchemy model.
Represents Healthcare Professional profiles in the CRM.
"""

from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base, TimestampMixin


class Doctor(TimestampMixin, Base):
    """Healthcare Professional (HCP) profile model."""

    __tablename__ = "hcp_profiles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    hospital: Mapped[str | None] = mapped_column(String(300), nullable=True)
    specialization: Mapped[str | None] = mapped_column(String(200), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(20), nullable=True)
    email: Mapped[str | None] = mapped_column(String(200), nullable=True)
    preferred_contact: Mapped[str] = mapped_column(
        String(50), default="In-Person", nullable=False
    )
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Relationships
    interactions = relationship("Interaction", back_populates="doctor", lazy="dynamic")

    def __repr__(self) -> str:
        return f"<Doctor(id={self.id}, name='{self.name}', specialization='{self.specialization}')>"

    def to_dict(self) -> dict:
        """Convert model to dictionary for API responses."""
        return {
            "id": self.id,
            "name": self.name,
            "hospital": self.hospital,
            "specialization": self.specialization,
            "phone": self.phone,
            "email": self.email,
            "preferred_contact": self.preferred_contact,
            "notes": self.notes,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
