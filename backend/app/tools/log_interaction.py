"""
Tool 1: Log Interaction
Extracts structured interaction data from natural language descriptions.
"""

from app.services.groq_service import get_groq_service
from app.services.prompt_service import get_extraction_prompt
from app.utils.parser import parse_json_from_llm, parse_date, parse_time
from app.utils.logger import get_logger

logger = get_logger(__name__)


def log_interaction(user_message: str, context: dict = None) -> dict:
    """
    Extract structured data from a natural language interaction description.
    
    Input example:
        "Met Dr Sharma today. Discussed CardioX. Doctor liked efficacy. 
         Shared brochure. Follow-up next Tuesday."
    
    Output:
        {
            "doctor": "Dr Sharma",
            "product": "CardioX",
            "sentiment": "Positive",
            "topics": ["efficacy"],
            "materials": ["brochure"],
            "summary": "...",
            "follow_up": "...",
            "date": "2026-07-09",
            "interaction_type": "Meeting"
        }
    """
    groq = get_groq_service()
    
    extraction_prompt = get_extraction_prompt(user_message)
    if not extraction_prompt:
        extraction_prompt = f"""Extract structured CRM data from this interaction description. Return a JSON object with these fields:
- doctor: Doctor's name (string)
- product: Product discussed (string)  
- sentiment: "Positive", "Neutral", or "Negative" (string)
- topics: Key discussion topics (array of strings)
- materials: Materials shared (array of strings)
- samples: Samples distributed (array of strings)
- summary: Professional 2-sentence summary (string)
- follow_up: Recommended follow-up action (string)
- outcomes: Key outcomes or agreements (string)
- date: Date of interaction (string, or "today" if mentioned)
- time: Time of interaction (string, if mentioned)
- interaction_type: "Meeting", "Call", "Email", "Conference", or "Other" (string)
- attendees: List of attendees (array of strings)

User message: {user_message}

Return ONLY the JSON object, no other text."""

    messages = [
        {"role": "system", "content": "You are a pharmaceutical CRM data extraction assistant. Extract structured data from interaction descriptions. Always respond with valid JSON."},
        {"role": "user", "content": extraction_prompt},
    ]

    response = groq.invoke(messages)
    extracted = parse_json_from_llm(response)

    if extracted:
        # Normalize date and time
        if extracted.get("date"):
            extracted["date"] = parse_date(extracted["date"]) or extracted["date"]
        if extracted.get("time"):
            extracted["time"] = parse_time(extracted["time"]) or extracted["time"]
        
        logger.info(f"Extracted interaction data: doctor={extracted.get('doctor')}, sentiment={extracted.get('sentiment')}")
        return extracted

    # Fallback: return basic structure
    logger.warning("Failed to parse LLM extraction response, returning defaults")
    return {
        "doctor": "",
        "product": "",
        "sentiment": "Neutral",
        "topics": [],
        "materials": [],
        "samples": [],
        "summary": user_message,
        "follow_up": "",
        "outcomes": "",
        "date": "",
        "time": "",
        "interaction_type": "Meeting",
        "attendees": [],
    }
