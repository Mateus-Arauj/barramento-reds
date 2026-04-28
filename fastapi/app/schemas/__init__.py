"""
Pydantic schemas para validação de recursos FHIR - BR Core
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
from .organization import OrganizationResource, OrganizationContact
from .location import LocationResource, LocationPosition, LocationHoursOfOperation
from .condition import ConditionResource, ConditionStage, ConditionEvidence
from .procedure import ProcedureResource, ProcedurePerformer, ProcedureFocalDevice
from .allergy_intolerance import AllergyIntoleranceResource, AllergyIntoleranceReaction
from .diagnostic_report import DiagnosticReportResource, DiagnosticReportMedia
from .immunization import (
    ImmunizationResource,
    ImmunizationPerformer,
    ImmunizationReaction,
    ImmunizationProtocolApplied
)
from .base import (
    Identifier,
    HumanName,
    ContactPoint,
    Address,
    Meta,
    CodeableConcept,
    Quantity,
    Range,
    Ratio,
    Period,
    Reference,
    Annotation,
    Coding,
    Duration,
    Attachment,
    Dosage,
    SYSTEM_CPF,
    SYSTEM_CNS,
    SYSTEM_RG,
    SYSTEM_CRM_PREFIX,
    SYSTEM_COREN_PREFIX,
    SYSTEM_CRO_PREFIX,
    SYSTEM_CRF_PREFIX,
    SYSTEM_CRP_PREFIX,
    SYSTEM_CBO,
    SYSTEM_TUSS,
    SYSTEM_SIGTAP,
    SYSTEM_IBGE,
    SYSTEM_CNES,
    SYSTEM_CNPJ,
    SYSTEM_CID10,
    SYSTEM_CIAP2,
    SYSTEM_LOINC,
    SYSTEM_SNOMED,
    SYSTEM_UCUM,
    SYSTEM_ATC,
    SYSTEM_ANVISA,
    PROFILE_BR_PATIENT,
    PROFILE_BR_PRACTITIONER,
    PROFILE_BR_ORGANIZATION,
    PROFILE_BR_ENCOUNTER,
    PROFILE_BR_OBSERVATION,
    PROFILE_BR_CONDITION,
    PROFILE_BR_PROCEDURE,
    PROFILE_BR_MEDICATION_REQUEST,
    PROFILE_BR_IMMUNIZATION,
    PROFILE_BR_ALLERGY,
    PROFILE_BR_DIAGNOSTIC_REPORT,
    PROFILE_BR_LOCATION,
    UF_BRAZIL,
)


