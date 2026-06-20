"""
Rotas para recursos FHIR Procedure (Procedimento)
"""
from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse
from typing import Optional

from app.schemas.procedure import ProcedureResource
from app.services.procedure import ProcedureService
from app.api.dependencies import check_auth, get_procedure_service

router = APIRouter(prefix="/fhir", tags=["Procedure"])


@router.post("/Procedure", response_model=None, status_code=201)
async def create_procedure(
    procedure: ProcedureResource,
    service: ProcedureService = Depends(get_procedure_service),
    _auth: bool = Depends(check_auth)
):
    """Cria um novo recurso Procedure (Procedimento SIGTAP/TUSS)"""
    db_proc = service.create(procedure)
    return JSONResponse(
        status_code=201,
        content=db_proc.resource_json,
        headers={"Location": f"/fhir/Procedure/{db_proc.id}"}
    )


@router.get("/Procedure/{procedure_id}", response_model=None)
async def get_procedure(
    procedure_id: str,
    service: ProcedureService = Depends(get_procedure_service),
    _auth: bool = Depends(check_auth)
):
    """Recupera um recurso Procedure por ID"""
    db_proc = service.get_by_id(procedure_id)
    return db_proc.resource_json


@router.put("/Procedure/{procedure_id}", response_model=None)
async def update_procedure(
    procedure_id: str,
    procedure: ProcedureResource,
    service: ProcedureService = Depends(get_procedure_service),
    _auth: bool = Depends(check_auth)
):
    """Atualiza um recurso Procedure existente"""
    db_proc = service.update(procedure_id, procedure)
    return db_proc.resource_json


@router.delete("/Procedure/{procedure_id}", status_code=204)
async def delete_procedure(
    procedure_id: str,
    service: ProcedureService = Depends(get_procedure_service),
    _auth: bool = Depends(check_auth)
):
    """Remove um recurso Procedure"""
    service.delete(procedure_id)
    return None


@router.get("/Procedure", response_model=None)
async def search_procedures(
    patient: Optional[str] = Query(None, description="Filtro por paciente (Patient/id)"),
    status: Optional[str] = Query(None, description="Filtro por status"),
    code: Optional[str] = Query(None, description="Filtro por código (SIGTAP/TUSS)"),
    date: Optional[str] = Query(None, description="Filtro por data (YYYY-MM-DD)"),
    _count: int = Query(50, alias="_count", description="Número máximo de resultados"),
    service: ProcedureService = Depends(get_procedure_service),
    _auth: bool = Depends(check_auth)
):
    """Busca recursos Procedure com filtros"""
    procedures = service.search(
        patient=patient, status=status,
        code=code, date=date, limit=_count
    )
    return {
        "resourceType": "Bundle",
        "type": "searchset",
        "total": len(procedures),
        "entry": [
            {"fullUrl": f"/fhir/Procedure/{p.id}", "resource": p.resource_json}
            for p in procedures
        ]
    }
