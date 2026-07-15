"""
Models package initialization.
Imports all models to register them with SQLAlchemy's metadata.
"""

from app.models.doctor import Doctor
from app.models.interaction import Interaction
from app.models.material import Material
from app.models.sample import Sample

__all__ = ["Doctor", "Interaction", "Material", "Sample"]
