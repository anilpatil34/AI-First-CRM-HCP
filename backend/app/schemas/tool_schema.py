"""
Pydantic schemas for Tool execution tracking.
"""

from pydantic import BaseModel, Field
from typing import Any, Optional


class ToolCall(BaseModel):
    """Schema representing a single tool execution."""
    tool_name: str = Field(..., description="Name of the tool executed")
    arguments: dict = Field(default_factory=dict, description="Arguments passed to the tool")
    result: Any = Field(None, description="Tool execution result")


class ToolResult(BaseModel):
    """Schema for tool execution result."""
    success: bool = True
    data: dict = Field(default_factory=dict)
    message: str = ""


class ExtractedInteraction(BaseModel):
    """Schema for structured data extracted from natural language."""
    doctor: Optional[str] = None
    product: Optional[str] = None
    sentiment: Optional[str] = "Neutral"
    topics: list[str] = Field(default_factory=list)
    materials: list[str] = Field(default_factory=list)
    samples: list[str] = Field(default_factory=list)
    summary: Optional[str] = None
    follow_up: Optional[str] = None
    outcomes: Optional[str] = None
    date: Optional[str] = None
    time: Optional[str] = None
    interaction_type: Optional[str] = "Meeting"
    attendees: list[str] = Field(default_factory=list)
