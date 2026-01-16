"""
Rotas para recursos FHIR Encounter
"""
from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse
from typing import Optional

from app.schemas.encounter import EncounterResource
from app.services.encounter import EncounterService
from app.api.dependencies import check_auth, get_encounter_service

router = APIRouter(prefix="/fhir", tags=["Encounter"])


@router.post("/Encounter", response_model=None, status_code=201)
async def create_encounter(
    encounter: EncounterResource,
    service: EncounterService = Depends(get_encounter_service),
    _auth: bool = Depends(check_auth)
):
    """
    Cria um novo recurso Encounter

    Valida a estrutura do recurso FHIR
    Verifica se o Patient referenciado existe
    Persiste no banco de dados PostgreSQL
    Retorna o recurso criado com ID e metadados
    """
    db_encounter = service.create(encounter)
    return JSONResponse(
        status_code=201,
        content=db_encounter.resource_json,
        headers={"Location": f"/fhir/Encounter/{db_encounter.id}"}
    )


@router.get("/Encounter/{encounter_id}", response_model=None)
async def get_encounter(
    encounter_id: str,
    service: EncounterService = Depends(get_encounter_service),
    _auth: bool = Depends(check_auth)
):
    """
    Recupera um recurso Encounter por ID

    Consulta o banco de dados
    Reconstrói o recurso em formato JSON FHIR
    Retorna 404 se não encontrado
    """
    db_encounter = service.get_by_id(encounter_id)
    return db_encounter.resource_json


@router.put("/Encounter/{encounter_id}", response_model=None)
async def update_encounter(
    encounter_id: str,
    encounter: EncounterResource,
    service: EncounterService = Depends(get_encounter_service),
    _auth: bool = Depends(check_auth)
):
    """
    Atualiza um recurso Encounter existente

    Valida a estrutura do recurso
    Atualiza no banco de dados
    Incrementa versionId nos metadados
    """
    db_encounter = service.update(encounter_id, encounter)
    return db_encounter.resource_json


@router.delete("/Encounter/{encounter_id}", status_code=204)
async def delete_encounter(
    encounter_id: str,
    service: EncounterService = Depends(get_encounter_service),
    _auth: bool = Depends(check_auth)
):
    """
    Remove um recurso Encounter

    Deleta o encontro do banco
    Retorna 204 No Content em caso de sucesso
    """
    service.delete(encounter_id)
    return None


@router.get("/Encounter", response_model=None)
async def search_encounters(
    patient: Optional[str] = Query(None, description="Filtro por paciente (Patient/id ou id)"),
    status: Optional[str] = Query(None, description="Filtro por status"),
    date: Optional[str] = Query(None, description="Filtro por data (YYYY-MM-DD)"),
    participant: Optional[str] = Query(None, description="Filtro por participante"),
    _count: int = Query(50, alias="_count", description="Número máximo de resultados"),
    service: EncounterService = Depends(get_encounter_service),
    _auth: bool = Depends(check_auth)
):
    """
    Busca recursos Encounter com filtros

    Parâmetros de busca suportados:
    - patient: referência ao paciente (Patient/123 ou apenas 123)
    - status: status do encontro (planned, arrived, in-progress, finished, etc)
    - date: data do período
    - participant: participante (Practitioner)
    - _count: limite de resultados (padrão: 50)
    """
    encounters = service.search(
        patient=patient,
        status=status,
        date=date,
        participant=participant,
        limit=_count
    )

    return {
        "resourceType": "Bundle",
        "type": "searchset",
        "total": len(encounters),
        "entry": [
            {
                "fullUrl": f"/fhir/Encounter/{e.id}",
                "resource": e.resource_json
            }
            for e in encounters
        ]
    }
