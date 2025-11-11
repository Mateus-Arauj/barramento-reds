"""
Schema para validação de recursos FHIR Observation
"""
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List, Dict, Any

from .base import Identifier, Meta, CodeableConcept, Quantity, Period, Reference, Annotation


class ObservationResource(BaseModel):
    """
    Recurso FHIR Observation (simplificado)
    """
    resourceType: str = Field(default="Observation")
    id: Optional[str] = None
    meta: Optional[Meta] = None
    identifier: Optional[List[Identifier]] = None
    status: str
    category: Optional[List[CodeableConcept]] = None
    code: CodeableConcept
    subject: Optional[Reference] = None
    effectiveDateTime: Optional[str] = None
    effectivePeriod: Optional[Period] = None
    issued: Optional[str] = None
    
    valueQuantity: Optional[Quantity] = None
    valueCodeableConcept: Optional[CodeableConcept] = None
    valueString: Optional[str] = None
    valueBoolean: Optional[bool] = None
    valueInteger: Optional[int] = None
    valueRange: Optional[Dict[str, Any]] = None
    valueRatio: Optional[Dict[str, Any]] = None
    valueSampledData: Optional[Dict[str, Any]] = None
    valueTime: Optional[str] = None
    valueDateTime: Optional[str] = None
    valuePeriod: Optional[Period] = None
    
    interpretation: Optional[List[CodeableConcept]] = None
    note: Optional[List[Annotation]] = None
    
    @field_validator('resourceType')
    @classmethod
    def validate_resource_type(cls, v):
        if v != "Observation":
            raise ValueError('resourceType must be "Observation"')
        return v
    
    @field_validator('status')
    @classmethod
    def validate_status(cls, v):
        valid_statuses = ['registered', 'preliminary', 'final', 'amended', 'corrected', 'cancelled', 'entered-in-error', 'unknown']
        if v not in valid_statuses:
            raise ValueError(f'status must be one of {valid_statuses}')
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "resourceType": "Observation",
                "status": "final",
                "code": {
                    "coding": [
                        {
                            "system": "http://loinc.org",
                            "code": "85354-9",
                            "display": "Blood pressure panel"
                        }
                    ],
                    "text": "Pressão Arterial"
                },
                "subject": {
                    "reference": "Patient/123"
                },
                "effectiveDateTime": "2024-01-15T10:30:00Z",
                "valueQuantity": {
                    "value": 120,
                    "unit": "mmHg",
                    "system": "http://unitsofmeasure.org",
                    "code": "mm[Hg]"
                }
            }
        }
