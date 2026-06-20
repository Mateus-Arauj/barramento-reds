"""
Schema para validação de recursos FHIR DiagnosticReport - Laudo Diagnóstico (BR Core)
"""
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List

from .base import (
    Identifier, Meta, CodeableConcept, Reference, Period, Attachment,
    SYSTEM_LOINC, PROFILE_BR_DIAGNOSTIC_REPORT
)


class DiagnosticReportMedia(BaseModel):
    """
    Mídia associada ao laudo (imagens, etc.)
    """
    comment: Optional[str] = None
    link: Reference


class DiagnosticReportResource(BaseModel):
    """
    Recurso FHIR DiagnosticReport - Laudo Diagnóstico
    Representa laudos laboratoriais, de imagem, etc.
    """
    resourceType: str = Field(default="DiagnosticReport")
    id: Optional[str] = None
    meta: Optional[Meta] = None
    identifier: Optional[List[Identifier]] = None
    basedOn: Optional[List[Reference]] = None
    status: str
    category: Optional[List[CodeableConcept]] = None
    code: CodeableConcept
    subject: Optional[Reference] = None
    encounter: Optional[Reference] = None
    effectiveDateTime: Optional[str] = None
    effectivePeriod: Optional[Period] = None
    issued: Optional[str] = None
    performer: Optional[List[Reference]] = None
    resultsInterpreter: Optional[List[Reference]] = None
    specimen: Optional[List[Reference]] = None
    result: Optional[List[Reference]] = None
    imagingStudy: Optional[List[Reference]] = None
    media: Optional[List[DiagnosticReportMedia]] = None
    conclusion: Optional[str] = None
    conclusionCode: Optional[List[CodeableConcept]] = None
    presentedForm: Optional[List[Attachment]] = None

    @field_validator('resourceType')
    @classmethod
    def validate_resource_type(cls, v):
        if v != "DiagnosticReport":
            raise ValueError('resourceType must be "DiagnosticReport"')
        return v

    @field_validator('status')
    @classmethod
    def validate_status(cls, v):
        valid_statuses = [
            'registered', 'partial', 'preliminary', 'final',
            'amended', 'corrected', 'appended', 'cancelled',
            'entered-in-error', 'unknown'
        ]
        if v not in valid_statuses:
            raise ValueError(f'status must be one of {valid_statuses}')
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "resourceType": "DiagnosticReport",
                "meta": {
                    "profile": [PROFILE_BR_DIAGNOSTIC_REPORT]
                },
                "status": "final",
                "category": [
                    {
                        "coding": [
                            {
                                "system": "http://terminology.hl7.org/CodeSystem/v2-0074",
                                "code": "LAB",
                                "display": "Laboratory"
                            }
                        ],
                        "text": "Laboratório"
                    }
                ],
                "code": {
                    "coding": [
                        {
                            "system": SYSTEM_LOINC,
                            "code": "58410-2",
                            "display": "Complete blood count (CBC) panel"
                        }
                    ],
                    "text": "Hemograma Completo"
                },
                "subject": {
                    "reference": "Patient/123"
                },
                "encounter": {
                    "reference": "Encounter/456"
                },
                "effectiveDateTime": "2024-01-15T08:00:00-03:00",
                "issued": "2024-01-15T14:00:00-03:00",
                "performer": [
                    {
                        "reference": "Organization/lab-001",
                        "display": "Laboratório Central"
                    }
                ],
                "result": [
                    {"reference": "Observation/hgb-001"},
                    {"reference": "Observation/wbc-001"},
                    {"reference": "Observation/plt-001"}
                ],
                "conclusion": "Hemograma dentro dos valores de referência"
            }
        }
