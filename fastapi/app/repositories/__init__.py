"""
Repositories para acesso a dados de recursos FHIR
"""
from .base import BaseRepository
from .patient import PatientRepository
from .observation import ObservationRepository
from .practitioner import PractitionerRepository
from .encounter import EncounterRepository
from .organization import OrganizationRepository
from .location import LocationRepository
from .condition import ConditionRepository
from .procedure import ProcedureRepository
from .allergy_intolerance import AllergyIntoleranceRepository
from .diagnostic_report import DiagnosticReportRepository
from .immunization import ImmunizationRepository

__all__ = [
    "BaseRepository",
    "PatientRepository",
    "ObservationRepository",
    "PractitionerRepository",
    "EncounterRepository",
    "OrganizationRepository",
    "LocationRepository",
    "ConditionRepository",
    "ProcedureRepository",
    "AllergyIntoleranceRepository",
    "DiagnosticReportRepository",
    "ImmunizationRepository",
]
