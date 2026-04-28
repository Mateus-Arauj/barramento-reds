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
    marital_status = Column(JSON)
    deceased_boolean = Column(String(10))
    deceased_datetime = Column(String(50))
    multiple_birth_boolean = Column(String(10))
    multiple_birth_integer = Column(String(10))
    contact = Column(JSON)
    communication = Column(JSON)
    general_practitioner = Column(JSON)
    managing_organization = Column(JSON)

    # Extensões BR Core
    mother_name = Column(String(255))
    father_name = Column(String(255))
    nationality = Column(JSON)
    race = Column(JSON)
    ethnicity = Column(JSON)
    birth_city = Column(JSON)

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
