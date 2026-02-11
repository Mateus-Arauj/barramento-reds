"""
Repository para recurso FHIR AllergyIntolerance
"""
from typing import Optional, List
from sqlalchemy.orm import Session

from .base import BaseRepository
from app.models.allergy_intolerance import AllergyIntolerance


class AllergyIntoleranceRepository(BaseRepository[AllergyIntolerance]):
    """
    Repository para operações de acesso a dados de AllergyIntolerance
    """

    def __init__(self, db: Session):
        super().__init__(db, AllergyIntolerance)

    def get_by_id_or_404(self, id: str) -> AllergyIntolerance:
        return super().get_by_id_or_404(id, "AllergyIntolerance")

    def search(
        self,
        patient_id: Optional[str] = None,
        clinical_status: Optional[str] = None,
        type_filter: Optional[str] = None,
        criticality: Optional[str] = None,
        limit: int = 50
    ) -> List[AllergyIntolerance]:
        query = self.db.query(AllergyIntolerance)

        if patient_id:
            query = query.filter(AllergyIntolerance.patient_id == patient_id)

        if clinical_status:
            query = query.filter(
                AllergyIntolerance.clinical_status.cast(str).ilike(f"%{clinical_status}%")
            )

        if type_filter:
            query = query.filter(AllergyIntolerance.type == type_filter)

        if criticality:
            query = query.filter(AllergyIntolerance.criticality == criticality)

        return query.limit(limit).all()

    def get_by_patient(self, patient_id: str, limit: int = 50) -> List[AllergyIntolerance]:
        return self.db.query(AllergyIntolerance).filter(
            AllergyIntolerance.patient_id == patient_id
        ).limit(limit).all()
