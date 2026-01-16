"""
Repository para recurso FHIR Patient
"""
from typing import Optional, List
from sqlalchemy.orm import Session

from .base import BaseRepository
from app.models.patient import Patient


class PatientRepository(BaseRepository[Patient]):
    """
    Repository para operações de acesso a dados de Patient
    """

    def __init__(self, db: Session):
        super().__init__(db, Patient)

    def get_by_id_or_404(self, id: str) -> Patient:
        """
        Busca Patient por ID, levanta 404 se não encontrado
        """
        return super().get_by_id_or_404(id, "Patient")

    def search(
        self,
        name: Optional[str] = None,
        gender: Optional[str] = None,
        birthdate: Optional[str] = None,
        limit: int = 50
    ) -> List[Patient]:
        """
        Busca patients com filtros
        """
        query = self.db.query(Patient)

        if name:
            query = query.filter(Patient.name.cast(str).ilike(f"%{name}%"))

        if gender:
            query = query.filter(Patient.gender == gender)

        if birthdate:
            query = query.filter(Patient.birth_date == birthdate)

        return query.limit(limit).all()
