"""
Repository para recurso FHIR Condition
"""
from typing import Optional, List
from sqlalchemy.orm import Session

from .base import BaseRepository
from app.models.condition import Condition


class ConditionRepository(BaseRepository[Condition]):
    """
    Repository para operações de acesso a dados de Condition
    """

    def __init__(self, db: Session):
        super().__init__(db, Condition)

    def get_by_id_or_404(self, id: str) -> Condition:
        return super().get_by_id_or_404(id, "Condition")

    def search(
        self,
        patient_id: Optional[str] = None,
        clinical_status: Optional[str] = None,
        code: Optional[str] = None,
        category: Optional[str] = None,
        limit: int = 50
    ) -> List[Condition]:
        query = self.db.query(Condition)

        if patient_id:
            query = query.filter(Condition.patient_id == patient_id)

        if clinical_status:
            query = query.filter(Condition.clinical_status.cast(str).ilike(f"%{clinical_status}%"))

        if code:
            query = query.filter(Condition.code.cast(str).ilike(f"%{code}%"))

        if category:
            query = query.filter(Condition.category.cast(str).ilike(f"%{category}%"))

        return query.limit(limit).all()

    def get_by_patient(self, patient_id: str, limit: int = 50) -> List[Condition]:
        return self.db.query(Condition).filter(
            Condition.patient_id == patient_id
        ).limit(limit).all()
