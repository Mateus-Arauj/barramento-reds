"""
Modelo SQLAlchemy para recurso FHIR Location (Local de Atendimento)
"""
from sqlalchemy import Column, String, JSON, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base, TimestampMixin, generate_uuid


class Location(Base, TimestampMixin):
    """
    Modelo para armazenar recursos FHIR Location
    Representa locais físicos onde atendimentos são realizados
    """
    __tablename__ = "locations"

    id = Column(String(64), primary_key=True, default=generate_uuid)
    resource_type = Column(String(50), nullable=False, default="Location")

    identifier = Column(JSON)
    status = Column(String(20))  # active | suspended | inactive
    operational_status = Column(JSON)
    name = Column(String(255))
    alias = Column(JSON)
    description = Column(String(500))
    mode = Column(String(20))  # instance | kind
    type = Column(JSON)
    telecom = Column(JSON)
    address = Column(JSON)
    physical_type = Column(JSON)
    position = Column(JSON)  # latitude, longitude, altitude
    managing_organization_id = Column(String(64), ForeignKey("organizations.id"), nullable=True)
    managing_organization = Column(JSON)
    part_of = Column(JSON)
    hours_of_operation = Column(JSON)
    availability_exceptions = Column(String(500))
    endpoint = Column(JSON)

    meta = Column(JSON)
    resource_json = Column(JSON, nullable=False)

    def __repr__(self):
        return f"<Location(id={self.id}, name={self.name})>"
