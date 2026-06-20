"""
Schema para validação de recursos FHIR Organization - BR Core (Estabelecimento de Saúde)
"""
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List

from .base import (
    Identifier, ContactPoint, Address, Meta, CodeableConcept, Reference,
    SYSTEM_CNES, SYSTEM_CNPJ, PROFILE_BR_ORGANIZATION
)


class OrganizationContact(BaseModel):
    """
    Contato da organização
    """
    purpose: Optional[CodeableConcept] = None
    name: Optional[dict] = None
    telecom: Optional[List[ContactPoint]] = None
    address: Optional[Address] = None


class OrganizationResource(BaseModel):
    """
    Recurso FHIR Organization conforme BR Core
    Representa estabelecimentos de saúde (hospitais, UBS, clínicas)
    """
    resourceType: str = Field(default="Organization")
    id: Optional[str] = None
    meta: Optional[Meta] = None
    identifier: Optional[List[Identifier]] = None
    active: Optional[bool] = None
    type: Optional[List[CodeableConcept]] = None
    name: Optional[str] = None
    alias: Optional[List[str]] = None
    telecom: Optional[List[ContactPoint]] = None
    address: Optional[List[Address]] = None
    partOf: Optional[Reference] = None
    contact: Optional[List[OrganizationContact]] = None
    endpoint: Optional[List[Reference]] = None

    @field_validator('resourceType')
    @classmethod
    def validate_resource_type(cls, v):
        if v != "Organization":
            raise ValueError('resourceType must be "Organization"')
        return v

    @field_validator('identifier')
    @classmethod
    def validate_identifiers(cls, v):
        if v:
            for identifier in v:
                if identifier.system and identifier.value:
                    if 'cnpj' in identifier.system.lower():
                        cnpj = identifier.value.replace(".", "").replace("/", "").replace("-", "")
                        if len(cnpj) != 14 or not cnpj.isdigit():
                            raise ValueError(f'CNPJ inválido: {identifier.value}')
                    elif 'cnes' in identifier.system.lower():
                        cnes = identifier.value.replace(" ", "")
                        if len(cnes) != 7 or not cnes.isdigit():
                            raise ValueError(f'CNES inválido: {identifier.value}')
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "resourceType": "Organization",
                "meta": {
                    "profile": [PROFILE_BR_ORGANIZATION]
                },
                "identifier": [
                    {
                        "system": SYSTEM_CNES,
                        "value": "1234567"
                    },
                    {
                        "system": SYSTEM_CNPJ,
                        "value": "12345678000190"
                    }
                ],
                "active": True,
                "type": [
                    {
                        "coding": [
                            {
                                "system": "http://www.saude.gov.br/fhir/r4/CodeSystem/BRTipoEstabelecimentoSaude",
                                "code": "1",
                                "display": "Hospital Geral"
                            }
                        ],
                        "text": "Hospital Geral"
                    }
                ],
                "name": "Hospital Municipal de São Paulo",
                "telecom": [
                    {"system": "phone", "value": "(11) 3333-4444", "use": "work"}
                ],
                "address": [
                    {
                        "use": "work",
                        "line": ["Av. Paulista, 1000"],
                        "city": "São Paulo",
                        "state": "SP",
                        "postalCode": "01311-100",
                        "country": "BR"
                    }
                ]
            }
        }
