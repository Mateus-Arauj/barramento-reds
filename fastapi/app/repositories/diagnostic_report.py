"""
Repository para recurso FHIR DiagnosticReport
"""
from typing import Optional, List
from sqlalchemy.orm import Session

from .base import BaseRepository
from app.models.diagnostic_report import DiagnosticReport


class DiagnosticReportRepository(BaseRepository[DiagnosticReport]):
    """
    Repository para operações de acesso a dados de DiagnosticReport
    """

    def __init__(self, db: Session):
        super().__init__(db, DiagnosticReport)

    def get_by_id_or_404(self, id: str) -> DiagnosticReport:
        return super().get_by_id_or_404(id, "DiagnosticReport")

    def search(
        self,
        patient_id: Optional[str] = None,
        status: Optional[str] = None,
        code: Optional[str] = None,
        category: Optional[str] = None,
        date: Optional[str] = None,
        limit: int = 50
    ) -> List[DiagnosticReport]:
        query = self.db.query(DiagnosticReport)

        if patient_id:
            query = query.filter(DiagnosticReport.patient_id == patient_id)

        if status:
            query = query.filter(DiagnosticReport.status == status)

        if code:
            query = query.filter(DiagnosticReport.code.cast(str).ilike(f"%{code}%"))

        if category:
            query = query.filter(DiagnosticReport.category.cast(str).ilike(f"%{category}%"))

        if date:
            query = query.filter(DiagnosticReport.effective_datetime.like(f"{date}%"))

        return query.limit(limit).all()

    def get_by_patient(self, patient_id: str, limit: int = 50) -> List[DiagnosticReport]:
        return self.db.query(DiagnosticReport).filter(
            DiagnosticReport.patient_id == patient_id
        ).limit(limit).all()
