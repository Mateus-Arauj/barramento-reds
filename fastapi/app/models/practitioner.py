"""
Modelo SQLAlchemy para recurso FHIR Practitioner
"""
from sqlalchemy import Column, String, JSON
from sqlalchemy.orm import relationship

from .base import Base, TimestampMixin, generate_uuid


class Practitioner(Base, TimestampMixin):
    """
    Modelo para armazenar recursos FHIR Practitioner
    """
    __tablename__ = "practitioners"

    id = Column(String(64), primary_key=True, default=generate_uuid)
    resource_type = Column(String(50), nullable=False, default="Practitioner")

    identifier = Column(JSON)
    active = Column(String(10))
    name = Column(JSON)
    telecom = Column(JSON)
    address = Column(JSON)
    gender = Column(String(20))
    birth_date = Column(String(20))
    photo = Column(JSON)
    qualification = Column(JSON)
    communication = Column(JSON)

    meta = Column(JSON)
    resource_json = Column(JSON, nullable=False)

    encounters = relationship(
        "Encounter",
        back_populates="practitioner_ref",
        foreign_keys="Encounter.practitioner_id"
    )

    def __repr__(self):
        return f"<Practitioner(id={self.id}, name={self.name})>"
