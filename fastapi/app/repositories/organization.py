"""
Repository para recurso FHIR Organization
"""
from typing import Optional, List
from sqlalchemy.orm import Session

from .base import BaseRepository
from app.models.organization import Organization


class OrganizationRepository(BaseRepository[Organization]):
    """
    Repository para operações de acesso a dados de Organization
    """

    def __init__(self, db: Session):
        super().__init__(db, Organization)

    def get_by_id_or_404(self, id: str) -> Organization:
        return super().get_by_id_or_404(id, "Organization")

    def search(
        self,
        name: Optional[str] = None,
        identifier: Optional[str] = None,
        active: Optional[bool] = None,
        type_code: Optional[str] = None,
        limit: int = 50
    ) -> List[Organization]:
        query = self.db.query(Organization)

        if name:
            query = query.filter(Organization.name.ilike(f"%{name}%"))

        if identifier:
            query = query.filter(Organization.identifier.cast(str).ilike(f"%{identifier}%"))

        if active is not None:
            query = query.filter(Organization.active == str(active))

        if type_code:
            query = query.filter(Organization.type.cast(str).ilike(f"%{type_code}%"))

        return query.limit(limit).all()
