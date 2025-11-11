"""
Schema para validação de recursos FHIR Patient
"""
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime

from .base import Identifier, HumanName, ContactPoint, Address, Meta


class PatientResource(BaseModel):
    """
    Recurso FHIR Patient (simplificado)
    """
    resourceType: str = Field(default="Patient")
    id: Optional[str] = None
    meta: Optional[Meta] = None
    identifier: Optional[List[Identifier]] = None
    active: Optional[bool] = None
    name: Optional[List[HumanName]] = None
    telecom: Optional[List[ContactPoint]] = None
    gender: Optional[str] = None
    birthDate: Optional[str] = None
    address: Optional[List[Address]] = None
    
    @field_validator('resourceType')
    @classmethod
    def validate_resource_type(cls, v):
        if v != "Patient":
            raise ValueError('resourceType must be "Patient"')
        return v
    
    @field_validator('gender')
    @classmethod
    def validate_gender(cls, v):
        if v and v not in ['male', 'female', 'other', 'unknown']:
            raise ValueError('gender must be male, female, other or unknown')
        return v
    
    @field_validator('birthDate')
    @classmethod
    def validate_birth_date(cls, v):
        if v:
            try:
                datetime.strptime(v, '%Y-%m-%d')
            except ValueError:
                raise ValueError('birthDate must be in YYYY-MM-DD format')
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "resourceType": "Patient",
                "identifier": [
                    {"system": "http://hospital.example.org/patients", "value": "12345"}
                ],
                "active": True,
                "name": [
                    {
                        "use": "official",
                        "family": "Silva",
                        "given": ["João", "Carlos"]
                    }
                ],
                "gender": "male",
                "birthDate": "1980-05-15"
            }
        }
