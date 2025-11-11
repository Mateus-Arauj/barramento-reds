"""
Rotas para recursos FHIR Patient
"""
from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.schemas.patient import PatientResource
from app.services.patient import PatientService
from app.api.dependencies import check_auth

router = APIRouter(prefix="/fhir", tags=["Patient"])


@router.post("/Patient", response_model=None, status_code=201)
async def create_patient(
    patient: PatientResource,
    db: Session = Depends(get_db),
    _auth: bool = Depends(check_auth)
):
    """
    Cria um novo recurso Patient
    
    Valida a estrutura do recurso FHIR
    Persiste no banco de dados PostgreSQL
    Retorna o recurso criado com ID e metadados
    """
    db_patient = PatientService.create_patient(db, patient)
    return JSONResponse(
        status_code=201,
        content=db_patient.resource_json,
        headers={"Location": f"/fhir/Patient/{db_patient.id}"}
    )


@router.get("/Patient/{patient_id}", response_model=None)
async def get_patient(
    patient_id: str,
    db: Session = Depends(get_db),
    _auth: bool = Depends(check_auth)
):
    """
    Recupera um recurso Patient por ID
    
    Consulta o banco de dados
    Reconstrói o recurso em formato JSON FHIR
    Retorna 404 se não encontrado
    """
    db_patient = PatientService.get_patient(db, patient_id)
    return db_patient.resource_json


@router.put("/Patient/{patient_id}", response_model=None)
async def update_patient(
    patient_id: str,
    patient: PatientResource,
    db: Session = Depends(get_db),
    _auth: bool = Depends(check_auth)
):
    """
    Atualiza um recurso Patient existente
    
    Valida a estrutura do recurso
    Atualiza no banco de dados
    Incrementa versionId nos metadados
    """
    db_patient = PatientService.update_patient(db, patient_id, patient)
    return db_patient.resource_json


@router.delete("/Patient/{patient_id}", status_code=204)
async def delete_patient(
    patient_id: str,
    db: Session = Depends(get_db),
    _auth: bool = Depends(check_auth)
):
    """
    Remove um recurso Patient
    
    Deleta o paciente e suas observações associadas
    Retorna 204 No Content em caso de sucesso
    """
    PatientService.delete_patient(db, patient_id)
    return None


@router.get("/Patient", response_model=None)
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
