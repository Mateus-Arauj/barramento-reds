"""
Repository para recurso FHIR Observation
"""
from typing import Optional, List
from sqlalchemy.orm import Session

from .base import BaseRepository
from app.models.observation import Observation


class ObservationRepository(BaseRepository[Observation]):
    """
    Repository para operações de acesso a dados de Observation
    """

    def __init__(self, db: Session):
        super().__init__(db, Observation)

    def get_by_id_or_404(self, id: str) -> Observation:
        """
        Busca Observation por ID, levanta 404 se não encontrado
        """
        return super().get_by_id_or_404(id, "Observation")

    def search(
        self,
        patient_id: Optional[str] = None,
        status: Optional[str] = None,
        date: Optional[str] = None,
        limit: int = 50
    ) -> List[Observation]:
        """
        Busca observations com filtros
        """
        query = self.db.query(Observation)

        if patient_id:
            query = query.filter(Observation.patient_id == patient_id)

        if status:
            query = query.filter(Observation.status == status)

        if date:
            query = query.filter(Observation.effective_datetime.like(f"{date}%"))

        return query.limit(limit).all()

    def get_by_patient(self, patient_id: str, limit: int = 50) -> List[Observation]:
        """
        Busca todas as observations de um paciente
        """
        return self.db.query(Observation).filter(
            Observation.patient_id == patient_id
        ).limit(limit).all()
