"""
Response formatting utilities.
Formats data for display, LLM context, and API responses.
"""

from typing import Optional


def format_interaction_for_display(interaction: dict) -> str:
    """Format interaction dictionary for human-readable display."""
    lines = []
    lines.append(f"📋 Interaction #{interaction.get('id', 'N/A')}")
    lines.append(f"   Type: {interaction.get('interaction_type', 'N/A')}")
    lines.append(f"   Date: {interaction.get('date', 'N/A')} at {interaction.get('time', 'N/A')}")

    if interaction.get("doctor_name"):
        lines.append(f"   Doctor: {interaction['doctor_name']}")
        if interaction.get("doctor_hospital"):
            lines.append(f"   Hospital: {interaction['doctor_hospital']}")

    if interaction.get("topics_discussed"):
        lines.append(f"   Topics: {interaction['topics_discussed']}")

    lines.append(f"   Sentiment: {interaction.get('sentiment', 'N/A')}")

    if interaction.get("outcomes"):
        lines.append(f"   Outcomes: {interaction['outcomes']}")

    if interaction.get("follow_up_actions"):
        lines.append(f"   Follow-up: {interaction['follow_up_actions']}")

    materials = interaction.get("materials_shared", [])
    if materials:
        lines.append(f"   Materials: {', '.join(materials)}")

    samples = interaction.get("samples_distributed", [])
    if samples:
        lines.append(f"   Samples: {', '.join(samples)}")

    return "\n".join(lines)


def format_doctor_for_display(doctor: dict) -> str:
    """Format doctor dictionary for human-readable display."""
    lines = []
    lines.append(f"👨‍⚕️ {doctor.get('name', 'Unknown')}")
    if doctor.get("hospital"):
        lines.append(f"   🏥 Hospital: {doctor['hospital']}")
    if doctor.get("specialization"):
        lines.append(f"   🔬 Specialization: {doctor['specialization']}")
    if doctor.get("phone"):
        lines.append(f"   📞 Phone: {doctor['phone']}")
    if doctor.get("email"):
        lines.append(f"   📧 Email: {doctor['email']}")
    if doctor.get("preferred_contact"):
        lines.append(f"   💬 Preferred Contact: {doctor['preferred_contact']}")
    if doctor.get("notes"):
        lines.append(f"   📝 Notes: {doctor['notes']}")
    return "\n".join(lines)


def format_interaction_for_llm(interaction: dict) -> str:
    """Format interaction as context text for LLM prompts."""
    parts = []
    if interaction.get("doctor_name"):
        parts.append(f"Doctor: {interaction['doctor_name']}")
    parts.append(f"Type: {interaction.get('interaction_type', 'Meeting')}")
    parts.append(f"Date: {interaction.get('date', 'Not specified')}")
    if interaction.get("topics_discussed"):
        parts.append(f"Topics: {interaction['topics_discussed']}")
    parts.append(f"Sentiment: {interaction.get('sentiment', 'Neutral')}")
    if interaction.get("outcomes"):
        parts.append(f"Outcomes: {interaction['outcomes']}")
    if interaction.get("materials_shared"):
        materials = interaction["materials_shared"]
        if isinstance(materials, list):
            parts.append(f"Materials Shared: {', '.join(materials)}")
        else:
            parts.append(f"Materials Shared: {materials}")
    if interaction.get("samples_distributed"):
        samples = interaction["samples_distributed"]
        if isinstance(samples, list):
            parts.append(f"Samples Given: {', '.join(samples)}")
        else:
            parts.append(f"Samples Given: {samples}")
    return " | ".join(parts)


def format_suggestions_list(suggestions: list[str]) -> str:
    """Format follow-up suggestions as a bullet list."""
    if not suggestions:
        return "No suggestions available."
    return "\n".join(f"• {suggestion}" for suggestion in suggestions)


def format_error_response(error: str, details: Optional[str] = None) -> dict:
    """Format a standardized error response."""
    response = {"error": error, "success": False}
    if details:
        response["details"] = details
    return response
