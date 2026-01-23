"""
Schema para validação de recursos FHIR Patient - BR Core
"""
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime

from .base import (
    Identifier, HumanName, ContactPoint, Address, Meta, CodeableConcept,
    SYSTEM_CPF, SYSTEM_CNS
)


def validate_cpf(cpf: str) -> bool:
    """
    Valida CPF brasileiro (11 dígitos com dígitos verificadores)
    """
    cpf = cpf.replace(".", "").replace("-", "")
    if len(cpf) != 11 or not cpf.isdigit():
        return False
    if cpf == cpf[0] * 11:
        return False

    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    resto = soma % 11
    digito1 = 0 if resto < 2 else 11 - resto

    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    resto = soma % 11
    digito2 = 0 if resto < 2 else 11 - resto

    return cpf[-2:] == f"{digito1}{digito2}"


def validate_cns(cns: str) -> bool:
    """
    Valida CNS brasileiro (15 dígitos)
    """
    cns = cns.replace(" ", "").replace(".", "").replace("-", "")
    if len(cns) != 15 or not cns.isdigit():
        return False
    return True


class PatientResource(BaseModel):
    """
    Recurso FHIR Patient conforme BR Core
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
    nationality: Optional[CodeableConcept] = None
    motherName: Optional[str] = None

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

    @field_validator('identifier')
    @classmethod
    def validate_brazilian_identifiers(cls, v):
        if v:
            for identifier in v:
                if identifier.system and identifier.value:
                    if 'cpf' in identifier.system.lower():
                        if not validate_cpf(identifier.value):
                            raise ValueError(f'CPF inválido: {identifier.value}')
                    elif 'cns' in identifier.system.lower():
                        if not validate_cns(identifier.value):
                            raise ValueError(f'CNS inválido: {identifier.value}')
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "resourceType": "Patient",
                "identifier": [
                    {
                        "system": SYSTEM_CPF,
                        "value": "12345678909"
                    },
                    {
                        "system": SYSTEM_CNS,
                        "value": "123456789012345"
                    }
                ],
                "active": True,
                "name": [
                    {
                        "use": "official",
                        "family": "Silva",
                        "given": ["João", "Carlos"]
                    }
                ],
                "telecom": [
                    {"system": "phone", "value": "(11) 99999-9999", "use": "mobile"}
                ],
                "gender": "male",
                "birthDate": "1980-05-15",
                "address": [
                    {
                        "use": "home",
                        "line": ["Rua das Flores, 123"],
                        "city": "São Paulo",
                        "state": "SP",
                        "postalCode": "01234-567",
                        "country": "BR"
                    }
                ],
                "motherName": "Maria da Silva"
            }
        }
