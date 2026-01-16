"""
Serviços de negócio para recursos FHIR
"""
from .patient import PatientService
from .observation import ObservationService
from .practitioner import PractitionerService
from .encounter import EncounterService

__all__ = ["PatientService", "ObservationService", "PractitionerService", "EncounterService"]

