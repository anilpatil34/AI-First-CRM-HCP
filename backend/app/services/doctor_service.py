"""
Doctor/HCP service layer.
Handles all business logic for doctor profile management.
"""

from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import Optional

from app.models.doctor import Doctor
from app.schemas.doctor_schema import DoctorCreate, DoctorUpdate
from app.utils.logger import get_logger

logger = get_logger(__name__)


def get_doctor_by_id(db: Session, doctor_id: int) -> Optional[Doctor]:
    """Get a doctor by their ID."""
    return db.query(Doctor).filter(Doctor.id == doctor_id).first()


def get_doctor_by_name(db: Session, name: str) -> Optional[Doctor]:
    """
    Get a doctor by name using case-insensitive search.
    Returns the best match.
    """
    # Try exact match first
    doctor = db.query(Doctor).filter(Doctor.name.ilike(name.strip())).first()
    if doctor:
        return doctor

    # Try partial match
    doctor = db.query(Doctor).filter(Doctor.name.ilike(f"%{name.strip()}%")).first()
    return doctor


def get_all_doctors(db: Session, skip: int = 0, limit: int = 100) -> list[Doctor]:
    """Get all doctors with pagination."""
    return db.query(Doctor).order_by(Doctor.name).offset(skip).limit(limit).all()


def create_doctor(db: Session, doctor_data: DoctorCreate) -> Doctor:
    """Create a new doctor profile."""
    doctor = Doctor(
        name=doctor_data.name,
        hospital=doctor_data.hospital,
        specialization=doctor_data.specialization,
        phone=doctor_data.phone,
        email=doctor_data.email,
        preferred_contact=doctor_data.preferred_contact,
        notes=doctor_data.notes,
    )
    db.add(doctor)
    db.commit()
    db.refresh(doctor)
    logger.info(f"Created doctor: {doctor.name} (ID: {doctor.id})")
    return doctor


def update_doctor(db: Session, doctor_id: int, doctor_data: DoctorUpdate) -> Optional[Doctor]:
    """Update an existing doctor profile."""
    doctor = get_doctor_by_id(db, doctor_id)
    if not doctor:
        return None

    update_data = doctor_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(doctor, field, value)

    db.commit()
    db.refresh(doctor)
    logger.info(f"Updated doctor: {doctor.name} (ID: {doctor.id})")
    return doctor


def search_doctors(db: Session, query: str, limit: int = 10) -> list[Doctor]:
    """
    Search doctors by name, hospital, or specialization.
    Uses case-insensitive partial matching.
    """
    search_term = f"%{query.strip()}%"
    return (
        db.query(Doctor)
        .filter(
            or_(
                Doctor.name.ilike(search_term),
                Doctor.hospital.ilike(search_term),
                Doctor.specialization.ilike(search_term),
            )
        )
        .limit(limit)
        .all()
    )


def get_doctor_with_interactions(db: Session, doctor_id: int) -> Optional[dict]:
    """Get doctor profile with their interaction history."""
    doctor = get_doctor_by_id(db, doctor_id)
    if not doctor:
        return None

    interactions = doctor.interactions.order_by(None).all()
    doctor_dict = doctor.to_dict()
    doctor_dict["interactions"] = [i.to_dict() for i in interactions]
    doctor_dict["total_interactions"] = len(interactions)
    return doctor_dict
