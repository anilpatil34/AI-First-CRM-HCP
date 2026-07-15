"""
Input validation utilities.
Validates interaction data, sentiment values, and contact information.
"""

import re
from typing import Optional


VALID_SENTIMENTS = {"Positive", "Neutral", "Negative"}
VALID_INTERACTION_TYPES = {"Meeting", "Call", "Email", "Conference", "Other"}


def validate_sentiment(value: str) -> Optional[str]:
    """Validate sentiment value. Returns normalized value or None if invalid."""
    if not value:
        return "Neutral"
    normalized = value.strip().capitalize()
    return normalized if normalized in VALID_SENTIMENTS else None


def validate_interaction_type(value: str) -> Optional[str]:
    """Validate interaction type. Returns normalized value or None if invalid."""
    if not value:
        return "Meeting"
    normalized = value.strip().capitalize()
    return normalized if normalized in VALID_INTERACTION_TYPES else None


def validate_email(value: str) -> bool:
    """Basic email format validation."""
    if not value:
        return True  # Email is optional
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, value.strip()))


def validate_phone(value: str) -> bool:
    """Basic phone number validation."""
    if not value:
        return True  # Phone is optional
    cleaned = re.sub(r"[\s\-\(\)\+]", "", value)
    return len(cleaned) >= 7 and cleaned.isdigit()


def validate_required(value: str, field_name: str) -> Optional[str]:
    """Check if required field is not empty. Returns error message or None."""
    if not value or not value.strip():
        return f"{field_name} is required"
    return None


def validate_date_format(value: str) -> bool:
    """Validate date is in YYYY-MM-DD format."""
    if not value:
        return True
    pattern = r"^\d{4}-\d{2}-\d{2}$"
    return bool(re.match(pattern, value.strip()))


def validate_interaction_data(data: dict) -> dict:
    """
    Validate complete interaction data.
    Returns dict with 'is_valid' and 'errors' keys.
    """
    errors = {}

    # Validate sentiment
    if "sentiment" in data and data["sentiment"]:
        if validate_sentiment(data["sentiment"]) is None:
            errors["sentiment"] = f"Invalid sentiment. Must be one of: {', '.join(VALID_SENTIMENTS)}"

    # Validate interaction type
    if "interaction_type" in data and data["interaction_type"]:
        if validate_interaction_type(data["interaction_type"]) is None:
            errors["interaction_type"] = f"Invalid type. Must be one of: {', '.join(VALID_INTERACTION_TYPES)}"

    # Validate date
    if "date" in data and data["date"]:
        if not validate_date_format(data["date"]):
            errors["date"] = "Date must be in YYYY-MM-DD format"

    return {"is_valid": len(errors) == 0, "errors": errors}
