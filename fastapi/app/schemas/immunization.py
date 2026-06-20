"""
Schema para validação de recursos FHIR Immunization - Imunização (BR Core / PNI)
"""
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List

from .base import (
    Identifier, Meta, CodeableConcept, Reference, Annotation, Quantity,
    PROFILE_BR_IMMUNIZATION
)


class ImmunizationPerformer(BaseModel):
    """
    Profissional que administrou a vacina
    """
    function: Optional[CodeableConcept] = None
    actor: Reference


class ImmunizationEducation(BaseModel):
    """
    Informação educacional fornecida ao paciente
    """
    documentType: Optional[str] = None
    reference: Optional[str] = None
    publicationDate: Optional[str] = None
    presentationDate: Optional[str] = None


class ImmunizationReaction(BaseModel):
    """
    Reação pós-vacinal
    """
    date: Optional[str] = None
    detail: Optional[Reference] = None
    reported: Optional[bool] = None


class ImmunizationProtocolApplied(BaseModel):
    """
    Protocolo aplicado (dose na série)
    """
    series: Optional[str] = None
    authority: Optional[Reference] = None
    targetDisease: Optional[List[CodeableConcept]] = None
    doseNumberPositiveInt: Optional[int] = None
    doseNumberString: Optional[str] = None
    seriesDosesPositiveInt: Optional[int] = None
    seriesDosesString: Optional[str] = None


class ImmunizationResource(BaseModel):
    """
    Recurso FHIR Immunization - Imunobiológico Administrado
    Conforme BR Core / PNI (Programa Nacional de Imunizações)
    """
    resourceType: str = Field(default="Immunization")
    id: Optional[str] = None
    meta: Optional[Meta] = None
    identifier: Optional[List[Identifier]] = None
    status: str
    statusReason: Optional[CodeableConcept] = None
    vaccineCode: CodeableConcept
    patient: Reference
    encounter: Optional[Reference] = None
    occurrenceDateTime: Optional[str] = None
    occurrenceString: Optional[str] = None
    recorded: Optional[str] = None
    primarySource: Optional[bool] = None
    reportOrigin: Optional[CodeableConcept] = None
    location: Optional[Reference] = None
    manufacturer: Optional[Reference] = None
    lotNumber: Optional[str] = None
    expirationDate: Optional[str] = None
    site: Optional[CodeableConcept] = None
    route: Optional[CodeableConcept] = None
    doseQuantity: Optional[Quantity] = None
    performer: Optional[List[ImmunizationPerformer]] = None
    note: Optional[List[Annotation]] = None
    reasonCode: Optional[List[CodeableConcept]] = None
    reasonReference: Optional[List[Reference]] = None
    isSubpotent: Optional[bool] = None
    subpotentReason: Optional[List[CodeableConcept]] = None
    education: Optional[List[ImmunizationEducation]] = None
    programEligibility: Optional[List[CodeableConcept]] = None
    fundingSource: Optional[CodeableConcept] = None
    reaction: Optional[List[ImmunizationReaction]] = None
    protocolApplied: Optional[List[ImmunizationProtocolApplied]] = None

    @field_validator('resourceType')
    @classmethod
    def validate_resource_type(cls, v):
        if v != "Immunization":
            raise ValueError('resourceType must be "Immunization"')
        return v

    @field_validator('status')
    @classmethod
    def validate_status(cls, v):
        valid_statuses = ['completed', 'entered-in-error', 'not-done']
        if v not in valid_statuses:
            raise ValueError(f'status must be one of {valid_statuses}')
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "resourceType": "Immunization",
                "meta": {
                    "profile": [PROFILE_BR_IMMUNIZATION]
                },
                "status": "completed",
                "vaccineCode": {
                    "coding": [
                        {
                            "system": "http://www.saude.gov.br/fhir/r4/CodeSystem/BRImunobiologico",
                            "code": "86",
                            "display": "COVID-19 - Pfizer/BioNTech"
                        }
                    ],
                    "text": "Vacina COVID-19 Pfizer"
                },
                "patient": {
                    "reference": "Patient/123"
                },
                "encounter": {
                    "reference": "Encounter/456"
                },
                "occurrenceDateTime": "2024-01-15T09:00:00-03:00",
                "recorded": "2024-01-15T09:05:00-03:00",
                "primarySource": True,
                "location": {
                    "reference": "Location/ubs-001",
                    "display": "UBS Centro"
                },
                "manufacturer": {
                    "display": "Pfizer/BioNTech"
                },
                "lotNumber": "EW0150",
                "expirationDate": "2024-06-30",
                "site": {
                    "coding": [
                        {
                            "system": "http://terminology.hl7.org/CodeSystem/v3-ActSite",
                            "code": "LA",
                            "display": "Left arm"
                        }
                    ],
                    "text": "Braço esquerdo"
                },
                "route": {
                    "coding": [
                        {
                            "system": "http://terminology.hl7.org/CodeSystem/v3-RouteOfAdministration",
                            "code": "IM",
                            "display": "Injection, intramuscular"
                        }
                    ],
                    "text": "Intramuscular"
                },
                "doseQuantity": {
                    "value": 0.3,
                    "unit": "mL",
                    "system": "http://unitsofmeasure.org",
                    "code": "mL"
                },
                "protocolApplied": [
                    {
                        "series": "Série primária",
                        "doseNumberPositiveInt": 1,
                        "seriesDosesPositiveInt": 2,
                        "targetDisease": [
                            {
                                "coding": [
                                    {
                                        "system": "http://hl7.org/fhir/sid/icd-10",
                                        "code": "U07.1",
                                        "display": "COVID-19"
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        }
