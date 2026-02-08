"""
Schema para validação de recursos FHIR Condition - Diagnóstico (BR Core)
Suporta CID-10 e CIAP-2
"""
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List

from .base import (
    Identifier, Meta, CodeableConcept, Reference, Annotation, Period,
    SYSTEM_CID10, SYSTEM_CIAP2, PROFILE_BR_CONDITION
)


class ConditionStage(BaseModel):
    """
    Estágio/classificação da condição
    """
    summary: Optional[CodeableConcept] = None
    assessment: Optional[List[Reference]] = None
    type: Optional[CodeableConcept] = None


class ConditionEvidence(BaseModel):
    """
    Evidência que suporta o diagnóstico
    """
    code: Optional[List[CodeableConcept]] = None
    detail: Optional[List[Reference]] = None


class ConditionResource(BaseModel):
    """
    Recurso FHIR Condition - Diagnóstico/Problema de Saúde
    Conforme BR Core, usando CID-10 e CIAP-2
    """
    resourceType: str = Field(default="Condition")
    id: Optional[str] = None
    meta: Optional[Meta] = None
    identifier: Optional[List[Identifier]] = None
    clinicalStatus: Optional[CodeableConcept] = None
    verificationStatus: Optional[CodeableConcept] = None
    category: Optional[List[CodeableConcept]] = None
    severity: Optional[CodeableConcept] = None
    code: Optional[CodeableConcept] = None
    bodySite: Optional[List[CodeableConcept]] = None
    subject: Reference
    encounter: Optional[Reference] = None
    onsetDateTime: Optional[str] = None
    onsetAge: Optional[dict] = None
    onsetPeriod: Optional[Period] = None
    onsetRange: Optional[dict] = None
    onsetString: Optional[str] = None
    abatementDateTime: Optional[str] = None
    abatementAge: Optional[dict] = None
    abatementPeriod: Optional[Period] = None
    abatementRange: Optional[dict] = None
    abatementString: Optional[str] = None
    recordedDate: Optional[str] = None
    recorder: Optional[Reference] = None
    asserter: Optional[Reference] = None
    stage: Optional[List[ConditionStage]] = None
    evidence: Optional[List[ConditionEvidence]] = None
    note: Optional[List[Annotation]] = None

    @field_validator('resourceType')
    @classmethod
    def validate_resource_type(cls, v):
        if v != "Condition":
            raise ValueError('resourceType must be "Condition"')
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "resourceType": "Condition",
                "meta": {
                    "profile": [PROFILE_BR_CONDITION]
                },
                "clinicalStatus": {
                    "coding": [
                        {
                            "system": "http://terminology.hl7.org/CodeSystem/condition-clinical",
                            "code": "active",
                            "display": "Active"
                        }
                    ]
                },
                "verificationStatus": {
                    "coding": [
                        {
                            "system": "http://terminology.hl7.org/CodeSystem/condition-ver-status",
                            "code": "confirmed",
                            "display": "Confirmed"
                        }
                    ]
                },
                "category": [
                    {
                        "coding": [
                            {
                                "system": "http://terminology.hl7.org/CodeSystem/condition-category",
                                "code": "encounter-diagnosis",
                                "display": "Encounter Diagnosis"
                            }
                        ]
                    }
                ],
                "code": {
                    "coding": [
                        {
                            "system": SYSTEM_CID10,
                            "code": "J06.9",
                            "display": "Infecção aguda das vias aéreas superiores, não especificada"
                        }
                    ],
                    "text": "IVAS"
                },
                "subject": {
                    "reference": "Patient/123"
                },
                "encounter": {
                    "reference": "Encounter/456"
                },
                "onsetDateTime": "2024-01-15",
                "recordedDate": "2024-01-15T10:30:00-03:00"
            }
        }
