"""
Interaction SQLAlchemy model.
Represents HCP interaction logs in the CRM.
"""

import json
from sqlalchemy import Integer, String, Text, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base, TimestampMixin


class Interaction(TimestampMixin, Base):
    """HCP Interaction log model."""

    __tablename__ = "hcp_interactions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    hcp_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("hcp_profiles.id"), nullable=True
    )
    interaction_type: Mapped[str] = mapped_column(
        String(50), default="Meeting", nullable=False
    )
    date: Mapped[str | None] = mapped_column(String(20), nullable=True)
    time: Mapped[str | None] = mapped_column(String(10), nullable=True)
    attendees: Mapped[str | None] = mapped_column(Text, nullable=True)  # JSON string
    topics_discussed: Mapped[str | None] = mapped_column(Text, nullable=True)
    sentiment: Mapped[str] = mapped_column(
        String(20), default="Neutral", nullable=False
    )
    outcomes: Mapped[str | None] = mapped_column(Text, nullable=True)
    follow_up_actions: Mapped[str | None] = mapped_column(Text, nullable=True)
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    ai_generated: Mapped[bool] = mapped_column(Boolean, default=False)
    materials_shared: Mapped[str | None] = mapped_column(Text, nullable=True)  # JSON
    samples_distributed: Mapped[str | None] = mapped_column(Text, nullable=True)  # JSON

    # Relationships
    doctor = relationship("Doctor", back_populates="interactions")

    def __repr__(self) -> str:
        return f"<Interaction(id={self.id}, type='{self.interaction_type}', date='{self.date}')>"

    @property
    def attendees_list(self) -> list[str]:
        """Parse attendees JSON string to list."""
        if not self.attendees:
            return []
        try:
            return json.loads(self.attendees)
        except (json.JSONDecodeError, TypeError):
            return [self.attendees] if self.attendees else []

    @attendees_list.setter
    def attendees_list(self, value: list[str]):
        """Set attendees from list."""
        self.attendees = json.dumps(value) if value else None

    @property
    def materials_list(self) -> list[str]:
        """Parse materials_shared JSON string to list."""
        if not self.materials_shared:
            return []
        try:
            return json.loads(self.materials_shared)
        except (json.JSONDecodeError, TypeError):
            return [self.materials_shared] if self.materials_shared else []

    @property
    def samples_list(self) -> list[str]:
        """Parse samples_distributed JSON string to list."""
        if not self.samples_distributed:
            return []
        try:
            return json.loads(self.samples_distributed)
        except (json.JSONDecodeError, TypeError):
            return [self.samples_distributed] if self.samples_distributed else []

    def to_dict(self) -> dict:
        """Convert model to dictionary for API responses."""
        return {
            "id": self.id,
            "hcp_id": self.hcp_id,
            "interaction_type": self.interaction_type,
            "date": self.date,
            "time": self.time,
            "attendees": self.attendees_list,
            "topics_discussed": self.topics_discussed,
            "sentiment": self.sentiment,
            "outcomes": self.outcomes,
            "follow_up_actions": self.follow_up_actions,
            "summary": self.summary,
            "ai_generated": self.ai_generated,
            "materials_shared": self.materials_list,
            "samples_distributed": self.samples_list,
            "doctor_name": self.doctor.name if self.doctor else None,
            "doctor_hospital": self.doctor.hospital if self.doctor else None,
            "doctor_specialization": self.doctor.specialization if self.doctor else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
