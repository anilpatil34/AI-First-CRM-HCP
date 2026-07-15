"""
Chat API endpoint.
Processes user messages through the LangGraph AI assistant.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.chat_schema import ChatRequest, ChatResponse
from app.services.chat_service import get_chat_service
from app.utils.logger import get_logger

router = APIRouter()
logger = get_logger(__name__)


@router.post("/chat", tags=["Chat"], response_model=ChatResponse)
def chat(request: ChatRequest, db: Session = Depends(get_db)):
    """
    Send a message to the AI assistant.
    
    The AI will:
    - Detect intent (log, edit, summarize, followup, lookup, general)
    - Execute appropriate tools
    - Return structured response with extracted data and form updates
    """
    try:
        chat_service = get_chat_service()
        response = chat_service.process_message(request, db)
        return response
    except Exception as e:
        logger.error(f"Chat endpoint error: {e}")
        raise HTTPException(
            status_code=500,
            detail="An error occurred while processing your message. Please try again."
        )
