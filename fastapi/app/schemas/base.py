"""
Schemas base para tipos FHIR comuns
"""
from pydantic import BaseModel, field_validator
from typing import Optional, List, Dict, Any


class Identifier(BaseModel):
    """
    Identificador FHIR
    """
    system: Optional[str] = None
    value: Optional[str] = None
    use: Optional[str] = None
    type: Optional[Dict[str, Any]] = None


class HumanName(BaseModel):
    """
    Nome humano FHIR
    """
    use: Optional[str] = None
    text: Optional[str] = None
    family: Optional[str] = None
    given: Optional[List[str]] = None
    prefix: Optional[List[str]] = None
    suffix: Optional[List[str]] = None


class ContactPoint(BaseModel):
    """
    Ponto de contato FHIR
    """
    system: Optional[str] = None
    value: Optional[str] = None
    use: Optional[str] = None


class Address(BaseModel):
    """
    Endereço FHIR adaptado para Brasil
    """
    use: Optional[str] = None
    type: Optional[str] = None
    text: Optional[str] = None
    line: Optional[List[str]] = None
    city: Optional[str] = None
    district: Optional[str] = None
    state: Optional[str] = None
    postalCode: Optional[str] = None
    country: Optional[str] = "BR"

    @field_validator('postalCode')
    @classmethod
    def validate_cep(cls, v):
        if v:
            clean = v.replace("-", "").replace(".", "")
            if len(clean) != 8 or not clean.isdigit():
                raise ValueError('CEP deve ter 8 dígitos')
        return v


class Meta(BaseModel):
    """
    Metadados FHIR
    """
    versionId: Optional[str] = None
    lastUpdated: Optional[str] = None
    source: Optional[str] = None
    profile: Optional[List[str]] = None
    security: Optional[List[Dict]] = None
    tag: Optional[List[Dict]] = None


class CodeableConcept(BaseModel):
    """
    Conceito codificável FHIR
    """
    coding: Optional[List[Dict[str, Any]]] = None
    text: Optional[str] = None


class Quantity(BaseModel):
    """
    Quantidade FHIR
    """
    value: Optional[float] = None
    unit: Optional[str] = None
    system: Optional[str] = None
    code: Optional[str] = None


class Period(BaseModel):
    """
    Período FHIR
    """
    start: Optional[str] = None
    end: Optional[str] = None


class Reference(BaseModel):
    """
    Referência FHIR
    """
    reference: Optional[str] = None
    display: Optional[str] = None


class Annotation(BaseModel):
    """
    Anotação FHIR
    """
    text: str
    authorString: Optional[str] = None
    time: Optional[str] = None


class Coding(BaseModel):
    """
    Codificação FHIR - representa um código de um sistema de terminologia
    """
    system: Optional[str] = None
    version: Optional[str] = None
    code: Optional[str] = None
    display: Optional[str] = None
    userSelected: Optional[bool] = None


class Duration(BaseModel):
    """
    Duração FHIR - quantidade de tempo
    """
    value: Optional[float] = None
    comparator: Optional[str] = None
    unit: Optional[str] = None
    system: Optional[str] = None
    code: Optional[str] = None


class Attachment(BaseModel):
    """
    Anexo FHIR - conteúdo binário referenciado
    """
    contentType: Optional[str] = None
    language: Optional[str] = None
    data: Optional[str] = None
    url: Optional[str] = None
    size: Optional[int] = None
    hash: Optional[str] = None
    title: Optional[str] = None
    creation: Optional[str] = None
