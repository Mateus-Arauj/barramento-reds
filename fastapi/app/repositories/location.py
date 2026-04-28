"""
Repository para recurso FHIR Location
"""
from typing import Optional, List
from sqlalchemy.orm import Session

from .base import BaseRepository
from app.models.location import Location


class LocationRepository(BaseRepository[Location]):
    """
    Repository para operações de acesso a dados de Location
    """

    def __init__(self, db: Session):
        super().__init__(db, Location)

    def get_by_id_or_404(self, id: str) -> Location:
        return super().get_by_id_or_404(id, "Location")

    def search(
        self,
        name: Optional[str] = None,
        status: Optional[str] = None,
        organization: Optional[str] = None,
        type_code: Optional[str] = None,
        limit: int = 50
    ) -> List[Location]:
        query = self.db.query(Location)

        if name:
            query = query.filter(Location.name.ilike(f"%{name}%"))

        if status:
            query = query.filter(Location.status == status)

        if organization:
            query = query.filter(Location.managing_organization_id == organization)

        if type_code:
            query = query.filter(Location.type.cast(str).ilike(f"%{type_code}%"))

        return query.limit(limit).all()
