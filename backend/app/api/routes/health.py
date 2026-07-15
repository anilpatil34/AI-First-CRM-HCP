"""
Health check API endpoint.
Provides application health status and dependency checks.
"""

from datetime import datetime, timezone
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.database.session import get_db
from app.config import get_settings

router = APIRouter()
settings = get_settings()


@router.get("/health", tags=["Health"])
def health_check(db: Session = Depends(get_db)):
    """
    Health check endpoint.
    Returns API status, database connectivity, and version info.
    """
    # Check database
    db_status = "connected"
    try:
        db.execute(text("SELECT 1"))
    except Exception:
        db_status = "error"

    # Check Groq API key
    groq_status = "configured" if (
        settings.GROQ_API_KEY and settings.GROQ_API_KEY != "your_groq_api_key_here"
    ) else "not_configured"

    return {
        "status": "healthy",
        "version": settings.APP_VERSION,
        "app_name": settings.APP_NAME,
        "database": db_status,
        "groq_api": groq_status,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
