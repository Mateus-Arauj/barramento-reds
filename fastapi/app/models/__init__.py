"""
Modelos SQLAlchemy para recursos FHIR
"""
from .base import Base, TimestampMixin, generate_uuid
from .patient import Patient
from .observation import Observation
from .practitioner import Practitioner
from .encounter import Encounter

__all__ = [
    "Base",
    "TimestampMixin",
    "generate_uuid",
    "Patient",
    "Observation",
    "Practitioner",
    "Encounter"
]
