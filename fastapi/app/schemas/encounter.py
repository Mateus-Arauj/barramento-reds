"""
Schema para validação de recursos FHIR Encounter - BR Core
"""
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List

from .base import (
    Identifier, Meta, CodeableConcept, Period, Reference, Coding, Duration,
    SYSTEM_TUSS, SYSTEM_SIGTAP
)


class EncounterStatusHistory(BaseModel):
    """
    Histórico de status do encontro
    """
    status: str
    period: Period


class EncounterClassHistory(BaseModel):
    """
    Histórico de classes do encontro
    """
    class_: Coding = Field(..., alias="class")
    period: Period

    class Config:
        populate_by_name = True


class EncounterParticipant(BaseModel):
    """
    Participante do encontro (profissionais de saúde)
    """
    type: Optional[List[CodeableConcept]] = None
    period: Optional[Period] = None
    individual: Optional[Reference] = None


class EncounterDiagnosis(BaseModel):
    """
    Diagnóstico associado ao encontro
    """
    condition: Reference
    use: Optional[CodeableConcept] = None
    rank: Optional[int] = None


class EncounterHospitalization(BaseModel):
    """
    Detalhes de hospitalização
    """
    preAdmissionIdentifier: Optional[Identifier] = None
    origin: Optional[Reference] = None
    admitSource: Optional[CodeableConcept] = None
    reAdmission: Optional[CodeableConcept] = None
    dietPreference: Optional[List[CodeableConcept]] = None
    specialCourtesy: Optional[List[CodeableConcept]] = None
    specialArrangement: Optional[List[CodeableConcept]] = None
    destination: Optional[Reference] = None
    dischargeDisposition: Optional[CodeableConcept] = None


class EncounterLocation(BaseModel):
    """
    Localização do encontro
    """
    location: Reference
    status: Optional[str] = None
    physicalType: Optional[CodeableConcept] = None
    period: Optional[Period] = None

    @field_validator('status')
    @classmethod
    def validate_location_status(cls, v):
        valid_statuses = ['planned', 'active', 'reserved', 'completed']
        if v and v not in valid_statuses:
            raise ValueError(f'location status must be one of {valid_statuses}')
        return v


class EncounterResource(BaseModel):
    """
    Recurso FHIR Encounter - Encontro/Atendimento médico
    """
    resourceType: str = Field(default="Encounter")
    id: Optional[str] = None
    meta: Optional[Meta] = None
    identifier: Optional[List[Identifier]] = None
    status: str
    statusHistory: Optional[List[EncounterStatusHistory]] = None
    class_: Coding = Field(..., alias="class")
    classHistory: Optional[List[EncounterClassHistory]] = None
    type: Optional[List[CodeableConcept]] = None
    serviceType: Optional[CodeableConcept] = None
    priority: Optional[CodeableConcept] = None
    subject: Optional[Reference] = None
    episodeOfCare: Optional[List[Reference]] = None
    basedOn: Optional[List[Reference]] = None
    participant: Optional[List[EncounterParticipant]] = None
    appointment: Optional[List[Reference]] = None
    period: Optional[Period] = None
    length: Optional[Duration] = None
    reasonCode: Optional[List[CodeableConcept]] = None
    reasonReference: Optional[List[Reference]] = None
    diagnosis: Optional[List[EncounterDiagnosis]] = None
    account: Optional[List[Reference]] = None
    hospitalization: Optional[EncounterHospitalization] = None
    location: Optional[List[EncounterLocation]] = None
    serviceProvider: Optional[Reference] = None
    partOf: Optional[Reference] = None

    @field_validator('resourceType')
    @classmethod
    def validate_resource_type(cls, v):
        if v != "Encounter":
            raise ValueError('resourceType must be "Encounter"')
        return v

    @field_validator('status')
    @classmethod
    def validate_status(cls, v):
        valid_statuses = [
            'planned', 'arrived', 'triaged', 'in-progress',
            'onleave', 'finished', 'cancelled', 'entered-in-error', 'unknown'
        ]
        if v not in valid_statuses:
            raise ValueError(f'status must be one of {valid_statuses}')
        return v

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "resourceType": "Encounter",
                "status": "finished",
                "class": {
                    "system": "http://terminology.hl7.org/CodeSystem/v3-ActCode",
                    "code": "AMB",
                    "display": "ambulatory"
                },
                "type": [
                    {
                        "coding": [
                            {
                                "system": SYSTEM_TUSS,
                                "code": "10101012",
                                "display": "Consulta em consultório"
                            }
                        ],
                        "text": "Consulta ambulatorial"
                    }
                ],
                "serviceType": {
                    "coding": [
                        {
                            "system": SYSTEM_SIGTAP,
                            "code": "0301010072",
                            "display": "Consulta médica em atenção básica"
                        }
                    ]
                },
                "subject": {
                    "reference": "Patient/123"
                },
                "participant": [
                    {
                        "individual": {
                            "reference": "Practitioner/456",
                            "display": "Dra. Maria Helena Santos"
                        }
                    }
                ],
                "period": {
                    "start": "2024-01-15T09:00:00-03:00",
                    "end": "2024-01-15T09:30:00-03:00"
                },
                "reasonCode": [
                    {
                        "coding": [
                            {
                                "system": "http://hl7.org/fhir/sid/icd-10",
                                "code": "R50.9",
                                "display": "Febre não especificada"
                            }
                        ],
                        "text": "Febre"
                    }
                ]
            }
        }

