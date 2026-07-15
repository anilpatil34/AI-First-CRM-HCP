"""
LangGraph tool routing logic.
Routes user intents to the appropriate tool.
"""

from app.graph.state import AgentState


# Intent keywords mapping
INTENT_KEYWORDS = {
    "log": ["met", "visited", "discussed", "meeting", "spoke", "talked", "saw", "interaction", "called", "attended", "conference", "presented", "email", "sent", "replied", "wrote", "mailed", "message", "logged"],
    "edit": ["change", "update", "modify", "edit", "correct", "fix", "set", "make it", "switch"],
    "summarize": ["summarize", "summary", "recap", "overview", "brief", "what happened"],
    "followup": ["follow up", "follow-up", "followup", "next steps", "suggest", "recommend", "what should", "action items"],
    "lookup": ["look up", "lookup", "find", "search", "who is", "tell me about", "doctor info", "profile", "details about"],
}


def detect_intent(user_message: str) -> str:
    """
    Detect user intent from the message text.
    Uses keyword matching as a fast first-pass classifier.
    """
    message_lower = user_message.lower().strip()

    # Score each intent
    scores = {}
    for intent, keywords in INTENT_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in message_lower)
        if score > 0:
            scores[intent] = score

    if not scores:
        return "general"

    # Prioritize log over followup if both match (e.g. logging an interaction that mentions follow-ups)
    if "log" in scores and "followup" in scores:
        # Check if they are just asking for suggestions
        if any(q in message_lower for q in ["what follow-up", "what follow up", "suggest follow", "recommend follow"]):
            return "followup"
        return "log"

    # Return the intent with the highest score
    return max(scores, key=scores.get)


def route_to_tool(state: AgentState) -> str:
    """
    Route based on detected intent.
    Returns the next node name in the graph.
    """
    intent = state.get("intent", "general")

    tool_mapping = {
        "log": "log_interaction",
        "edit": "edit_interaction",
        "summarize": "summarize_interaction",
        "followup": "suggest_followup",
        "lookup": "doctor_lookup",
    }

    return tool_mapping.get(intent, "general_response")
