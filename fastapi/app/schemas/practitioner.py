"""
Schema para validação de recursos FHIR Practitioner - BR Core
"""
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List

from .base import (
    Identifier, HumanName, ContactPoint, Address, Meta, 
    CodeableConcept, Period, Reference, Attachment,
    SYSTEM_CRM_PREFIX, SYSTEM_COREN_PREFIX, SYSTEM_CBO
)


UF_BRAZIL = [
    "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA",
    "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN",
    "RS", "RO", "RR", "SC", "SP", "SE", "TO"
]


class PractitionerQualification(BaseModel):
    """
    Qualificação do profissional de saúde (especialidades, CBO)
    """
    identifier: Optional[List[Identifier]] = None
    code: CodeableConcept
    period: Optional[Period] = None
    issuer: Optional[Reference] = None


class PractitionerResource(BaseModel):
    """
    Recurso FHIR Practitioner conforme BR Core
    """
    resourceType: str = Field(default="Practitioner")
    id: Optional[str] = None
    meta: Optional[Meta] = None
    identifier: Optional[List[Identifier]] = None
    active: Optional[bool] = None
    name: Optional[List[HumanName]] = None
    telecom: Optional[List[ContactPoint]] = None
    address: Optional[List[Address]] = None
    gender: Optional[str] = None
    birthDate: Optional[str] = None
    photo: Optional[List[Attachment]] = None
    qualification: Optional[List[PractitionerQualification]] = None
    communication: Optional[List[CodeableConcept]] = None

    @field_validator('resourceType')
    @classmethod
    def validate_resource_type(cls, v):
        if v != "Practitioner":
            raise ValueError('resourceType must be "Practitioner"')
        return v

    @field_validator('gender')
    @classmethod
    def validate_gender(cls, v):
        if v and v not in ['male', 'female', 'other', 'unknown']:
            raise ValueError('gender must be male, female, other or unknown')
        return v

    @field_validator('identifier')
    @classmethod
    def validate_professional_identifiers(cls, v):
        if v:
            for identifier in v:
                if identifier.system and identifier.value:
                    system_lower = identifier.system.lower()
                    if 'crm' in system_lower or 'coren' in system_lower or 'cro' in system_lower:
                        if not identifier.value.replace("-", "").replace(".", "").isdigit():
                            raise ValueError(f'Número de registro profissional inválido: {identifier.value}')
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "resourceType": "Practitioner",
                "identifier": [
                    {
                        "system": f"{SYSTEM_CRM_PREFIX}sp",
                        "value": "123456"
                    }
                ],
                "active": True,
                "name": [
                    {
                        "use": "official",
                        "family": "Santos",
                        "given": ["Maria", "Helena"],
                        "prefix": ["Dra."]
                    }
                ],
                "telecom": [
                    {"system": "phone", "value": "(11) 99999-9999", "use": "work"},
                    {"system": "email", "value": "dra.maria@hospital.com.br", "use": "work"}
                ],
                "gender": "female",
                "birthDate": "1975-03-20",
                "qualification": [
                    {
                        "code": {
                            "coding": [
                                {
                                    "system": SYSTEM_CBO,
                                    "code": "225125",
                                    "display": "Médico clínico"
                                }
                            ],
                            "text": "Médica Clínica"
                        },
                        "issuer": {
                            "display": "Conselho Regional de Medicina de São Paulo"
                        }
                    }
                ]
            }
        }
