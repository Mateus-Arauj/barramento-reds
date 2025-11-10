"""
Validadores para recursos FHIR usando Pydantic
"""
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List, Any, Dict
from datetime import datetime


class Identifier(BaseModel):
    """Identificador FHIR"""
    system: Optional[str] = None
    value: Optional[str] = None
    use: Optional[str] = None


class HumanName(BaseModel):
    """Nome humano FHIR"""
    use: Optional[str] = None
    text: Optional[str] = None
    family: Optional[str] = None
    given: Optional[List[str]] = None
    prefix: Optional[List[str]] = None
    suffix: Optional[List[str]] = None


class ContactPoint(BaseModel):
    """Ponto de contato FHIR"""
    system: Optional[str] = None  # phone | fax | email | pager | url | sms | other
    value: Optional[str] = None
    use: Optional[str] = None  # home | work | temp | old | mobile


class Address(BaseModel):
    """Endereço FHIR"""
    use: Optional[str] = None  # home | work | temp | old | billing
    type: Optional[str] = None  # postal | physical | both
    text: Optional[str] = None
    line: Optional[List[str]] = None
    city: Optional[str] = None
    district: Optional[str] = None
    state: Optional[str] = None
    postalCode: Optional[str] = None
    country: Optional[str] = None


class Meta(BaseModel):
    """Metadados FHIR"""
    versionId: Optional[str] = None
    lastUpdated: Optional[str] = None
    source: Optional[str] = None
    profile: Optional[List[str]] = None
    security: Optional[List[Dict]] = None
    tag: Optional[List[Dict]] = None


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
    gender: Optional[str] = None  # male | female | other | unknown
    birthDate: Optional[str] = None  # YYYY-MM-DD
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


class CodeableConcept(BaseModel):
    """Conceito codificável FHIR"""
    coding: Optional[List[Dict[str, Any]]] = None
    text: Optional[str] = None


class Quantity(BaseModel):
    """Quantidade FHIR"""
    value: Optional[float] = None
    unit: Optional[str] = None
    system: Optional[str] = None
    code: Optional[str] = None


class Period(BaseModel):
    """Período FHIR"""
    start: Optional[str] = None
    end: Optional[str] = None


class Reference(BaseModel):
    """Referência FHIR"""
    reference: Optional[str] = None
    display: Optional[str] = None


class Annotation(BaseModel):
    """Anotação FHIR"""
    text: str
    authorString: Optional[str] = None
    time: Optional[str] = None


class ObservationResource(BaseModel):
    """
    Recurso FHIR Observation (simplificado)
    """
    resourceType: str = Field(default="Observation")
    id: Optional[str] = None
    meta: Optional[Meta] = None
    identifier: Optional[List[Identifier]] = None
    status: str  # registered | preliminary | final | amended | corrected | cancelled
    category: Optional[List[CodeableConcept]] = None
    code: CodeableConcept  # Tipo de observação (obrigatório)
    subject: Optional[Reference] = None  # Referência ao paciente
    effectiveDateTime: Optional[str] = None
    effectivePeriod: Optional[Period] = None
    issued: Optional[str] = None
    
    # Valor da observação (apenas um deve ser usado)
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
