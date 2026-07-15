"""
Tool registry.
Provides access to all available LangGraph tools.
"""

from app.tools.log_interaction import log_interaction
from app.tools.edit_interaction import edit_interaction
from app.tools.summarize_interaction import summarize_interaction
from app.tools.suggest_followup import suggest_followup
from app.tools.doctor_lookup import doctor_lookup

TOOLS = {
    "log_interaction": log_interaction,
    "edit_interaction": edit_interaction,
    "summarize_interaction": summarize_interaction,
    "suggest_followup": suggest_followup,
    "doctor_lookup": doctor_lookup,
}


def get_tool(name: str):
    """Get a tool function by name."""
    return TOOLS.get(name)


def get_tool_names() -> list[str]:
    """Get list of all available tool names."""
    return list(TOOLS.keys())


def get_tools() -> dict:
    """Get all tools as a dictionary."""
    return TOOLS
