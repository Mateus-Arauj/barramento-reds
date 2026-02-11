"""
Rotas para recursos FHIR AllergyIntolerance
"""
from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse
from typing import Optional

from app.schemas.allergy_intolerance import AllergyIntoleranceResource
from app.services.allergy_intolerance import AllergyIntoleranceService
from app.api.dependencies import check_auth, get_allergy_intolerance_service

router = APIRouter(prefix="/fhir", tags=["AllergyIntolerance"])


@router.post("/AllergyIntolerance", response_model=None, status_code=201)
async def create_allergy_intolerance(
    allergy: AllergyIntoleranceResource,
    service: AllergyIntoleranceService = Depends(get_allergy_intolerance_service),
    _auth: bool = Depends(check_auth)
):
    """Cria um novo recurso AllergyIntolerance (Alergia/Reação Adversa)"""
    db_allergy = service.create(allergy)
    return JSONResponse(
        status_code=201,
        content=db_allergy.resource_json,
        headers={"Location": f"/fhir/AllergyIntolerance/{db_allergy.id}"}
    )


@router.get("/AllergyIntolerance/{allergy_id}", response_model=None)
async def get_allergy_intolerance(
    allergy_id: str,
    service: AllergyIntoleranceService = Depends(get_allergy_intolerance_service),
    _auth: bool = Depends(check_auth)
):
    """Recupera um recurso AllergyIntolerance por ID"""
    db_allergy = service.get_by_id(allergy_id)
    return db_allergy.resource_json


@router.put("/AllergyIntolerance/{allergy_id}", response_model=None)
async def update_allergy_intolerance(
    allergy_id: str,
    allergy: AllergyIntoleranceResource,
    service: AllergyIntoleranceService = Depends(get_allergy_intolerance_service),
    _auth: bool = Depends(check_auth)
):
    """Atualiza um recurso AllergyIntolerance existente"""
    db_allergy = service.update(allergy_id, allergy)
    return db_allergy.resource_json


@router.delete("/AllergyIntolerance/{allergy_id}", status_code=204)
async def delete_allergy_intolerance(
    allergy_id: str,
    service: AllergyIntoleranceService = Depends(get_allergy_intolerance_service),
    _auth: bool = Depends(check_auth)
):
    """Remove um recurso AllergyIntolerance"""
    service.delete(allergy_id)
    return None


@router.get("/AllergyIntolerance", response_model=None)
async def search_allergy_intolerances(
    patient: Optional[str] = Query(None, description="Filtro por paciente (Patient/id)"),
    clinical_status: Optional[str] = Query(None, alias="clinical-status", description="Filtro por status clínico"),
    type: Optional[str] = Query(None, description="Filtro por tipo (allergy/intolerance)"),
    criticality: Optional[str] = Query(None, description="Filtro por criticidade"),
    _count: int = Query(50, alias="_count", description="Número máximo de resultados"),
    service: AllergyIntoleranceService = Depends(get_allergy_intolerance_service),
    _auth: bool = Depends(check_auth)
):
    """Busca recursos AllergyIntolerance com filtros"""
    allergies = service.search(
        patient=patient, clinical_status=clinical_status,
        type_filter=type, criticality=criticality, limit=_count
    )
    return {
        "resourceType": "Bundle",
        "type": "searchset",
        "total": len(allergies),
        "entry": [
            {"fullUrl": f"/fhir/AllergyIntolerance/{a.id}", "resource": a.resource_json}
            for a in allergies
        ]
    }
