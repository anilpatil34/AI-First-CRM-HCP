"""
Tool 5: Doctor Lookup
Retrieves doctor profile with interaction history from the database.
"""

from sqlalchemy.orm import Session
from typing import Optional

from app.services.doctor_service import get_doctor_by_name, search_doctors
from app.services.interaction_service import get_interactions_by_doctor
from app.utils.formatter import format_doctor_for_display
from app.utils.logger import get_logger

logger = get_logger(__name__)


def doctor_lookup(doctor_name: str, db: Session) -> dict:
    """
    Retrieve doctor profile with interaction history.
    
    Input: "Dr Sharma" or "Sharma"
    
    Output:
        {
            "found": true,
            "doctor": {
                "name": "Dr. Rajesh Sharma",
                "hospital": "Apollo Hospital, Mumbai",
                "specialization": "Cardiology",
                "phone": "+91-9876543210",
                "email": "r.sharma@apollo.com",
                "preferred_contact": "In-Person",
                "notes": "Key opinion leader..."
            },
            "interactions": [...],
            "total_meetings": 5,
            "products_discussed": ["CardioX", "OncoBoost"],
            "display_text": "formatted text for chat"
        }
    """
    # Try exact name lookup
    doctor = get_doctor_by_name(db, doctor_name)

    if not doctor:
        # Try broader search
        results = search_doctors(db, doctor_name, limit=1)
        doctor = results[0] if results else None

    if not doctor:
        logger.info(f"Doctor not found: {doctor_name}")
        return {
            "found": False,
            "doctor": None,
            "interactions": [],
            "total_meetings": 0,
            "products_discussed": [],
            "display_text": f"No doctor found matching '{doctor_name}'. Please check the name and try again.",
        }

    # Get interaction history
    interactions = get_interactions_by_doctor(db, doctor.name)
    interaction_dicts = [i.to_dict() for i in interactions]

    # Extract unique products discussed
    products = set()
    for interaction in interaction_dicts:
        topics = interaction.get("topics_discussed", "")
        if topics:
            products.add(topics[:50])  # Simple extraction
        materials = interaction.get("materials_shared", [])
        for mat in materials:
            products.add(mat)

    doctor_dict = doctor.to_dict()
    display_text = format_doctor_for_display(doctor_dict)
    
    # Add interaction summary to display
    if interactions:
        display_text += f"\n\n📊 Total Interactions: {len(interactions)}"
        display_text += f"\n📅 Last Visit: {interaction_dicts[0].get('date', 'N/A')}" if interaction_dicts else ""
    else:
        display_text += "\n\n📊 No previous interactions recorded."

    logger.info(f"Doctor lookup: {doctor.name} ({len(interactions)} interactions)")

    return {
        "found": True,
        "doctor": doctor_dict,
        "interactions": interaction_dicts[:5],  # Last 5 interactions
        "total_meetings": len(interactions),
        "products_discussed": list(products)[:10],
        "display_text": display_text,
    }
