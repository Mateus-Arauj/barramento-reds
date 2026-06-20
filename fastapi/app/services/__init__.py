"""
Serviços de negócio para recursos FHIR
"""
from .patient import PatientService
from .observation import ObservationService
from .practitioner import PractitionerService
from .encounter import EncounterService
from .organization import OrganizationService
from .location import LocationService
from .condition import ConditionService
from .procedure import ProcedureService
from .allergy_intolerance import AllergyIntoleranceService
from .diagnostic_report import DiagnosticReportService
from .immunization import ImmunizationService

__all__ = [
    "PatientService",
    "ObservationService",
    "PractitionerService",
    "EncounterService",
    "OrganizationService",
    "LocationService",
    "ConditionService",
    "ProcedureService",
    "AllergyIntoleranceService",
    "DiagnosticReportService",
    "ImmunizationService",
]

