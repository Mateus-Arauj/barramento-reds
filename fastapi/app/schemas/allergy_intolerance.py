"""
Schema para validação de recursos FHIR AllergyIntolerance - Alergias e Reações Adversas (BR Core)
"""
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List

from .base import (
    Identifier, Meta, CodeableConcept, Reference, Annotation, Period,
    PROFILE_BR_ALLERGY
)


class AllergyIntoleranceReaction(BaseModel):
    """
    Reação alérgica/adversa
    """
    substance: Optional[CodeableConcept] = None
    manifestation: List[CodeableConcept]
    description: Optional[str] = None
    onset: Optional[str] = None
    severity: Optional[str] = None  # mild | moderate | severe
    exposureRoute: Optional[CodeableConcept] = None
    note: Optional[List[Annotation]] = None

    @field_validator('severity')
    @classmethod
    def validate_severity(cls, v):
        valid = ['mild', 'moderate', 'severe']
        if v and v not in valid:
            raise ValueError(f'severity must be one of {valid}')
        return v


class AllergyIntoleranceResource(BaseModel):
    """
    Recurso FHIR AllergyIntolerance - Alergias e Reações Adversas
    """
    resourceType: str = Field(default="AllergyIntolerance")
    id: Optional[str] = None
    meta: Optional[Meta] = None
    identifier: Optional[List[Identifier]] = None
    clinicalStatus: Optional[CodeableConcept] = None
    verificationStatus: Optional[CodeableConcept] = None
    type: Optional[str] = None  # allergy | intolerance
    category: Optional[List[str]] = None  # food | medication | environment | biologic
    criticality: Optional[str] = None  # low | high | unable-to-assess
    code: Optional[CodeableConcept] = None
    patient: Reference
    encounter: Optional[Reference] = None
    onsetDateTime: Optional[str] = None
    onsetAge: Optional[dict] = None
    onsetPeriod: Optional[Period] = None
    onsetRange: Optional[dict] = None
    onsetString: Optional[str] = None
    recordedDate: Optional[str] = None
    recorder: Optional[Reference] = None
    asserter: Optional[Reference] = None
    lastOccurrence: Optional[str] = None
    note: Optional[List[Annotation]] = None
    reaction: Optional[List[AllergyIntoleranceReaction]] = None

    @field_validator('resourceType')
    @classmethod
    def validate_resource_type(cls, v):
        if v != "AllergyIntolerance":
            raise ValueError('resourceType must be "AllergyIntolerance"')
        return v

    @field_validator('type')
    @classmethod
    def validate_type(cls, v):
        valid = ['allergy', 'intolerance']
        if v and v not in valid:
            raise ValueError(f'type must be one of {valid}')
        return v

    @field_validator('category')
    @classmethod
    def validate_category(cls, v):
        valid = ['food', 'medication', 'environment', 'biologic']
        if v:
            for cat in v:
                if cat not in valid:
                    raise ValueError(f'category must be one of {valid}')
        return v

    @field_validator('criticality')
    @classmethod
    def validate_criticality(cls, v):
        valid = ['low', 'high', 'unable-to-assess']
        if v and v not in valid:
            raise ValueError(f'criticality must be one of {valid}')
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "resourceType": "AllergyIntolerance",
                "meta": {
                    "profile": [PROFILE_BR_ALLERGY]
                },
                "clinicalStatus": {
                    "coding": [
                        {
                            "system": "http://terminology.hl7.org/CodeSystem/allergyintolerance-clinical",
                            "code": "active",
                            "display": "Active"
                        }
                    ]
                },
                "verificationStatus": {
                    "coding": [
                        {
                            "system": "http://terminology.hl7.org/CodeSystem/allergyintolerance-verification",
                            "code": "confirmed",
                            "display": "Confirmed"
                        }
                    ]
                },
                "type": "allergy",
                "category": ["medication"],
                "criticality": "high",
                "code": {
                    "coding": [
                        {
                            "system": "http://snomed.info/sct",
                            "code": "387458008",
                            "display": "Aspirin"
                        }
                    ],
                    "text": "Alergia a Aspirina"
                },
                "patient": {
                    "reference": "Patient/123"
                },
                "recordedDate": "2024-01-15",
                "reaction": [
                    {
                        "manifestation": [
                            {
                                "coding": [
                                    {
                                        "system": "http://snomed.info/sct",
                                        "code": "39579001",
                                        "display": "Anaphylaxis"
                                    }
                                ],
                                "text": "Anafilaxia"
                            }
                        ],
                        "severity": "severe"
                    }
                ]
            }
        }
