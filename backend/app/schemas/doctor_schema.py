"""
Pydantic schemas for Doctor/HCP API endpoints.
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class DoctorCreate(BaseModel):
    """Schema for creating a new doctor profile."""
    name: str = Field(..., min_length=1, max_length=200, description="Doctor's full name")
    hospital: Optional[str] = Field(None, max_length=300)
    specialization: Optional[str] = Field(None, max_length=200)
    phone: Optional[str] = Field(None, max_length=20)
    email: Optional[str] = Field(None, max_length=200)
    preferred_contact: str = Field("In-Person", max_length=50)
    notes: Optional[str] = None


class DoctorUpdate(BaseModel):
    """Schema for updating a doctor profile. All fields optional."""
    name: Optional[str] = Field(None, max_length=200)
    hospital: Optional[str] = Field(None, max_length=300)
    specialization: Optional[str] = Field(None, max_length=200)
    phone: Optional[str] = Field(None, max_length=20)
    email: Optional[str] = Field(None, max_length=200)
    preferred_contact: Optional[str] = Field(None, max_length=50)
    notes: Optional[str] = None


class DoctorResponse(BaseModel):
    """Schema for doctor API responses."""
    id: int
    name: str
    hospital: Optional[str] = None
    specialization: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    preferred_contact: str = "In-Person"
    notes: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class DoctorSearch(BaseModel):
    """Schema for doctor search requests."""
    query: str = Field(..., min_length=1, description="Search term")
    limit: int = Field(10, ge=1, le=100)
