"""
Schema para validação de recursos FHIR Procedure - Procedimento Realizado (BR Core)
Suporta SIGTAP e TUSS
"""
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List

from .base import (
    Identifier, Meta, CodeableConcept, Reference, Annotation, Period,
    SYSTEM_TUSS, SYSTEM_SIGTAP, PROFILE_BR_PROCEDURE
)


class ProcedurePerformer(BaseModel):
    """
    Profissional que realizou o procedimento
    """
    function: Optional[CodeableConcept] = None
    actor: Reference
    onBehalfOf: Optional[Reference] = None


class ProcedureFocalDevice(BaseModel):
    """
    Dispositivo utilizado no procedimento
    """
    action: Optional[CodeableConcept] = None
    manipulated: Reference


class ProcedureResource(BaseModel):
    """
    Recurso FHIR Procedure - Procedimento Realizado
    Conforme BR Core, usando SIGTAP e TUSS
    """
    resourceType: str = Field(default="Procedure")
    id: Optional[str] = None
    meta: Optional[Meta] = None
    identifier: Optional[List[Identifier]] = None
    instantiatesCanonical: Optional[List[str]] = None
    instantiatesUri: Optional[List[str]] = None
    basedOn: Optional[List[Reference]] = None
    partOf: Optional[List[Reference]] = None
    status: str
    statusReason: Optional[CodeableConcept] = None
    category: Optional[CodeableConcept] = None
    code: Optional[CodeableConcept] = None
    subject: Reference
    encounter: Optional[Reference] = None
    performedDateTime: Optional[str] = None
    performedPeriod: Optional[Period] = None
    performedString: Optional[str] = None
    performedAge: Optional[dict] = None
    performedRange: Optional[dict] = None
    recorder: Optional[Reference] = None
    asserter: Optional[Reference] = None
    performer: Optional[List[ProcedurePerformer]] = None
    location: Optional[Reference] = None
    reasonCode: Optional[List[CodeableConcept]] = None
    reasonReference: Optional[List[Reference]] = None
    bodySite: Optional[List[CodeableConcept]] = None
    outcome: Optional[CodeableConcept] = None
    report: Optional[List[Reference]] = None
    complication: Optional[List[CodeableConcept]] = None
    complicationDetail: Optional[List[Reference]] = None
    followUp: Optional[List[CodeableConcept]] = None
    note: Optional[List[Annotation]] = None
    focalDevice: Optional[List[ProcedureFocalDevice]] = None
    usedReference: Optional[List[Reference]] = None
    usedCode: Optional[List[CodeableConcept]] = None

    @field_validator('resourceType')
    @classmethod
    def validate_resource_type(cls, v):
        if v != "Procedure":
            raise ValueError('resourceType must be "Procedure"')
        return v

    @field_validator('status')
    @classmethod
    def validate_status(cls, v):
        valid_statuses = [
            'preparation', 'in-progress', 'not-done', 'on-hold',
            'stopped', 'completed', 'entered-in-error', 'unknown'
        ]
        if v not in valid_statuses:
            raise ValueError(f'status must be one of {valid_statuses}')
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "resourceType": "Procedure",
                "meta": {
                    "profile": [PROFILE_BR_PROCEDURE]
                },
                "status": "completed",
                "code": {
                    "coding": [
                        {
                            "system": SYSTEM_SIGTAP,
                            "code": "0301010072",
                            "display": "Consulta médica em atenção básica"
                        },
                        {
                            "system": SYSTEM_TUSS,
                            "code": "10101012",
                            "display": "Consulta em consultório"
                        }
                    ],
                    "text": "Consulta médica"
                },
                "subject": {
                    "reference": "Patient/123"
                },
                "encounter": {
                    "reference": "Encounter/456"
                },
                "performedDateTime": "2024-01-15T10:00:00-03:00",
                "performer": [
                    {
                        "actor": {
                            "reference": "Practitioner/789",
                            "display": "Dra. Maria Santos"
                        }
                    }
                ],
                "reasonCode": [
                    {
                        "coding": [
                            {
                                "system": "http://hl7.org/fhir/sid/icd-10",
                                "code": "J06.9",
                                "display": "IVAS"
                            }
                        ]
                    }
                ]
            }
        }
