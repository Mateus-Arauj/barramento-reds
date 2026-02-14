"""
Repository para recurso FHIR Immunization
"""
from typing import Optional, List
from sqlalchemy.orm import Session

from .base import BaseRepository
from app.models.immunization import Immunization


class ImmunizationRepository(BaseRepository[Immunization]):
    """
    Repository para operações de acesso a dados de Immunization
    """

    def __init__(self, db: Session):
        super().__init__(db, Immunization)

    def get_by_id_or_404(self, id: str) -> Immunization:
        return super().get_by_id_or_404(id, "Immunization")

    def search(
        self,
        patient_id: Optional[str] = None,
        status: Optional[str] = None,
        vaccine_code: Optional[str] = None,
        date: Optional[str] = None,
        limit: int = 50
    ) -> List[Immunization]:
        query = self.db.query(Immunization)

        if patient_id:
            query = query.filter(Immunization.patient_id == patient_id)

        if status:
            query = query.filter(Immunization.status == status)

        if vaccine_code:
            query = query.filter(Immunization.vaccine_code.cast(str).ilike(f"%{vaccine_code}%"))

        if date:
            query = query.filter(Immunization.occurrence_datetime.like(f"{date}%"))

        return query.limit(limit).all()

    def get_by_patient(self, patient_id: str, limit: int = 50) -> List[Immunization]:
        return self.db.query(Immunization).filter(
            Immunization.patient_id == patient_id
        ).limit(limit).all()
