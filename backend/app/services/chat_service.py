"""
Chat service layer.
Orchestrates the AI chat flow by invoking the LangGraph agent.
"""

from sqlalchemy.orm import Session
from typing import Optional

from app.schemas.chat_schema import ChatRequest, ChatResponse
from app.graph.graph import get_graph
from app.graph.memory import get_memory_store
from app.utils.logger import get_logger

logger = get_logger(__name__)


class ChatService:
    """Service for processing chat messages through the LangGraph agent."""

    def __init__(self):
        self.graph = get_graph()
        self.memory = get_memory_store()

    def process_message(
        self, request: ChatRequest, db: Session
    ) -> ChatResponse:
        """
        Process a user chat message through the LangGraph pipeline.
        
        Args:
            request: Chat request with message and session_id
            db: Database session for tool operations
        
        Returns:
            ChatResponse with AI response, extracted data, and suggestions
        """
        session_id = request.session_id
        logger.info(f"Processing message for session {session_id}: {request.message[:50]}...")

        # Get conversation history
        history = self.memory.get_history(session_id)

        # Build initial state for the graph
        initial_state = {
            "messages": history + [{"role": "user", "content": request.message}],
            "user_message": request.message,
            "session_id": session_id,
            "db": db,
            "extracted_data": None,
            "tool_calls": [],
            "suggestions": [],
            "form_updates": None,
            "response": "",
        }

        try:
            # Run the LangGraph agent
            result = self.graph.invoke(initial_state)

            # Save messages to memory
            self.memory.add_message(session_id, "user", request.message)
            self.memory.add_message(session_id, "assistant", result.get("response", ""))

            return ChatResponse(
                response=result.get("response", "I processed your message but couldn't generate a response."),
                extracted_data=result.get("extracted_data"),
                tool_calls=result.get("tool_calls", []),
                suggestions=result.get("suggestions", []),
                form_updates=result.get("form_updates"),
                session_id=session_id,
            )

        except Exception as e:
            logger.error(f"Chat processing error: {e}")

            # Save the user message even on error
            self.memory.add_message(session_id, "user", request.message)

            error_response = (
                "I apologize, but I encountered an error processing your message. "
                "Please try again or rephrase your request."
            )
            self.memory.add_message(session_id, "assistant", error_response)

            return ChatResponse(
                response=error_response,
                extracted_data=None,
                tool_calls=[],
                suggestions=[],
                form_updates=None,
                session_id=session_id,
            )


# Singleton instance
_chat_service: Optional[ChatService] = None


def get_chat_service() -> ChatService:
    """Get or create the chat service singleton."""
    global _chat_service
    if _chat_service is None:
        _chat_service = ChatService()
    return _chat_service
