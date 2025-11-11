"""
Serviços de negócio para recursos FHIR
"""
from .patient import PatientService
from .observation import ObservationService

__all__ = ["PatientService", "ObservationService"]
