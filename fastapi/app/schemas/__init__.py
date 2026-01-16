"""
Pydantic schemas para validação de recursos FHIR
"""
from .patient import PatientResource
from .observation import ObservationResource
from .practitioner import PractitionerResource, PractitionerQualification
from .encounter import (
    EncounterResource,
    EncounterStatusHistory,
    EncounterClassHistory,
    EncounterParticipant,
    EncounterDiagnosis,
    EncounterHospitalization,
    EncounterLocation
)
from .base import (
    Identifier,
    HumanName,
    ContactPoint,
    Address,
    Meta,
    CodeableConcept,
    Quantity,
    Period,
    Reference,
    Annotation,
    Coding,
    Duration,
    Attachment
)

__all__ = [
    "PatientResource",
    "ObservationResource",
    "PractitionerResource",
    "PractitionerQualification",
    "EncounterResource",
    "EncounterStatusHistory",
    "EncounterClassHistory",
    "EncounterParticipant",
    "EncounterDiagnosis",
    "EncounterHospitalization",
    "EncounterLocation",
    "Identifier",
    "HumanName",
    "ContactPoint",
    "Address",
    "Meta",
    "CodeableConcept",
    "Quantity",
    "Period",
    "Reference",
    "Annotation",
    "Coding",
    "Duration",
    "Attachment",
    "SYSTEM_CPF",
    "SYSTEM_CNS",
    "SYSTEM_CRM_PREFIX",
    "SYSTEM_COREN_PREFIX",
    "SYSTEM_CRO_PREFIX",
    "SYSTEM_CBO",
    "SYSTEM_TUSS",
    "SYSTEM_SIGTAP",
    "SYSTEM_IBGE"
]


