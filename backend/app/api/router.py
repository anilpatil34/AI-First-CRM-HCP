"""
Main API router.
Aggregates all route modules into a single router.
"""

from fastapi import APIRouter

from app.api.routes import health, chat, interaction, hcp

api_router = APIRouter()

# Include all route modules
api_router.include_router(health.router, tags=["Health"])
api_router.include_router(chat.router, tags=["Chat"])
api_router.include_router(interaction.router, tags=["Interactions"])
api_router.include_router(hcp.router, tags=["HCP"])
