"""
HCP/Doctor API endpoints.
Provides CRUD operations and search for doctor profiles.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.doctor_schema import DoctorCreate, DoctorUpdate, DoctorResponse
from app.services import doctor_service

router = APIRouter()


@router.get("/doctors", tags=["HCP"], response_model=list[DoctorResponse])
def list_doctors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all doctors with pagination."""
    doctors = doctor_service.get_all_doctors(db, skip=skip, limit=limit)
    return [DoctorResponse.model_validate(d) for d in doctors]


@router.get("/doctor/{doctor_id}", tags=["HCP"], response_model=DoctorResponse)
def get_doctor(doctor_id: int, db: Session = Depends(get_db)):
    """Get a specific doctor by ID."""
    doctor = doctor_service.get_doctor_by_id(db, doctor_id)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return DoctorResponse.model_validate(doctor)


@router.get("/doctor/search/{query}", tags=["HCP"], response_model=list[DoctorResponse])
def search_doctors(query: str, limit: int = 10, db: Session = Depends(get_db)):
    """Search doctors by name, hospital, or specialization."""
    doctors = doctor_service.search_doctors(db, query=query, limit=limit)
    return [DoctorResponse.model_validate(d) for d in doctors]


@router.get("/doctor/{doctor_id}/profile", tags=["HCP"])
def get_doctor_profile(doctor_id: int, db: Session = Depends(get_db)):
    """Get doctor profile with interaction history."""
    profile = doctor_service.get_doctor_with_interactions(db, doctor_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return profile


@router.post("/doctor", tags=["HCP"], response_model=DoctorResponse, status_code=201)
def create_doctor(doctor_data: DoctorCreate, db: Session = Depends(get_db)):
    """Create a new doctor profile."""
    doctor = doctor_service.create_doctor(db, doctor_data)
    return DoctorResponse.model_validate(doctor)


@router.put("/doctor/{doctor_id}", tags=["HCP"], response_model=DoctorResponse)
def update_doctor(doctor_id: int, doctor_data: DoctorUpdate, db: Session = Depends(get_db)):
    """Update an existing doctor profile."""
    doctor = doctor_service.update_doctor(db, doctor_id, doctor_data)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return DoctorResponse.model_validate(doctor)
