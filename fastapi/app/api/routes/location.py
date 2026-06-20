"""
Rotas para recursos FHIR Location
"""
from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse
from typing import Optional

from app.schemas.location import LocationResource
from app.services.location import LocationService
from app.api.dependencies import check_auth, get_location_service

router = APIRouter(prefix="/fhir", tags=["Location"])


@router.post("/Location", response_model=None, status_code=201)
async def create_location(
    location: LocationResource,
    service: LocationService = Depends(get_location_service),
    _auth: bool = Depends(check_auth)
):
    """Cria um novo recurso Location (Local de Atendimento)"""
    db_loc = service.create(location)
    return JSONResponse(
        status_code=201,
        content=db_loc.resource_json,
        headers={"Location": f"/fhir/Location/{db_loc.id}"}
    )


@router.get("/Location/{location_id}", response_model=None)
async def get_location(
    location_id: str,
    service: LocationService = Depends(get_location_service),
    _auth: bool = Depends(check_auth)
):
    """Recupera um recurso Location por ID"""
    db_loc = service.get_by_id(location_id)
    return db_loc.resource_json


@router.put("/Location/{location_id}", response_model=None)
async def update_location(
    location_id: str,
    location: LocationResource,
    service: LocationService = Depends(get_location_service),
    _auth: bool = Depends(check_auth)
):
    """Atualiza um recurso Location existente"""
    db_loc = service.update(location_id, location)
    return db_loc.resource_json


@router.delete("/Location/{location_id}", status_code=204)
async def delete_location(
    location_id: str,
    service: LocationService = Depends(get_location_service),
    _auth: bool = Depends(check_auth)
):
    """Remove um recurso Location"""
    service.delete(location_id)
    return None


@router.get("/Location", response_model=None)
async def search_locations(
    name: Optional[str] = Query(None, description="Busca por nome"),
    status: Optional[str] = Query(None, description="Filtro por status"),
    organization: Optional[str] = Query(None, description="Filtro por organização"),
    type: Optional[str] = Query(None, description="Filtro por tipo"),
    _count: int = Query(50, alias="_count", description="Número máximo de resultados"),
    service: LocationService = Depends(get_location_service),
    _auth: bool = Depends(check_auth)
):
    """Busca recursos Location com filtros"""
    locations = service.search(name=name, status=status, organization=organization, type_code=type, limit=_count)
    return {
        "resourceType": "Bundle",
        "type": "searchset",
        "total": len(locations),
        "entry": [
            {"fullUrl": f"/fhir/Location/{l.id}", "resource": l.resource_json}
            for l in locations
        ]
    }
