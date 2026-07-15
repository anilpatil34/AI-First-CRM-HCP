"""
Prompt template service.
Loads and formats prompt templates from the prompts directory.
"""

import os
from typing import Optional
from app.utils.logger import get_logger

logger = get_logger(__name__)

# Path to prompts directory
PROMPTS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "prompts")


def load_prompt(prompt_name: str) -> str:
    """
    Load a prompt template from file.
    
    Args:
        prompt_name: Name of the prompt file (without .txt extension)
    
    Returns:
        Prompt text content
    """
    file_path = os.path.join(PROMPTS_DIR, f"{prompt_name}.txt")
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read().strip()
    except FileNotFoundError:
        logger.warning(f"Prompt file not found: {file_path}")
        return ""


def format_prompt(template: str, **kwargs) -> str:
    """
    Format a prompt template with variable substitution.
    Uses {variable} syntax for placeholders.
    """
    try:
        return template.format(**kwargs)
    except KeyError as e:
        logger.warning(f"Missing template variable: {e}")
        return template


def get_system_prompt() -> str:
    """Load and return the system prompt for the AI assistant."""
    return load_prompt("system_prompt")


def get_extraction_prompt(user_message: str) -> str:
    """Load extraction prompt and inject the user message."""
    template = load_prompt("extraction_prompt")
    if not template:
        return f"Extract structured data from this message:\n\n{user_message}"
    return format_prompt(template, user_message=user_message)


def get_followup_prompt(interaction_context: str) -> str:
    """Load follow-up suggestion prompt with interaction context."""
    template = load_prompt("followup_prompt")
    if not template:
        return f"Suggest follow-up actions for this interaction:\n\n{interaction_context}"
    return format_prompt(template, interaction_context=interaction_context)
