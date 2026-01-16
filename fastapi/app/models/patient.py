"""
Modelo SQLAlchemy para recurso FHIR Patient
"""
from sqlalchemy import Column, String, JSON
from sqlalchemy.orm import relationship

from .base import Base, TimestampMixin, generate_uuid


class Patient(Base, TimestampMixin):
    """
    Modelo para armazenar recursos FHIR Patient
    """
    __tablename__ = "patients"

    id = Column(String(64), primary_key=True, default=generate_uuid)
    resource_type = Column(String(50), nullable=False, default="Patient")

    identifier = Column(JSON)
    active = Column(String(10))
    name = Column(JSON)
    telecom = Column(JSON)
    gender = Column(String(20))
    birth_date = Column(String(20))
    address = Column(JSON)

    meta = Column(JSON)
    resource_json = Column(JSON, nullable=False)

    observations = relationship(
        "Observation",
        back_populates="patient",
        cascade="all, delete-orphan"
    )
    encounters = relationship(
        "Encounter",
        back_populates="patient",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Patient(id={self.id}, name={self.name})>"
