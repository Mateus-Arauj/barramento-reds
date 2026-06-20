"""
Rotas para recursos FHIR Practitioner
"""
from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse
from typing import Optional

from app.schemas.practitioner import PractitionerResource
from app.services.practitioner import PractitionerService
from app.api.dependencies import check_auth, get_practitioner_service

router = APIRouter(prefix="/fhir", tags=["Practitioner"])


@router.post("/Practitioner", response_model=None, status_code=201)
async def create_practitioner(
    practitioner: PractitionerResource,
    service: PractitionerService = Depends(get_practitioner_service),
    _auth: bool = Depends(check_auth)
):
    """
    Cria um novo recurso Practitioner

    Valida a estrutura do recurso FHIR
    Persiste no banco de dados PostgreSQL
    Retorna o recurso criado com ID e metadados
    """
    db_practitioner = service.create(practitioner)
    return JSONResponse(
        status_code=201,
        content=db_practitioner.resource_json,
        headers={"Location": f"/fhir/Practitioner/{db_practitioner.id}"}
    )


@router.get("/Practitioner/{practitioner_id}", response_model=None)
async def get_practitioner(
    practitioner_id: str,
    service: PractitionerService = Depends(get_practitioner_service),
    _auth: bool = Depends(check_auth)
):
    """
    Recupera um recurso Practitioner por ID

    Consulta o banco de dados
    Reconstrói o recurso em formato JSON FHIR
    Retorna 404 se não encontrado
    """
    db_practitioner = service.get_by_id(practitioner_id)
    return db_practitioner.resource_json


@router.put("/Practitioner/{practitioner_id}", response_model=None)
async def update_practitioner(
    practitioner_id: str,
    practitioner: PractitionerResource,
    service: PractitionerService = Depends(get_practitioner_service),
    _auth: bool = Depends(check_auth)
):
    """
    Atualiza um recurso Practitioner existente

    Valida a estrutura do recurso
    Atualiza no banco de dados
    Incrementa versionId nos metadados
    """
    db_practitioner = service.update(practitioner_id, practitioner)
    return db_practitioner.resource_json


@router.delete("/Practitioner/{practitioner_id}", status_code=204)
async def delete_practitioner(
    practitioner_id: str,
    service: PractitionerService = Depends(get_practitioner_service),
    _auth: bool = Depends(check_auth)
):
    """
    Remove um recurso Practitioner

    Deleta o profissional do banco
    Retorna 204 No Content em caso de sucesso
    """
    service.delete(practitioner_id)
    return None


@router.get("/Practitioner", response_model=None)
async def search_practitioners(
    name: Optional[str] = Query(None, description="Busca por nome"),
    identifier: Optional[str] = Query(None, description="Busca por identificador (CRM, COREN)"),
    active: Optional[bool] = Query(None, description="Filtro por status ativo"),
    _count: int = Query(50, alias="_count", description="Número máximo de resultados"),
    service: PractitionerService = Depends(get_practitioner_service),
    _auth: bool = Depends(check_auth)
):
    """
    Busca recursos Practitioner com filtros

    Parâmetros de busca suportados:
    - name: nome do profissional
    - identifier: identificador (CRM, COREN, etc)
    - active: status ativo (true/false)
    - _count: limite de resultados (padrão: 50)
    """
    practitioners = service.search(
        name=name,
        identifier=identifier,
        active=active,
        limit=_count
    )

    return {
        "resourceType": "Bundle",
        "type": "searchset",
        "total": len(practitioners),
        "entry": [
            {
                "fullUrl": f"/fhir/Practitioner/{p.id}",
                "resource": p.resource_json
            }
            for p in practitioners
        ]
    }
