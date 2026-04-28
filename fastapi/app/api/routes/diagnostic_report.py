"""
Rotas para recursos FHIR DiagnosticReport (Laudo Diagnóstico)
"""
from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse
from typing import Optional

from app.schemas.diagnostic_report import DiagnosticReportResource
from app.services.diagnostic_report import DiagnosticReportService
from app.api.dependencies import check_auth, get_diagnostic_report_service

router = APIRouter(prefix="/fhir", tags=["DiagnosticReport"])


@router.post("/DiagnosticReport", response_model=None, status_code=201)
async def create_diagnostic_report(
    report: DiagnosticReportResource,
    service: DiagnosticReportService = Depends(get_diagnostic_report_service),
    _auth: bool = Depends(check_auth)
):
    """Cria um novo recurso DiagnosticReport (Laudo de Exame)"""
    db_report = service.create(report)
    return JSONResponse(
        status_code=201,
        content=db_report.resource_json,
        headers={"Location": f"/fhir/DiagnosticReport/{db_report.id}"}
    )


@router.get("/DiagnosticReport/{report_id}", response_model=None)
async def get_diagnostic_report(
    report_id: str,
    service: DiagnosticReportService = Depends(get_diagnostic_report_service),
    _auth: bool = Depends(check_auth)
):
    """Recupera um recurso DiagnosticReport por ID"""
    db_report = service.get_by_id(report_id)
    return db_report.resource_json


@router.put("/DiagnosticReport/{report_id}", response_model=None)
async def update_diagnostic_report(
    report_id: str,
    report: DiagnosticReportResource,
    service: DiagnosticReportService = Depends(get_diagnostic_report_service),
    _auth: bool = Depends(check_auth)
):
    """Atualiza um recurso DiagnosticReport existente"""
    db_report = service.update(report_id, report)
    return db_report.resource_json


@router.delete("/DiagnosticReport/{report_id}", status_code=204)
async def delete_diagnostic_report(
    report_id: str,
    service: DiagnosticReportService = Depends(get_diagnostic_report_service),
    _auth: bool = Depends(check_auth)
):
    """Remove um recurso DiagnosticReport"""
    service.delete(report_id)
    return None


@router.get("/DiagnosticReport", response_model=None)
async def search_diagnostic_reports(
    patient: Optional[str] = Query(None, description="Filtro por paciente (Patient/id)"),
    status: Optional[str] = Query(None, description="Filtro por status"),
    code: Optional[str] = Query(None, description="Filtro por código do laudo"),
    category: Optional[str] = Query(None, description="Filtro por categoria (LAB, RAD, etc)"),
    date: Optional[str] = Query(None, description="Filtro por data (YYYY-MM-DD)"),
    _count: int = Query(50, alias="_count", description="Número máximo de resultados"),
    service: DiagnosticReportService = Depends(get_diagnostic_report_service),
    _auth: bool = Depends(check_auth)
):
    """Busca recursos DiagnosticReport com filtros"""
    reports = service.search(
        patient=patient, status=status,
        code=code, category=category, date=date, limit=_count
    )
    return {
        "resourceType": "Bundle",
        "type": "searchset",
        "total": len(reports),
        "entry": [
            {"fullUrl": f"/fhir/DiagnosticReport/{r.id}", "resource": r.resource_json}
            for r in reports
        ]
    }
