"""
Tool 3: Summarize Interaction
Generates a professional two-paragraph meeting summary.
"""

from app.services.groq_service import get_groq_service
from app.utils.formatter import format_interaction_for_llm
from app.utils.logger import get_logger

logger = get_logger(__name__)


def summarize_interaction(interaction_data: dict) -> str:
    """
    Generate a professional 2-paragraph meeting summary.
    
    Input: Interaction data dictionary
    Output: Formatted summary string
    """
    groq = get_groq_service()

    context = format_interaction_for_llm(interaction_data)

    messages = [
        {
            "role": "system",
            "content": (
                "You are a professional pharmaceutical CRM assistant. "
                "Generate a concise, professional two-paragraph meeting summary. "
                "Paragraph 1: Describe the meeting — who was met, where, what was discussed, "
                "what products were presented, and the doctor's response. "
                "Paragraph 2: Outline the outcomes, next steps, and follow-up actions. "
                "Use professional business language. Be specific and factual. "
                "Do NOT use bullet points — write in prose paragraphs."
            ),
        },
        {
            "role": "user",
            "content": f"Summarize this interaction:\n\n{context}",
        },
    ]

    response = groq.invoke(messages)
    
    if response and len(response.strip()) > 20:
        logger.info("Generated interaction summary successfully")
        return response.strip()

    # Fallback summary from available data
    return _generate_fallback_summary(interaction_data)


def _generate_fallback_summary(data: dict) -> str:
    """Generate a basic summary from available data fields."""
    parts = []
    
    doctor = data.get("doctor_name") or data.get("doctor") or "the healthcare professional"
    itype = data.get("interaction_type", "meeting").lower()
    
    # Paragraph 1
    p1 = f"A {itype} was conducted with {doctor}"
    if data.get("date"):
        p1 += f" on {data['date']}"
    if data.get("doctor_hospital"):
        p1 += f" at {data['doctor_hospital']}"
    p1 += "."
    
    if data.get("topics_discussed"):
        p1 += f" The discussion covered: {data['topics_discussed']}."
    
    sentiment = data.get("sentiment", "Neutral")
    p1 += f" The overall sentiment was {sentiment.lower()}."
    parts.append(p1)
    
    # Paragraph 2
    p2_items = []
    if data.get("outcomes"):
        p2_items.append(f"Key outcomes: {data['outcomes']}.")
    if data.get("follow_up_actions"):
        p2_items.append(f"Follow-up: {data['follow_up_actions']}.")
    
    if p2_items:
        parts.append(" ".join(p2_items))
    else:
        parts.append("Further follow-up actions to be determined based on the discussion outcomes.")
    
    return "\n\n".join(parts)
