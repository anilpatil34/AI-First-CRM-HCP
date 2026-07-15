"""
Interaction API endpoints.
Provides CRUD operations for HCP interaction records.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.interaction_schema import (
    InteractionCreate, InteractionUpdate, InteractionResponse, InteractionList
)
from app.services import interaction_service

router = APIRouter()


@router.post("/interaction", tags=["Interactions"], response_model=InteractionResponse, status_code=201)
def create_interaction(data: InteractionCreate, db: Session = Depends(get_db)):
    """Create a new HCP interaction record."""
    interaction = interaction_service.create_interaction(db, data)
    return interaction.to_dict()


@router.get("/interaction/{interaction_id}", tags=["Interactions"], response_model=InteractionResponse)
def get_interaction(interaction_id: int, db: Session = Depends(get_db)):
    """Get a specific interaction by ID."""
    interaction = interaction_service.get_interaction_by_id(db, interaction_id)
    if not interaction:
        raise HTTPException(status_code=404, detail="Interaction not found")
    return interaction.to_dict()


@router.put("/interaction/{interaction_id}", tags=["Interactions"], response_model=InteractionResponse)
def update_interaction(interaction_id: int, data: InteractionUpdate, db: Session = Depends(get_db)):
    """Update an existing interaction."""
    interaction = interaction_service.update_interaction(db, interaction_id, data)
    if not interaction:
        raise HTTPException(status_code=404, detail="Interaction not found")
    return interaction.to_dict()


@router.delete("/interaction/{interaction_id}", tags=["Interactions"])
def delete_interaction(interaction_id: int, db: Session = Depends(get_db)):
    """Delete an interaction."""
    success = interaction_service.delete_interaction(db, interaction_id)
    if not success:
        raise HTTPException(status_code=404, detail="Interaction not found")
    return {"message": "Interaction deleted successfully", "id": interaction_id}


@router.get("/interactions", tags=["Interactions"], response_model=InteractionList)
def list_interactions(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    """Get all interactions with pagination."""
    items, total = interaction_service.get_all_interactions(db, skip=skip, limit=limit)
    return InteractionList(
        items=[InteractionResponse(**i.to_dict()) for i in items],
        total=total,
        skip=skip,
        limit=limit,
    )


@router.get("/history/{doctor_name}", tags=["Interactions"])
def get_interaction_history(doctor_name: str, db: Session = Depends(get_db)):
    """Get interaction history for a specific doctor."""
    interactions = interaction_service.get_interactions_by_doctor(db, doctor_name)
    return {
        "doctor_name": doctor_name,
        "total": len(interactions),
        "interactions": [i.to_dict() for i in interactions],
    }
