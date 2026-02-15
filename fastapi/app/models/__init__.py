"""
Modelos SQLAlchemy para recursos FHIR - BR Core
"""
from .base import Base, TimestampMixin, generate_uuid
from .patient import Patient
from .observation import Observation
from .practitioner import Practitioner
from .encounter import Encounter
from .organization import Organization
from .location import Location
from .condition import Condition
from .procedure import Procedure
from .allergy_intolerance import AllergyIntolerance
from .diagnostic_report import DiagnosticReport
from .immunization import Immunization

__all__ = [
    "Base",
    "TimestampMixin",
    "generate_uuid",
    "Patient",
    "Observation",
    "Practitioner",
    "Encounter",
    "Organization",
    "Location",
    "Condition",
    "Procedure",
    "AllergyIntolerance",
    "DiagnosticReport",
    "Immunization",
]
