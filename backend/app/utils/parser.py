"""
Response parsing utilities.
Handles JSON extraction from LLM responses and date/time parsing.
"""

import json
import re
from datetime import datetime, timedelta
from typing import Any, Optional


def parse_json_from_llm(text: str) -> Optional[dict]:
    """
    Extract JSON object from LLM text response.
    Handles markdown code blocks, plain JSON, nested objects, and arrays.
    """
    if not text:
        return None

    # Try to find JSON in markdown code blocks
    code_block_pattern = r"```(?:json)?\s*\n?(.*?)\n?\s*```"
    matches = re.findall(code_block_pattern, text, re.DOTALL)
    if matches:
        for match in matches:
            try:
                return json.loads(match.strip())
            except json.JSONDecodeError:
                continue

    # Use bracket counting to extract properly nested JSON
    # Find the first '{' and match until balanced closing '}'
    start_idx = text.find('{')
    while start_idx != -1:
        depth = 0
        in_string = False
        escape_next = False
        for i in range(start_idx, len(text)):
            c = text[i]
            if escape_next:
                escape_next = False
                continue
            if c == '\\' and in_string:
                escape_next = True
                continue
            if c == '"' and not escape_next:
                in_string = not in_string
                continue
            if in_string:
                continue
            if c == '{':
                depth += 1
            elif c == '}':
                depth -= 1
                if depth == 0:
                    candidate = text[start_idx:i + 1]
                    try:
                        return json.loads(candidate)
                    except json.JSONDecodeError:
                        break
        # Try next '{' if this one failed
        start_idx = text.find('{', start_idx + 1)

    # Try the whole text as JSON
    try:
        return json.loads(text.strip())
    except json.JSONDecodeError:
        return None


def parse_date(date_str: str) -> Optional[str]:
    """
    Parse various date formats to YYYY-MM-DD standard format.
    Handles: 'today', 'tomorrow', 'yesterday', 'next Tuesday',
    DD-MM-YYYY, DD/MM/YYYY, YYYY-MM-DD, etc.
    """
    if not date_str:
        return None

    date_str = date_str.strip().lower()
    today = datetime.now()

    # Relative dates
    if date_str == "today":
        return today.strftime("%Y-%m-%d")
    elif date_str == "tomorrow":
        return (today + timedelta(days=1)).strftime("%Y-%m-%d")
    elif date_str == "yesterday":
        return (today - timedelta(days=1)).strftime("%Y-%m-%d")

    # "next <weekday>"
    weekdays = {
        "monday": 0, "tuesday": 1, "wednesday": 2, "thursday": 3,
        "friday": 4, "saturday": 5, "sunday": 6
    }
    next_match = re.match(r"next\s+(\w+)", date_str)
    if next_match:
        day_name = next_match.group(1).lower()
        if day_name in weekdays:
            target = weekdays[day_name]
            current = today.weekday()
            days_ahead = target - current
            if days_ahead <= 0:
                days_ahead += 7
            result = today + timedelta(days=days_ahead)
            return result.strftime("%Y-%m-%d")

    # Standard date formats
    formats = [
        "%Y-%m-%d", "%d-%m-%Y", "%d/%m/%Y", "%m/%d/%Y",
        "%Y/%m/%d", "%d %B %Y", "%d %b %Y", "%B %d, %Y",
        "%b %d, %Y", "%d-%m-%y", "%d/%m/%y",
    ]
    for fmt in formats:
        try:
            parsed = datetime.strptime(date_str, fmt)
            return parsed.strftime("%Y-%m-%d")
        except ValueError:
            continue

    return date_str


def parse_time(time_str: str) -> Optional[str]:
    """Parse various time formats to HH:MM format."""
    if not time_str:
        return None

    time_str = time_str.strip().lower()

    # Handle AM/PM
    formats = ["%I:%M %p", "%I:%M%p", "%H:%M", "%I %p", "%H:%M:%S"]
    for fmt in formats:
        try:
            parsed = datetime.strptime(time_str, fmt)
            return parsed.strftime("%H:%M")
        except ValueError:
            continue

    return time_str


def clean_text(text: str) -> str:
    """Strip and normalize whitespace in text."""
    if not text:
        return ""
    return re.sub(r"\s+", " ", text.strip())


def extract_field_value(text: str, field: str) -> Optional[str]:
    """Extract a specific field value from natural language text."""
    patterns = {
        "doctor": r"(?:dr\.?|doctor)\s+([a-zA-Z\s]+?)(?:\.|,|$|\s+(?:at|in|from))",
        "sentiment": r"(?:sentiment|feeling|mood|response)\s*(?:is|was|to|:)?\s*(positive|negative|neutral)",
        "product": r"(?:discussed|about|regarding|product)\s+([A-Z][a-zA-Z]+(?:\s+\d+\w*)?)",
    }
    if field in patterns:
        match = re.search(patterns[field], text, re.IGNORECASE)
        if match:
            return match.group(1).strip()
    return None
