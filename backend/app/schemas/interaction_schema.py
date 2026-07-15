"""
Pydantic schemas for Interaction API endpoints.
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class InteractionCreate(BaseModel):
    """Schema for creating a new interaction."""
    hcp_id: Optional[int] = None
    hcp_name: Optional[str] = Field(None, description="Doctor name for auto-lookup")
    interaction_type: str = Field("Meeting", description="Meeting, Call, Email, Conference, Other")
    date: Optional[str] = None
    time: Optional[str] = None
    attendees: list[str] = Field(default_factory=list)
    topics_discussed: Optional[str] = None
    sentiment: str = Field("Neutral", description="Positive, Neutral, or Negative")
    outcomes: Optional[str] = None
    follow_up_actions: Optional[str] = None
    summary: Optional[str] = None
    ai_generated: bool = False
    materials_shared: list[str] = Field(default_factory=list)
    samples_distributed: list[str] = Field(default_factory=list)


class InteractionUpdate(BaseModel):
    """Schema for updating an interaction. All fields optional."""
    hcp_id: Optional[int] = None
    hcp_name: Optional[str] = None
    interaction_type: Optional[str] = None
    date: Optional[str] = None
    time: Optional[str] = None
    attendees: Optional[list[str]] = None
    topics_discussed: Optional[str] = None
    sentiment: Optional[str] = None
    outcomes: Optional[str] = None
    follow_up_actions: Optional[str] = None
    summary: Optional[str] = None
    ai_generated: Optional[bool] = None
    materials_shared: Optional[list[str]] = None
    samples_distributed: Optional[list[str]] = None


class InteractionResponse(BaseModel):
    """Schema for interaction API responses."""
    id: int
    hcp_id: Optional[int] = None
    interaction_type: str = "Meeting"
    date: Optional[str] = None
    time: Optional[str] = None
    attendees: list[str] = Field(default_factory=list)
    topics_discussed: Optional[str] = None
    sentiment: str = "Neutral"
    outcomes: Optional[str] = None
    follow_up_actions: Optional[str] = None
    summary: Optional[str] = None
    ai_generated: bool = False
    materials_shared: list[str] = Field(default_factory=list)
    samples_distributed: list[str] = Field(default_factory=list)
    doctor_name: Optional[str] = None
    doctor_hospital: Optional[str] = None
    doctor_specialization: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class InteractionList(BaseModel):
    """Schema for paginated interaction list response."""
    items: list[InteractionResponse]
    total: int
    skip: int = 0
    limit: int = 20
