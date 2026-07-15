"""
Interaction service layer.
Handles all business logic for HCP interaction management.
"""

import json
from sqlalchemy.orm import Session, joinedload
from typing import Optional

from app.models.interaction import Interaction
from app.models.doctor import Doctor
from app.schemas.interaction_schema import InteractionCreate, InteractionUpdate
from app.services.doctor_service import get_doctor_by_name
from app.utils.logger import get_logger

logger = get_logger(__name__)


def create_interaction(db: Session, data: InteractionCreate) -> Interaction:
    """Create a new interaction record."""
    # Auto-lookup doctor by name if hcp_id not provided
    hcp_id = data.hcp_id
    if not hcp_id and data.hcp_name:
        doctor = get_doctor_by_name(db, data.hcp_name)
        if doctor:
            hcp_id = doctor.id
            logger.info(f"Auto-matched doctor: {data.hcp_name} -> ID {hcp_id}")

    interaction = Interaction(
        hcp_id=hcp_id,
        interaction_type=data.interaction_type,
        date=data.date,
        time=data.time,
        attendees=json.dumps(data.attendees) if data.attendees else None,
        topics_discussed=data.topics_discussed,
        sentiment=data.sentiment,
        outcomes=data.outcomes,
        follow_up_actions=data.follow_up_actions,
        summary=data.summary,
        ai_generated=data.ai_generated,
        materials_shared=json.dumps(data.materials_shared) if data.materials_shared else None,
        samples_distributed=json.dumps(data.samples_distributed) if data.samples_distributed else None,
    )
    db.add(interaction)
    db.commit()
    db.refresh(interaction)
    logger.info(f"Created interaction #{interaction.id} (type: {interaction.interaction_type})")
    return interaction


def get_interaction_by_id(db: Session, interaction_id: int) -> Optional[Interaction]:
    """Get an interaction by ID with doctor info loaded."""
    return (
        db.query(Interaction)
        .options(joinedload(Interaction.doctor))
        .filter(Interaction.id == interaction_id)
        .first()
    )


def get_all_interactions(
    db: Session, skip: int = 0, limit: int = 20
) -> tuple[list[Interaction], int]:
    """Get all interactions with pagination. Returns (items, total_count)."""
    query = db.query(Interaction).options(joinedload(Interaction.doctor))
    total = query.count()
    items = query.order_by(Interaction.created_at.desc()).offset(skip).limit(limit).all()
    return items, total


def update_interaction(
    db: Session, interaction_id: int, data: InteractionUpdate
) -> Optional[Interaction]:
    """Update an existing interaction."""
    interaction = get_interaction_by_id(db, interaction_id)
    if not interaction:
        return None

    update_data = data.model_dump(exclude_unset=True)

    # Handle doctor name lookup
    if "hcp_name" in update_data and update_data["hcp_name"]:
        doctor = get_doctor_by_name(db, update_data["hcp_name"])
        if doctor:
            interaction.hcp_id = doctor.id
        del update_data["hcp_name"]

    # Handle list fields (serialize to JSON)
    list_fields = ["attendees", "materials_shared", "samples_distributed"]
    for field in list_fields:
        if field in update_data and update_data[field] is not None:
            update_data[field] = json.dumps(update_data[field])

    for field, value in update_data.items():
        if hasattr(interaction, field):
            setattr(interaction, field, value)

    db.commit()
    db.refresh(interaction)
    logger.info(f"Updated interaction #{interaction.id}")
    return interaction


def delete_interaction(db: Session, interaction_id: int) -> bool:
    """Delete an interaction by ID."""
    interaction = db.query(Interaction).filter(Interaction.id == interaction_id).first()
    if not interaction:
        return False
    db.delete(interaction)
    db.commit()
    logger.info(f"Deleted interaction #{interaction_id}")
    return True


def get_interactions_by_doctor(db: Session, doctor_name: str) -> list[Interaction]:
    """Get all interactions for a specific doctor by name."""
    doctor = get_doctor_by_name(db, doctor_name)
    if not doctor:
        return []
    return (
        db.query(Interaction)
        .options(joinedload(Interaction.doctor))
        .filter(Interaction.hcp_id == doctor.id)
        .order_by(Interaction.created_at.desc())
        .all()
    )


def get_latest_interaction(db: Session) -> Optional[Interaction]:
    """Get the most recent interaction."""
    return (
        db.query(Interaction)
        .options(joinedload(Interaction.doctor))
        .order_by(Interaction.created_at.desc())
        .first()
    )
