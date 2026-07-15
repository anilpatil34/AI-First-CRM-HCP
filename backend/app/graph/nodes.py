"""
LangGraph node functions.
Each node processes the state and returns updated state.
"""

from app.graph.state import AgentState
from app.graph.router import detect_intent
from app.tools.log_interaction import log_interaction
from app.tools.edit_interaction import edit_interaction
from app.tools.summarize_interaction import summarize_interaction
from app.tools.suggest_followup import suggest_followup
from app.tools.doctor_lookup import doctor_lookup
from app.services.groq_service import get_groq_service
from app.services.prompt_service import get_system_prompt
from app.utils.logger import get_logger

logger = get_logger(__name__)


def intent_node(state: AgentState) -> dict:
    """Detect user intent from the message."""
    user_message = state["user_message"]
    intent = detect_intent(user_message)
    logger.info(f"Detected intent: {intent}")
    return {"intent": intent}


def tool_node(state: AgentState) -> dict:
    """Execute the appropriate tool based on detected intent."""
    intent = state.get("intent", "general")
    user_message = state["user_message"]
    db = state.get("db")
    tool_calls = []

    try:
        if intent == "log":
            result = log_interaction(user_message)
            tool_calls.append({"tool_name": "log_interaction", "arguments": {"message": user_message[:100]}, "result": "Data extracted"})
            
            # Build form updates from extracted data
            form_updates = {}
            field_mapping = {
                "doctor": "hcpName",
                "sentiment": "sentiment",
                "date": "date",
                "time": "time",
                "topics": "topicsDiscussed",
                "summary": "summary",
                "follow_up": "followUpActions",
                "outcomes": "outcomes",
                "interaction_type": "interactionType",
                "materials": "materialsShared",
                "samples": "samplesDistributed",
                "attendees": "attendees",
            }
            
            for src, dst in field_mapping.items():
                value = result.get(src)
                if value:
                    if isinstance(value, list):
                        if dst == "topicsDiscussed":
                            form_updates[dst] = ", ".join(value)
                        else:
                            form_updates[dst] = value
                    else:
                        form_updates[dst] = value
            
            form_updates["aiGenerated"] = True
            
            # Generate follow-up suggestions
            suggestions = suggest_followup(result)
            tool_calls.append({"tool_name": "suggest_followup", "arguments": {}, "result": f"{len(suggestions)} suggestions"})

            return {
                "extracted_data": result,
                "form_updates": form_updates,
                "tool_calls": tool_calls,
                "suggestions": suggestions,
                "tool_result": result,
            }

        elif intent == "edit":
            result = edit_interaction(user_message)
            tool_calls.append({"tool_name": "edit_interaction", "arguments": {"message": user_message[:100]}, "result": result})
            
            form_updates = {}
            updates = result.get("updates", {})
            field_mapping = {
                "sentiment": "sentiment",
                "interaction_type": "interactionType",
                "date": "date",
                "time": "time",
                "topics_discussed": "topicsDiscussed",
                "outcomes": "outcomes",
                "follow_up_actions": "followUpActions",
                "summary": "summary",
            }
            for src, dst in field_mapping.items():
                if src in updates:
                    form_updates[dst] = updates[src]

            return {
                "extracted_data": result,
                "form_updates": form_updates if form_updates else None,
                "tool_calls": tool_calls,
                "tool_result": result,
            }

        elif intent == "summarize":
            current_data = state.get("extracted_data") or {}
            summary = summarize_interaction(current_data)
            tool_calls.append({"tool_name": "summarize_interaction", "arguments": {}, "result": "Summary generated"})
            
            return {
                "tool_calls": tool_calls,
                "form_updates": {"summary": summary},
                "tool_result": {"summary": summary},
            }

        elif intent == "followup":
            current_data = state.get("extracted_data") or {}
            suggestions = suggest_followup(current_data)
            tool_calls.append({"tool_name": "suggest_followup", "arguments": {}, "result": f"{len(suggestions)} suggestions"})
            
            return {
                "suggestions": suggestions,
                "tool_calls": tool_calls,
                "tool_result": {"suggestions": suggestions},
            }

        elif intent == "lookup":
            if db:
                # Extract doctor name from the message
                import re
                name_match = re.search(r"(?:dr\.?\s+[a-zA-Z\s]+)", user_message, re.IGNORECASE)
                search_name = name_match.group(0).strip() if name_match else user_message
                result = doctor_lookup(search_name, db)
            else:
                result = {"found": False, "display_text": "Database not available for lookup."}
            tool_calls.append({"tool_name": "doctor_lookup", "arguments": {"name": search_name if db else user_message[:50]}, "result": result.get("display_text", "")[:100]})
            
            return {
                "extracted_data": result.get("doctor"),
                "tool_calls": tool_calls,
                "tool_result": result,
            }

    except Exception as e:
        logger.error(f"Tool execution error ({intent}): {e}")
        return {
            "tool_calls": [{"tool_name": intent, "arguments": {}, "result": f"Error: {str(e)}"}],
            "tool_result": {"error": str(e)},
        }

    return {}


def response_node(state: AgentState) -> dict:
    """Generate the final AI response based on tool results."""
    intent = state.get("intent", "general")
    user_message = state["user_message"]
    tool_result = state.get("tool_result")
    messages = state.get("messages", [])

    groq = get_groq_service()
    system_prompt = get_system_prompt()

    if not system_prompt:
        system_prompt = (
            "You are an AI assistant for a pharmaceutical CRM system. "
            "Help sales representatives log doctor interactions, edit records, "
            "generate summaries, suggest follow-ups, and look up doctor profiles. "
            "Be professional, concise, and helpful."
        )

    # Build context from tool results
    context = ""
    if intent == "log" and tool_result:
        doctor = tool_result.get("doctor", "the doctor")
        sentiment = tool_result.get("sentiment", "neutral")
        context = (
            f"I've extracted the interaction data and populated the form. "
            f"Doctor: {doctor}, Sentiment: {sentiment}. "
            "The form has been auto-filled with the extracted information. "
            "Please let the user know what was captured and ask if anything needs to be corrected."
        )
    elif intent == "edit" and tool_result:
        field = tool_result.get("field", "a field")
        value = tool_result.get("value", "")
        context = f"I've updated the {field} to '{value}'. Confirm this change to the user."
    elif intent == "summarize" and tool_result:
        summary = tool_result.get("summary", "")
        context = f"I generated this summary:\n{summary}\nConfirm to the user that the summary has been generated."
    elif intent == "followup" and tool_result:
        suggestions = tool_result.get("suggestions", [])
        context = f"I generated these follow-up suggestions:\n" + "\n".join(f"• {s}" for s in suggestions)
    elif intent == "lookup" and tool_result:
        context = tool_result.get("display_text", "No information found.")

    # Build messages for response generation
    llm_messages = [
        {"role": "system", "content": system_prompt},
    ]

    # Add recent conversation history (last 4 messages)
    for msg in messages[-4:]:
        llm_messages.append(msg)

    if context:
        llm_messages.append({
            "role": "system",
            "content": f"Tool execution result:\n{context}\n\nGenerate a helpful, conversational response based on this result.",
        })

    llm_messages.append({"role": "user", "content": user_message})

    response = groq.invoke(llm_messages)

    return {"response": response}
