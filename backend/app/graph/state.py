"""
LangGraph conversation state schema.
Defines the state that flows through the graph nodes.
"""

from typing import TypedDict, Optional, Any
from sqlalchemy.orm import Session


class AgentState(TypedDict):
    """State that flows through the LangGraph workflow."""
    
    # Input
    messages: list[dict]           # Conversation history
    user_message: str              # Current user message
    session_id: str                # Session identifier
    db: Any                        # Database session (Any to avoid TypedDict issues)
    
    # Processing
    intent: Optional[str]          # Detected intent: log, edit, summarize, followup, lookup, general
    extracted_data: Optional[dict] # Structured data extracted from message
    selected_tool: Optional[str]   # Tool to execute
    tool_result: Optional[dict]    # Result from tool execution
    
    # Output
    form_updates: Optional[dict]   # Fields to update in the CRM form
    tool_calls: list[dict]         # List of tools that were called
    suggestions: list[str]         # Follow-up suggestions
    response: str                  # Final AI response text
