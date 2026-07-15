"""
Tool 2: Edit Interaction
Updates specific fields of an existing interaction via natural language.
"""

from app.services.groq_service import get_groq_service
from app.utils.parser import parse_json_from_llm, parse_date, parse_time
from app.utils.logger import get_logger

logger = get_logger(__name__)

EDITABLE_FIELDS = [
    "sentiment", "interaction_type", "date", "time", "topics_discussed",
    "outcomes", "follow_up_actions", "summary", "doctor", "hcp_name",
    "materials_shared", "samples_distributed", "attendees",
]


def edit_interaction(user_message: str, current_data: dict = None) -> dict:
    """
    Parse an edit request and return the field(s) to update.
    
    Input example:
        "Change sentiment to Negative"
    
    Output:
        {
            "field": "sentiment",
            "value": "Negative",
            "updates": {"sentiment": "Negative"}
        }
    """
    groq = get_groq_service()

    current_context = ""
    if current_data:
        current_context = f"\n\nCurrent interaction data:\n{_format_current_data(current_data)}"

    messages = [
        {
            "role": "system",
            "content": (
                "You are a CRM field editor. The user wants to modify an interaction record. "
                "Identify which field(s) to update and the new value(s). "
                f"Editable fields: {', '.join(EDITABLE_FIELDS)}\n"
                "Return a JSON object with:\n"
                '- "field": the field name to update (string)\n'
                '- "value": the new value (string or array)\n'
                '- "updates": object mapping field names to new values\n'
                "Return ONLY the JSON object."
            ),
        },
        {
            "role": "user",
            "content": f"Edit request: {user_message}{current_context}",
        },
    ]

    response = groq.invoke(messages)
    result = parse_json_from_llm(response)

    if result:
        # Normalize fields in updates dict
        updates = result.get("updates", {})
        if not updates and "field" in result:
            updates = {result["field"]: result.get("value")}
            result["updates"] = updates

        if "date" in updates and updates["date"]:
            updates["date"] = parse_date(updates["date"]) or updates["date"]
            if result.get("field") == "date":
                result["value"] = updates["date"]

        if "time" in updates and updates["time"]:
            updates["time"] = parse_time(updates["time"]) or updates["time"]
            if result.get("field") == "time":
                result["value"] = updates["time"]

        logger.info(f"Edit parsed: {result.get('field')} -> {result.get('value')}")
        return result

    # Fallback: try simple parsing
    fallback_result = _simple_parse_edit(user_message)
    updates = fallback_result.get("updates", {})
    if "date" in updates and updates["date"]:
        updates["date"] = parse_date(updates["date"]) or updates["date"]
    if "time" in updates and updates["time"]:
        updates["time"] = parse_time(updates["time"]) or updates["time"]
    return fallback_result


def _format_current_data(data: dict) -> str:
    """Format current interaction data for context."""
    lines = []
    for key, value in data.items():
        if value and key not in ("id", "created_at", "updated_at"):
            lines.append(f"  {key}: {value}")
    return "\n".join(lines)


def _simple_parse_edit(message: str) -> dict:
    """Simple fallback parsing for common edit patterns."""
    message_lower = message.lower()

    # Sentiment changes
    for sentiment in ["positive", "neutral", "negative"]:
        if sentiment in message_lower and ("sentiment" in message_lower or "change" in message_lower or "set" in message_lower):
            return {
                "field": "sentiment",
                "value": sentiment.capitalize(),
                "updates": {"sentiment": sentiment.capitalize()},
            }

    # Type changes
    for itype in ["meeting", "call", "email", "conference"]:
        if itype in message_lower and ("type" in message_lower or "change" in message_lower):
            return {
                "field": "interaction_type",
                "value": itype.capitalize(),
                "updates": {"interaction_type": itype.capitalize()},
            }

    return {"field": "unknown", "value": message, "updates": {}}
