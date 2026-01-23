"""
Repository para recurso FHIR Encounter
"""
from typing import Optional, List
from sqlalchemy.orm import Session

from .base import BaseRepository
from app.models.encounter import Encounter


class EncounterRepository(BaseRepository[Encounter]):
    """
    Repository para operações de acesso a dados de Encounter
    """

    def __init__(self, db: Session):
        super().__init__(db, Encounter)

    def get_by_id_or_404(self, id: str) -> Encounter:
        """
        Busca Encounter por ID, levanta 404 se não encontrado
        """
        return super().get_by_id_or_404(id, "Encounter")

    def search(
        self,
        patient_id: Optional[str] = None,
        status: Optional[str] = None,
        date: Optional[str] = None,
        participant: Optional[str] = None,
        limit: int = 50
    ) -> List[Encounter]:
        """
        Busca encounters com filtros
        """
        query = self.db.query(Encounter)

        if patient_id:
            query = query.filter(Encounter.patient_id == patient_id)

        if status:
            query = query.filter(Encounter.status == status)

        if date:
            query = query.filter(Encounter.period.cast(str).ilike(f"%{date}%"))

        if participant:
            query = query.filter(Encounter.participant.cast(str).ilike(f"%{participant}%"))

        return query.limit(limit).all()

    def get_by_patient(self, patient_id: str, limit: int = 50) -> List[Encounter]:
        """
        Busca todos os encounters de um paciente
        """
        return self.db.query(Encounter).filter(
            Encounter.patient_id == patient_id
        ).limit(limit).all()

    def get_by_practitioner(self, practitioner_id: str, limit: int = 50) -> List[Encounter]:
        """
        Busca todos os encounters de um profissional
        """
        return self.db.query(Encounter).filter(
            Encounter.practitioner_id == practitioner_id
        ).limit(limit).all()
