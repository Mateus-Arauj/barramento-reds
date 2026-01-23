"""
Repository para recurso FHIR Practitioner
"""
from typing import Optional, List
from sqlalchemy.orm import Session

from .base import BaseRepository
from app.models.practitioner import Practitioner


class PractitionerRepository(BaseRepository[Practitioner]):
    """
    Repository para operações de acesso a dados de Practitioner
    """

    def __init__(self, db: Session):
        super().__init__(db, Practitioner)

    def get_by_id_or_404(self, id: str) -> Practitioner:
        """
        Busca Practitioner por ID, levanta 404 se não encontrado
        """
        return super().get_by_id_or_404(id, "Practitioner")

    def search(
        self,
        name: Optional[str] = None,
        identifier: Optional[str] = None,
        active: Optional[bool] = None,
        limit: int = 50
    ) -> List[Practitioner]:
        """
        Busca practitioners com filtros
        """
        query = self.db.query(Practitioner)

        if name:
            query = query.filter(Practitioner.name.cast(str).ilike(f"%{name}%"))

        if identifier:
            query = query.filter(Practitioner.identifier.cast(str).ilike(f"%{identifier}%"))

        if active is not None:
            query = query.filter(Practitioner.active == str(active))

        return query.limit(limit).all()
