"""
Rotas para recursos FHIR Observation
"""
from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.schemas.observation import ObservationResource
from app.services.observation import ObservationService
from app.api.dependencies import check_auth

router = APIRouter(prefix="/fhir", tags=["Observation"])


@router.post("/Observation", response_model=None, status_code=201)
async def create_observation(
    observation: ObservationResource,
    db: Session = Depends(get_db),
    _auth: bool = Depends(check_auth)
):
    """
    Cria um novo recurso Observation
    
    Valida a estrutura do recurso FHIR
    Verifica se o Patient referenciado existe
    Persiste no banco de dados PostgreSQL
    Retorna o recurso criado com ID e metadados
    """
    db_observation = ObservationService.create_observation(db, observation)
    return JSONResponse(
        status_code=201,
        content=db_observation.resource_json,
        headers={"Location": f"/fhir/Observation/{db_observation.id}"}
    )


@router.get("/Observation/{observation_id}", response_model=None)
async def get_observation(
    observation_id: str,
    db: Session = Depends(get_db),
    _auth: bool = Depends(check_auth)
):
    """
    Recupera um recurso Observation por ID
    
    Consulta o banco de dados
    Reconstrói o recurso em formato JSON FHIR
    Retorna 404 se não encontrado
    """
    db_observation = ObservationService.get_observation(db, observation_id)
    return db_observation.resource_json


@router.get("/Observation", response_model=None)
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
