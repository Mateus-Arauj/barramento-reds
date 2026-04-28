"""
Schemas base para tipos FHIR comuns - Adaptado para FHIR BR Core
Referência: http://www.saude.gov.br/fhir/r4/
"""
from pydantic import BaseModel, field_validator
from typing import Optional, List, Dict, Any


# ===========================================================================
# Constantes de sistemas de identificação brasileiros (BR Core)
# ===========================================================================

# Identificadores de pacientes
SYSTEM_CPF = "http://www.saude.gov.br/fhir/r4/StructureDefinition/BRIndividuo-1.0/BRDocumentoIndividuo-CPF"
SYSTEM_CNS = "http://www.saude.gov.br/fhir/r4/StructureDefinition/BRIndividuo-1.0/BRDocumentoIndividuo-CNS"
SYSTEM_RG = "http://www.saude.gov.br/fhir/r4/StructureDefinition/BRIndividuo-1.0/BRDocumentoIndividuo-RG"

# Conselhos profissionais (sufixo = UF em minúsculo, ex: crm-sp)
SYSTEM_CRM_PREFIX = "http://www.saude.gov.br/fhir/r4/NamingSystem/crm-"
SYSTEM_COREN_PREFIX = "http://www.saude.gov.br/fhir/r4/NamingSystem/coren-"
SYSTEM_CRO_PREFIX = "http://www.saude.gov.br/fhir/r4/NamingSystem/cro-"
SYSTEM_CRF_PREFIX = "http://www.saude.gov.br/fhir/r4/NamingSystem/crf-"
SYSTEM_CREFITO_PREFIX = "http://www.saude.gov.br/fhir/r4/NamingSystem/crefito-"
SYSTEM_CRP_PREFIX = "http://www.saude.gov.br/fhir/r4/NamingSystem/crp-"

# Classificações e terminologias brasileiras
SYSTEM_CBO = "http://www.saude.gov.br/fhir/r4/CodeSystem/BRCBO"
SYSTEM_TUSS = "http://www.ans.gov.br/fhir/tuss"
SYSTEM_SIGTAP = "http://www.saude.gov.br/fhir/r4/CodeSystem/BRProcedimentosNacionais"
SYSTEM_IBGE = "http://www.saude.gov.br/fhir/r4/CodeSystem/BRDivisaoGeograficaBrasil"
SYSTEM_CNES = "http://www.saude.gov.br/fhir/r4/NamingSystem/cnes"
SYSTEM_CNPJ = "http://www.saude.gov.br/fhir/r4/StructureDefinition/BREstabelecimentoSaude-1.0/CNPJ"

# CID-10 (Classificação Internacional de Doenças)
SYSTEM_CID10 = "http://hl7.org/fhir/sid/icd-10"
SYSTEM_CIAP2 = "http://hl7.org/fhir/sid/icpc-2"

# Sistemas internacionais comuns no contexto brasileiro
SYSTEM_LOINC = "http://loinc.org"
SYSTEM_SNOMED = "http://snomed.info/sct"
SYSTEM_UCUM = "http://unitsofmeasure.org"
SYSTEM_ATC = "http://www.whocc.no/atc"
SYSTEM_ANVISA = "http://www.saude.gov.br/fhir/r4/CodeSystem/BRMedicamento"

