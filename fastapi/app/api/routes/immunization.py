"""
Rotas para recursos FHIR Immunization (Imunização / PNI)
"""
from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse
from typing import Optional

from app.schemas.immunization import ImmunizationResource
from app.services.immunization import ImmunizationService
from app.api.dependencies import check_auth, get_immunization_service

router = APIRouter(prefix="/fhir", tags=["Immunization"])


@router.post("/Immunization", response_model=None, status_code=201)
async def create_immunization(
    immunization: ImmunizationResource,
    service: ImmunizationService = Depends(get_immunization_service),
    _auth: bool = Depends(check_auth)
):
    """Cria um novo recurso Immunization (Vacinação PNI)"""
    db_imm = service.create(immunization)
    return JSONResponse(
        status_code=201,
        content=db_imm.resource_json,
        headers={"Location": f"/fhir/Immunization/{db_imm.id}"}
    )


@router.get("/Immunization/{immunization_id}", response_model=None)
async def get_immunization(
    immunization_id: str,
    service: ImmunizationService = Depends(get_immunization_service),
    _auth: bool = Depends(check_auth)
):
    """Recupera um recurso Immunization por ID"""
    db_imm = service.get_by_id(immunization_id)
    return db_imm.resource_json


@router.put("/Immunization/{immunization_id}", response_model=None)
async def update_immunization(
    immunization_id: str,
    immunization: ImmunizationResource,
    service: ImmunizationService = Depends(get_immunization_service),
    _auth: bool = Depends(check_auth)
):
    """Atualiza um recurso Immunization existente"""
    db_imm = service.update(immunization_id, immunization)
    return db_imm.resource_json


@router.delete("/Immunization/{immunization_id}", status_code=204)
async def delete_immunization(
    immunization_id: str,
    service: ImmunizationService = Depends(get_immunization_service),
    _auth: bool = Depends(check_auth)
):
    """Remove um recurso Immunization"""
    service.delete(immunization_id)
    return None


@router.get("/Immunization", response_model=None)
async def search_immunizations(
    patient: Optional[str] = Query(None, description="Filtro por paciente (Patient/id)"),
    status: Optional[str] = Query(None, description="Filtro por status"),
    vaccine_code: Optional[str] = Query(None, alias="vaccine-code", description="Filtro por código da vacina"),
    date: Optional[str] = Query(None, description="Filtro por data (YYYY-MM-DD)"),
    _count: int = Query(50, alias="_count", description="Número máximo de resultados"),
    service: ImmunizationService = Depends(get_immunization_service),
    _auth: bool = Depends(check_auth)
):
    """Busca recursos Immunization com filtros"""
    immunizations = service.search(
        patient=patient, status=status,
        vaccine_code=vaccine_code, date=date, limit=_count
    )
    return {
        "resourceType": "Bundle",
        "type": "searchset",
        "total": len(immunizations),
        "entry": [
            {"fullUrl": f"/fhir/Immunization/{i.id}", "resource": i.resource_json}
            for i in immunizations
        ]
    }
