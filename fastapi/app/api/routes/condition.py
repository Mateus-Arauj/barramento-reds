"""
Rotas para recursos FHIR Condition (Diagnóstico)
"""
from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse
from typing import Optional

from app.schemas.condition import ConditionResource
from app.services.condition import ConditionService
from app.api.dependencies import check_auth, get_condition_service

router = APIRouter(prefix="/fhir", tags=["Condition"])


@router.post("/Condition", response_model=None, status_code=201)
async def create_condition(
    condition: ConditionResource,
    service: ConditionService = Depends(get_condition_service),
    _auth: bool = Depends(check_auth)
):
    """Cria um novo recurso Condition (Diagnóstico CID-10/CIAP-2)"""
    db_cond = service.create(condition)
    return JSONResponse(
        status_code=201,
        content=db_cond.resource_json,
        headers={"Location": f"/fhir/Condition/{db_cond.id}"}
    )


@router.get("/Condition/{condition_id}", response_model=None)
async def get_condition(
    condition_id: str,
    service: ConditionService = Depends(get_condition_service),
    _auth: bool = Depends(check_auth)
):
    """Recupera um recurso Condition por ID"""
    db_cond = service.get_by_id(condition_id)
    return db_cond.resource_json


@router.put("/Condition/{condition_id}", response_model=None)
async def update_condition(
    condition_id: str,
    condition: ConditionResource,
    service: ConditionService = Depends(get_condition_service),
    _auth: bool = Depends(check_auth)
):
    """Atualiza um recurso Condition existente"""
    db_cond = service.update(condition_id, condition)
    return db_cond.resource_json


@router.delete("/Condition/{condition_id}", status_code=204)
async def delete_condition(
    condition_id: str,
    service: ConditionService = Depends(get_condition_service),
    _auth: bool = Depends(check_auth)
):
    """Remove um recurso Condition"""
    service.delete(condition_id)
    return None


@router.get("/Condition", response_model=None)
async def search_conditions(
    patient: Optional[str] = Query(None, description="Filtro por paciente (Patient/id)"),
    clinical_status: Optional[str] = Query(None, alias="clinical-status", description="Filtro por status clínico"),
    code: Optional[str] = Query(None, description="Filtro por código (CID-10/CIAP-2)"),
    category: Optional[str] = Query(None, description="Filtro por categoria"),
    _count: int = Query(50, alias="_count", description="Número máximo de resultados"),
    service: ConditionService = Depends(get_condition_service),
    _auth: bool = Depends(check_auth)
):
    """Busca recursos Condition com filtros"""
    conditions = service.search(
        patient=patient, clinical_status=clinical_status,
        code=code, category=category, limit=_count
    )
    return {
        "resourceType": "Bundle",
        "type": "searchset",
        "total": len(conditions),
        "entry": [
            {"fullUrl": f"/fhir/Condition/{c.id}", "resource": c.resource_json}
            for c in conditions
        ]
    }
