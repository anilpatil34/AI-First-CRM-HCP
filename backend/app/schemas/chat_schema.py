"""
Pydantic schemas for Chat API endpoints.
"""

from pydantic import BaseModel, Field
from typing import Optional
import uuid


class ChatRequest(BaseModel):
    """Schema for incoming chat messages."""
    message: str = Field(..., min_length=1, max_length=5000, description="User message text")
    session_id: Optional[str] = Field(
        default_factory=lambda: str(uuid.uuid4()),
        description="Session ID for conversation continuity"
    )


class ChatResponse(BaseModel):
    """Schema for AI chat responses."""
    response: str = Field(..., description="AI response text")
    extracted_data: Optional[dict] = Field(None, description="Structured data extracted from message")
    tool_calls: list[dict] = Field(default_factory=list, description="Tools executed by the AI")
    suggestions: list[str] = Field(default_factory=list, description="Suggested follow-up actions")
    form_updates: Optional[dict] = Field(None, description="Fields to update in the CRM form")
    session_id: str = Field(..., description="Session ID for this conversation")
