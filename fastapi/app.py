"""
Mini HAPI - Servidor FHIR simplificado usando FastAPI
Implementa endpoints para Patient e Observation
"""
import os
from fastapi import FastAPI, Header, HTTPException, Depends, Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import Optional, List
from contextlib import asynccontextmanager

from database import init_db, get_db
from validators import PatientResource, ObservationResource
from services import PatientService, ObservationService

# Token de autenticação
API_TOKEN = os.getenv("API_TOKEN", "troque-essa-chave")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gerencia o ciclo de vida da aplicação
    Inicializa o banco de dados na startup
    """
    print("🚀 Iniciando Mini HAPI Server...")
    init_db()
    print("✓ Banco de dados inicializado")
    yield
    print("👋 Encerrando Mini HAPI Server...")


app = FastAPI(
    title="Mini HAPI - FHIR Server",
    description="Servidor FHIR simplificado com suporte a Patient e Observation",
    version="1.0.0",
    lifespan=lifespan
)


def check_auth(authorization: str | None = Header(default=None)):
    """
    Valida o token de autorização Bearer
    """
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing Bearer token")
    token = authorization.split(" ", 1)[1]
    if token != API_TOKEN:
        raise HTTPException(status_code=403, detail="Invalid token")
    return True


# ==================== Endpoints de Sistema ====================

@app.get("/health", tags=["System"])
async def health_check():
    """Verifica o status do servidor"""
    return {"status": "ok", "service": "Mini HAPI FHIR Server"}


@app.get("/metadata", tags=["System"])
async def get_metadata():
    """
    Retorna CapabilityStatement (simplificado)
    Documenta as capacidades do servidor FHIR
    """
    return {
        "resourceType": "CapabilityStatement",
        "status": "active",
        "date": "2024-01-15",
        "kind": "instance",
        "software": {
            "name": "Mini HAPI",
            "version": "1.0.0"
        },
        "implementation": {
            "description": "Servidor FHIR simplificado - TCC",
            "url": "http://localhost:8000/fhir"
        },
        "fhirVersion": "4.0.1",
        "format": ["application/fhir+json", "application/json"],
        "rest": [
            {
                "mode": "server",
                "resource": [
                    {
                        "type": "Patient",
                        "interaction": [
                            {"code": "read"},
                            {"code": "create"},
                            {"code": "update"},
                            {"code": "delete"},
                            {"code": "search-type"}
                        ],
                        "searchParam": [
                            {"name": "name", "type": "string"},
                            {"name": "gender", "type": "token"},
                            {"name": "birthdate", "type": "date"}
                        ]
                    },
                    {
                        "type": "Observation",
                        "interaction": [
                            {"code": "read"},
                            {"code": "create"},
                            {"code": "search-type"}
                        ],
                        "searchParam": [
                            {"name": "patient", "type": "reference"},
                            {"name": "status", "type": "token"},
                            {"name": "date", "type": "date"}
                        ]
                    }
                ]
            }
        ]
    }


# ==================== Endpoints Patient ====================

@app.post("/fhir/Patient", 
          response_model=None,
          status_code=201,
          tags=["Patient"])
async def create_patient(
    patient: PatientResource,
    db: Session = Depends(get_db),
    _auth: bool = Depends(check_auth)
):
    """
    Cria um novo recurso Patient
    
    - Valida a estrutura do recurso FHIR
    - Persiste no banco de dados PostgreSQL
    - Retorna o recurso criado com ID e metadados
    """
    db_patient = PatientService.create_patient(db, patient)
    return JSONResponse(
        status_code=201,
        content=db_patient.resource_json,
        headers={"Location": f"/fhir/Patient/{db_patient.id}"}
    )


@app.get("/fhir/Patient/{patient_id}",
         response_model=None,
         tags=["Patient"])
async def get_patient(
    patient_id: str,
    db: Session = Depends(get_db),
    _auth: bool = Depends(check_auth)
):
    """
    Recupera um recurso Patient por ID
    
    - Consulta o banco de dados
    - Reconstrói o recurso em formato JSON FHIR
    - Retorna 404 se não encontrado
    """
    db_patient = PatientService.get_patient(db, patient_id)
    return db_patient.resource_json


@app.put("/fhir/Patient/{patient_id}",
         response_model=None,
         tags=["Patient"])
async def update_patient(
    patient_id: str,
    patient: PatientResource,
    db: Session = Depends(get_db),
    _auth: bool = Depends(check_auth)
):
    """
    Atualiza um recurso Patient existente
    
    - Valida a estrutura do recurso
    - Atualiza no banco de dados
    - Incrementa versionId nos metadados
    """
    db_patient = PatientService.update_patient(db, patient_id, patient)
    return db_patient.resource_json


@app.delete("/fhir/Patient/{patient_id}",
            status_code=204,
            tags=["Patient"])
async def delete_patient(
    patient_id: str,
    db: Session = Depends(get_db),
    _auth: bool = Depends(check_auth)
):
    """
    Remove um recurso Patient
    
    - Deleta o paciente e suas observações associadas
    - Retorna 204 No Content em caso de sucesso
    """
    PatientService.delete_patient(db, patient_id)
    return None


@app.get("/fhir/Patient",
         response_model=None,
         tags=["Patient"])
async def search_patients(
    name: Optional[str] = Query(None, description="Busca por nome (family name)"),
    gender: Optional[str] = Query(None, description="Filtro por gênero"),
    birthdate: Optional[str] = Query(None, description="Filtro por data de nascimento"),
    _count: int = Query(50, alias="_count", description="Número máximo de resultados"),
    db: Session = Depends(get_db),
    _auth: bool = Depends(check_auth)
):
    """
    Busca recursos Patient com filtros
    
    Parâmetros de busca suportados:
    - name: nome do paciente
    - gender: gênero (male, female, other, unknown)
    - birthdate: data de nascimento (YYYY-MM-DD)
    - _count: limite de resultados (padrão: 50)
    """
    patients = PatientService.search_patients(
        db, 
        name=name, 
        gender=gender, 
        birthdate=birthdate,
        limit=_count
    )
    
    # Retorna Bundle FHIR
    return {
        "resourceType": "Bundle",
        "type": "searchset",
        "total": len(patients),
        "entry": [
            {
                "fullUrl": f"/fhir/Patient/{p.id}",
                "resource": p.resource_json
            }
            for p in patients
        ]
    }


# ==================== Endpoints Observation ====================

@app.post("/fhir/Observation",
          response_model=None,
          status_code=201,
          tags=["Observation"])
async def create_observation(
    observation: ObservationResource,
    db: Session = Depends(get_db),
    _auth: bool = Depends(check_auth)
):
    """
    Cria um novo recurso Observation
    
    - Valida a estrutura do recurso FHIR
    - Verifica se o Patient referenciado existe
    - Persiste no banco de dados PostgreSQL
    - Retorna o recurso criado com ID e metadados
    """
    db_observation = ObservationService.create_observation(db, observation)
    return JSONResponse(
        status_code=201,
        content=db_observation.resource_json,
        headers={"Location": f"/fhir/Observation/{db_observation.id}"}
    )


@app.get("/fhir/Observation/{observation_id}",
         response_model=None,
         tags=["Observation"])
async def get_observation(
    observation_id: str,
    db: Session = Depends(get_db),
    _auth: bool = Depends(check_auth)
):
    """
    Recupera um recurso Observation por ID
    
    - Consulta o banco de dados
    - Reconstrói o recurso em formato JSON FHIR
    - Retorna 404 se não encontrado
    """
    db_observation = ObservationService.get_observation(db, observation_id)
    return db_observation.resource_json


@app.get("/fhir/Observation",
         response_model=None,
         tags=["Observation"])
async def search_observations(
    patient: Optional[str] = Query(None, description="Filtro por paciente (Patient/id ou id)"),
    status: Optional[str] = Query(None, description="Filtro por status"),
    date: Optional[str] = Query(None, description="Filtro por data (YYYY-MM-DD)"),
    _count: int = Query(50, alias="_count", description="Número máximo de resultados"),
    db: Session = Depends(get_db),
    _auth: bool = Depends(check_auth)
):
    """
    Busca recursos Observation com filtros
    
    Parâmetros de busca suportados:
    - patient: referência ao paciente (Patient/123 ou apenas 123)
    - status: status da observação
    - date: data efetiva (YYYY-MM-DD)
    - _count: limite de resultados (padrão: 50)
    """
    observations = ObservationService.search_observations(
        db,
        patient=patient,
        status=status,
        date=date,
        limit=_count
    )
    
    # Retorna Bundle FHIR
    return {
        "resourceType": "Bundle",
        "type": "searchset",
        "total": len(observations),
        "entry": [
            {
                "fullUrl": f"/fhir/Observation/{o.id}",
                "resource": o.resource_json
            }
            for o in observations
        ]
    }


# ==================== Endpoint de compatibilidade (proxy) ====================

@app.api_route("/fhir/{path:path}", 
               methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
               include_in_schema=False)
async def fhir_fallback(path: str):
    """
    Endpoint de fallback para recursos não implementados
    Retorna uma mensagem informativa
    """
    return JSONResponse(
        status_code=501,
        content={
            "resourceType": "OperationOutcome",
            "issue": [
                {
                    "severity": "error",
                    "code": "not-supported",
                    "diagnostics": f"Recurso '{path}' não implementado no Mini HAPI. Recursos suportados: Patient, Observation"
                }
            ]
        }
    )
