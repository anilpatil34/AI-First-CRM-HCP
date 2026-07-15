"""
Groq LLM service.
Wraps the Groq API via LangChain for AI inference.
"""

from typing import Optional
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

from app.config import get_settings
from app.utils.logger import get_logger

logger = get_logger(__name__)
settings = get_settings()


class GroqService:
    """Service for interacting with Groq LLM API."""

    def __init__(self):
        self.api_key = settings.GROQ_API_KEY
        self.primary_model = settings.GROQ_MODEL_PRIMARY
        self.fallback_model = settings.GROQ_MODEL_FALLBACK

        if not self.api_key or self.api_key == "your_groq_api_key_here":
            logger.warning("Groq API key not configured. AI features will be limited.")
            self.llm = None
            self.fallback_llm = None
        else:
            self.llm = ChatGroq(
                api_key=self.api_key,
                model=self.primary_model,
                temperature=0.3,
                max_tokens=2048,
            )
            self.fallback_llm = ChatGroq(
                api_key=self.api_key,
                model=self.fallback_model,
                temperature=0.3,
                max_tokens=2048,
            )
            logger.info(f"Groq service initialized with model: {self.primary_model}")

    def invoke(self, messages: list[dict]) -> str:
        """
        Send messages to Groq and return the response text.
        
        Args:
            messages: List of dicts with 'role' and 'content' keys
        
        Returns:
            AI response text
        """
        if not self.llm:
            return self._get_fallback_response(messages)

        langchain_messages = self._convert_messages(messages)

        try:
            response = self.llm.invoke(langchain_messages)
            return response.content
        except Exception as e:
            logger.error(f"Groq primary model error: {e}")
            return self.invoke_with_fallback(messages)

    def invoke_with_fallback(self, messages: list[dict]) -> str:
        """Try primary model, fall back to secondary on failure."""
        if not self.fallback_llm:
            return self._get_fallback_response(messages)

        langchain_messages = self._convert_messages(messages)

        try:
            logger.info(f"Attempting fallback model: {self.fallback_model}")
            response = self.fallback_llm.invoke(langchain_messages)
            return response.content
        except Exception as e:
            logger.error(f"Groq fallback model error: {e}")
            return self._get_fallback_response(messages)

    def _convert_messages(self, messages: list[dict]) -> list:
        """Convert dict messages to LangChain message objects."""
        langchain_messages = []
        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            if role == "system":
                langchain_messages.append(SystemMessage(content=content))
            elif role == "assistant":
                langchain_messages.append(AIMessage(content=content))
            else:
                langchain_messages.append(HumanMessage(content=content))
        return langchain_messages

    def _get_fallback_response(self, messages: list[dict]) -> str:
        """Generate a fallback response when LLM is unavailable."""
        user_msg = ""
        for msg in reversed(messages):
            if msg.get("role") == "user":
                user_msg = msg.get("content", "")
                break

        return (
            "I understand you said: \"{}\"\n\n"
            "⚠️ The AI service is currently unavailable. "
            "Please configure your Groq API key in the backend/.env file.\n\n"
            "You can get a free API key at: https://console.groq.com"
        ).format(user_msg[:100])


# Singleton instance
_groq_service: Optional[GroqService] = None


def get_groq_service() -> GroqService:
    """Get or create the Groq service singleton."""
    global _groq_service
    if _groq_service is None:
        _groq_service = GroqService()
    return _groq_service
