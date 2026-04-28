"""
Repository para recurso FHIR Procedure
"""
from typing import Optional, List
from sqlalchemy.orm import Session

from .base import BaseRepository
from app.models.procedure import Procedure


class ProcedureRepository(BaseRepository[Procedure]):
    """
    Repository para operações de acesso a dados de Procedure
    """

    def __init__(self, db: Session):
        super().__init__(db, Procedure)

    def get_by_id_or_404(self, id: str) -> Procedure:
        return super().get_by_id_or_404(id, "Procedure")

    def search(
        self,
        patient_id: Optional[str] = None,
        status: Optional[str] = None,
        code: Optional[str] = None,
        date: Optional[str] = None,
        limit: int = 50
    ) -> List[Procedure]:
        query = self.db.query(Procedure)

        if patient_id:
            query = query.filter(Procedure.patient_id == patient_id)

        if status:
            query = query.filter(Procedure.status == status)

        if code:
            query = query.filter(Procedure.code.cast(str).ilike(f"%{code}%"))

        if date:
            query = query.filter(Procedure.performed_datetime.like(f"{date}%"))

        return query.limit(limit).all()

    def get_by_patient(self, patient_id: str, limit: int = 50) -> List[Procedure]:
        return self.db.query(Procedure).filter(
            Procedure.patient_id == patient_id
        ).limit(limit).all()
