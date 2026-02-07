"""
Rotas para recursos FHIR Organization
"""
from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse
from typing import Optional

from app.schemas.organization import OrganizationResource
from app.services.organization import OrganizationService
from app.api.dependencies import check_auth, get_organization_service

router = APIRouter(prefix="/fhir", tags=["Organization"])


@router.post("/Organization", response_model=None, status_code=201)
async def create_organization(
    organization: OrganizationResource,
    service: OrganizationService = Depends(get_organization_service),
    _auth: bool = Depends(check_auth)
):
    """Cria um novo recurso Organization (Estabelecimento de Saúde)"""
    db_org = service.create(organization)
    return JSONResponse(
        status_code=201,
        content=db_org.resource_json,
        headers={"Location": f"/fhir/Organization/{db_org.id}"}
    )


@router.get("/Organization/{org_id}", response_model=None)
async def get_organization(
    org_id: str,
    service: OrganizationService = Depends(get_organization_service),
    _auth: bool = Depends(check_auth)
):
    """Recupera um recurso Organization por ID"""
    db_org = service.get_by_id(org_id)
    return db_org.resource_json


@router.put("/Organization/{org_id}", response_model=None)
async def update_organization(
    org_id: str,
    organization: OrganizationResource,
    service: OrganizationService = Depends(get_organization_service),
    _auth: bool = Depends(check_auth)
):
    """Atualiza um recurso Organization existente"""
    db_org = service.update(org_id, organization)
    return db_org.resource_json


@router.delete("/Organization/{org_id}", status_code=204)
async def delete_organization(
    org_id: str,
    service: OrganizationService = Depends(get_organization_service),
    _auth: bool = Depends(check_auth)
):
    """Remove um recurso Organization"""
    service.delete(org_id)
    return None


@router.get("/Organization", response_model=None)
async def search_organizations(
    name: Optional[str] = Query(None, description="Busca por nome"),
    identifier: Optional[str] = Query(None, description="Busca por CNES ou CNPJ"),
    active: Optional[bool] = Query(None, description="Filtro por status ativo"),
    type: Optional[str] = Query(None, description="Filtro por tipo de organização"),
    _count: int = Query(50, alias="_count", description="Número máximo de resultados"),
    service: OrganizationService = Depends(get_organization_service),
    _auth: bool = Depends(check_auth)
):
    """Busca recursos Organization com filtros"""
    orgs = service.search(name=name, identifier=identifier, active=active, type_code=type, limit=_count)
    return {
        "resourceType": "Bundle",
        "type": "searchset",
        "total": len(orgs),
        "entry": [
            {"fullUrl": f"/fhir/Organization/{o.id}", "resource": o.resource_json}
            for o in orgs
        ]
    }
