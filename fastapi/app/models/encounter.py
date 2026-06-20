"""
Modelo SQLAlchemy para recurso FHIR Encounter
"""
from sqlalchemy import Column, String, JSON, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base, TimestampMixin, generate_uuid


class Encounter(Base, TimestampMixin):
    """
    Modelo para armazenar recursos FHIR Encounter
    """
    __tablename__ = "encounters"

    id = Column(String(64), primary_key=True, default=generate_uuid)
    resource_type = Column(String(50), nullable=False, default="Encounter")

    identifier = Column(JSON)
    status = Column(String(30))
    status_history = Column(JSON)
    encounter_class = Column(JSON)
    class_history = Column(JSON)
    type = Column(JSON)
    service_type = Column(JSON)
    priority = Column(JSON)

    subject_reference = Column(String(255))
    patient_id = Column(String(64), ForeignKey("patients.id"), nullable=True)
    practitioner_id = Column(String(64), ForeignKey("practitioners.id"), nullable=True)

    episode_of_care = Column(JSON)
    based_on = Column(JSON)
    participant = Column(JSON)
    appointment = Column(JSON)
    period = Column(JSON)
    length = Column(JSON)
    reason_code = Column(JSON)
    reason_reference = Column(JSON)
    diagnosis = Column(JSON)
    account = Column(JSON)
    hospitalization = Column(JSON)
    location = Column(JSON)
    service_provider = Column(JSON)
    part_of = Column(JSON)

    meta = Column(JSON)
    resource_json = Column(JSON, nullable=False)

    patient = relationship("Patient", back_populates="encounters")
    practitioner_ref = relationship(
        "Practitioner",
        back_populates="encounters",
        foreign_keys=[practitioner_id]
    )

    def __repr__(self):
        return f"<Encounter(id={self.id}, status={self.status})>"
