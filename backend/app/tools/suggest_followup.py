"""
Tool 4: Suggest Follow-up
Generates intelligent follow-up action suggestions based on interaction context.
"""

from app.services.groq_service import get_groq_service
from app.services.prompt_service import get_followup_prompt
from app.utils.formatter import format_interaction_for_llm
from app.utils.parser import parse_json_from_llm
from app.utils.logger import get_logger

logger = get_logger(__name__)


def suggest_followup(interaction_data: dict) -> list[str]:
    """
    Generate contextual follow-up action suggestions.
    
    Output examples:
        - "Schedule follow-up meeting in 2 weeks"
        - "Send OncoBoost Phase III PDF"
        - "Add Dr. Sharma to advisory board invite list"
        - "Arrange product webinar"
    """
    groq = get_groq_service()

    context = format_interaction_for_llm(interaction_data)
    followup_prompt = get_followup_prompt(context)

    if not followup_prompt or len(followup_prompt) < 20:
        followup_prompt = f"""Based on this pharmaceutical sales interaction, suggest 3-5 specific, actionable follow-up actions.

Interaction details:
{context}

Consider:
- What materials or data should be shared
- When to schedule the next visit
- Any specific doctor requests to fulfill
- Relationship-building opportunities

Return a JSON object with a "suggestions" array of strings. Each suggestion should be a specific, actionable task.
Example: {{"suggestions": ["Schedule follow-up meeting in 2 weeks", "Send efficacy study PDF via email"]}}"""

    messages = [
        {
            "role": "system",
            "content": "You are a pharmaceutical sales advisor. Suggest specific, actionable follow-up actions. Return a JSON object with a 'suggestions' array.",
        },
        {"role": "user", "content": followup_prompt},
    ]

    response = groq.invoke(messages)
    result = parse_json_from_llm(response)

    if result and "suggestions" in result:
        suggestions = result["suggestions"]
        if isinstance(suggestions, list) and len(suggestions) > 0:
            logger.info(f"Generated {len(suggestions)} follow-up suggestions")
            return suggestions[:5]  # Max 5 suggestions

    # Parse as plain text list if JSON failed
    if response:
        lines = [line.strip().lstrip("•-*123456789.") .strip() 
                 for line in response.strip().split("\n") if line.strip()]
        suggestions = [s for s in lines if len(s) > 10]
        if suggestions:
            return suggestions[:5]

    # Fallback suggestions based on available data
    return _generate_fallback_suggestions(interaction_data)


def _generate_fallback_suggestions(data: dict) -> list[str]:
    """Generate generic follow-up suggestions from interaction data."""
    suggestions = []
    doctor = data.get("doctor_name") or data.get("doctor") or "the doctor"
    sentiment = data.get("sentiment", "Neutral")

    suggestions.append(f"Schedule follow-up meeting with {doctor} in 2 weeks")

    if sentiment == "Positive":
        suggestions.append(f"Send thank you email to {doctor}")
        suggestions.append("Prepare detailed product comparison sheet")
    elif sentiment == "Negative":
        suggestions.append("Address concerns raised during the meeting")
        suggestions.append("Prepare additional clinical evidence")
    
    suggestions.append("Update CRM with any additional notes")
    suggestions.append("Share relevant clinical study materials")

    return suggestions[:5]