# Perfis BR Core
PROFILE_BR_PATIENT = "http://www.saude.gov.br/fhir/r4/StructureDefinition/BRIndividuo-1.0"
PROFILE_BR_PRACTITIONER = "http://www.saude.gov.br/fhir/r4/StructureDefinition/BRProfissional-1.0"
PROFILE_BR_ORGANIZATION = "http://www.saude.gov.br/fhir/r4/StructureDefinition/BREstabelecimentoSaude-1.0"
PROFILE_BR_ENCOUNTER = "http://www.saude.gov.br/fhir/r4/StructureDefinition/BRContatoAssistencial-1.0"
PROFILE_BR_OBSERVATION = "http://www.saude.gov.br/fhir/r4/StructureDefinition/BRObservacao-1.0"
PROFILE_BR_CONDITION = "http://www.saude.gov.br/fhir/r4/StructureDefinition/BRDiagnostico-1.0"
PROFILE_BR_PROCEDURE = "http://www.saude.gov.br/fhir/r4/StructureDefinition/BRProcedimentoRealizado-1.0"
PROFILE_BR_MEDICATION_REQUEST = "http://www.saude.gov.br/fhir/r4/StructureDefinition/BRPrescricaoMedicamento-1.0"
PROFILE_BR_IMMUNIZATION = "http://www.saude.gov.br/fhir/r4/StructureDefinition/BRImunobiologicoAdministrado-1.0"
PROFILE_BR_ALLERGY = "http://www.saude.gov.br/fhir/r4/StructureDefinition/BRAlergiasReacoesAdversas-1.0"
PROFILE_BR_DIAGNOSTIC_REPORT = "http://www.saude.gov.br/fhir/r4/StructureDefinition/BRDiagnosticoLaboratorioClinico-1.0"
PROFILE_BR_LOCATION = "http://www.saude.gov.br/fhir/r4/StructureDefinition/BRLocalAtendimento-1.0"

# UFs brasileiras
UF_BRAZIL = [
    "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA",
    "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN",
    "RS", "RO", "RR", "SC", "SP", "SE", "TO"
]


# ===========================================================================
# Tipos de dados FHIR base
# ===========================================================================

class Identifier(BaseModel):
    """
    Identificador FHIR - adaptado para documentos brasileiros
    """
    system: Optional[str] = None
    value: Optional[str] = None
    use: Optional[str] = None
    type: Optional[Dict[str, Any]] = None
    period: Optional[Dict[str, Any]] = None
    assigner: Optional[Dict[str, Any]] = None


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
    rank: Optional[int] = None
    period: Optional[Dict[str, Any]] = None


class Address(BaseModel):
    """
    Endereço FHIR adaptado para Brasil (BR Core)
    Inclui código IBGE do município e campos de bairro
    """
    use: Optional[str] = None
    type: Optional[str] = None
    text: Optional[str] = None
    line: Optional[List[str]] = None
    city: Optional[str] = None
    cityCode: Optional[str] = None  # Código IBGE do município
    district: Optional[str] = None  # Bairro
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

    @field_validator('state')
    @classmethod
    def validate_state(cls, v):
        if v and v.upper() not in UF_BRAZIL and len(v) == 2:
            raise ValueError(f'UF inválida: {v}. Deve ser uma das: {", ".join(UF_BRAZIL)}')
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
    comparator: Optional[str] = None
    unit: Optional[str] = None
    system: Optional[str] = None
    code: Optional[str] = None


class Range(BaseModel):
    """
    Faixa de valores FHIR
    """
    low: Optional[Quantity] = None
    high: Optional[Quantity] = None


class Ratio(BaseModel):
    """
    Razão FHIR (numerador/denominador)
    """
    numerator: Optional[Quantity] = None
    denominator: Optional[Quantity] = None


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
    type: Optional[str] = None
    display: Optional[str] = None
    identifier: Optional[Dict[str, Any]] = None


class Annotation(BaseModel):
    """
    Anotação FHIR
    """
    text: str
    authorString: Optional[str] = None
    authorReference: Optional[Dict[str, Any]] = None
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


class Dosage(BaseModel):
    """
    Dosagem FHIR - instrução de dosagem de medicamento
    """
    sequence: Optional[int] = None
    text: Optional[str] = None
    timing: Optional[Dict[str, Any]] = None
    asNeededBoolean: Optional[bool] = None
    asNeededCodeableConcept: Optional[Dict[str, Any]] = None
    route: Optional[Dict[str, Any]] = None
    doseAndRate: Optional[List[Dict[str, Any]]] = None
    maxDosePerPeriod: Optional[Dict[str, Any]] = None
