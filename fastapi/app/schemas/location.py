"""
Schema para validação de recursos FHIR Location - Local de Atendimento
"""
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List

from .base import (
    Identifier, ContactPoint, Address, Meta, CodeableConcept, Reference, Coding,
    PROFILE_BR_LOCATION
)


class LocationPosition(BaseModel):
    """
    Coordenadas geográficas do local
    """
    longitude: float
    latitude: float
    altitude: Optional[float] = None


class LocationHoursOfOperation(BaseModel):
    """
    Horário de funcionamento
    """
    daysOfWeek: Optional[List[str]] = None
    allDay: Optional[bool] = None
    openingTime: Optional[str] = None
    closingTime: Optional[str] = None


class LocationResource(BaseModel):
    """
    Recurso FHIR Location - Local de Atendimento
    """
    resourceType: str = Field(default="Location")
    id: Optional[str] = None
    meta: Optional[Meta] = None
    identifier: Optional[List[Identifier]] = None
    status: Optional[str] = None
    operationalStatus: Optional[Coding] = None
    name: Optional[str] = None
    alias: Optional[List[str]] = None
    description: Optional[str] = None
    mode: Optional[str] = None
    type: Optional[List[CodeableConcept]] = None
    telecom: Optional[List[ContactPoint]] = None
    address: Optional[Address] = None
    physicalType: Optional[CodeableConcept] = None
    position: Optional[LocationPosition] = None
    managingOrganization: Optional[Reference] = None
    partOf: Optional[Reference] = None
    hoursOfOperation: Optional[List[LocationHoursOfOperation]] = None
    availabilityExceptions: Optional[str] = None
    endpoint: Optional[List[Reference]] = None

    @field_validator('resourceType')
    @classmethod
    def validate_resource_type(cls, v):
        if v != "Location":
            raise ValueError('resourceType must be "Location"')
        return v

    @field_validator('status')
    @classmethod
    def validate_status(cls, v):
        valid_statuses = ['active', 'suspended', 'inactive']
        if v and v not in valid_statuses:
            raise ValueError(f'status must be one of {valid_statuses}')
        return v

    @field_validator('mode')
    @classmethod
    def validate_mode(cls, v):
        valid_modes = ['instance', 'kind']
        if v and v not in valid_modes:
            raise ValueError(f'mode must be one of {valid_modes}')
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "resourceType": "Location",
                "meta": {
                    "profile": [PROFILE_BR_LOCATION]
                },
                "status": "active",
                "name": "Sala de Consulta 01 - UBS Centro",
                "description": "Consultório médico para atendimento ambulatorial",
                "mode": "instance",
                "type": [
                    {
                        "coding": [
                            {
                                "system": "http://terminology.hl7.org/CodeSystem/v3-RoleCode",
                                "code": "AMB",
                                "display": "Ambulatory"
                            }
                        ],
                        "text": "Ambulatório"
                    }
                ],
                "telecom": [
                    {"system": "phone", "value": "(11) 3333-5555", "use": "work"}
                ],
                "address": {
                    "use": "work",
                    "line": ["Rua da Saúde, 200 - Sala 101"],
                    "city": "São Paulo",
                    "state": "SP",
                    "postalCode": "01000-000",
                    "country": "BR"
                },
                "physicalType": {
                    "coding": [
                        {
                            "system": "http://terminology.hl7.org/CodeSystem/location-physical-type",
                            "code": "ro",
                            "display": "Room"
                        }
                    ],
                    "text": "Sala"
                },
                "managingOrganization": {
                    "reference": "Organization/123",
                    "display": "UBS Centro"
                }
            }
        }
