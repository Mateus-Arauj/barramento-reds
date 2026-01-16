"""
Repositories para acesso a dados de recursos FHIR
"""
from .base import BaseRepository
from .patient import PatientRepository
from .observation import ObservationRepository
from .practitioner import PractitionerRepository
from .encounter import EncounterRepository

__all__ = [
    "BaseRepository",
    "PatientRepository",
    "ObservationRepository",
    "PractitionerRepository",
    "EncounterRepository"
]
