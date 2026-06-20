"""
Modelo SQLAlchemy para recurso FHIR AllergyIntolerance
"""
from sqlalchemy import Column, String, JSON, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base, TimestampMixin, generate_uuid


class AllergyIntolerance(Base, TimestampMixin):
    """
    Modelo para armazenar recursos FHIR AllergyIntolerance
    Representa alergias e reações adversas do paciente
    """
    __tablename__ = "allergy_intolerances"

    id = Column(String(64), primary_key=True, default=generate_uuid)
    resource_type = Column(String(50), nullable=False, default="AllergyIntolerance")

    identifier = Column(JSON)
    clinical_status = Column(JSON)  # active | inactive | resolved
    verification_status = Column(JSON)  # unconfirmed | confirmed | refuted | entered-in-error
    type = Column(String(20))  # allergy | intolerance
    category = Column(JSON)  # food | medication | environment | biologic
    criticality = Column(String(20))  # low | high | unable-to-assess
    code = Column(JSON)  # Substância causadora

    subject_reference = Column(String(255))
    patient_id = Column(String(64), ForeignKey("patients.id"), nullable=True)
    encounter_id = Column(String(64), ForeignKey("encounters.id"), nullable=True)

    onset_datetime = Column(String(50))
    onset_age = Column(JSON)
    onset_period = Column(JSON)
    onset_range = Column(JSON)
    onset_string = Column(String(255))

    recorded_date = Column(String(50))
    recorder = Column(JSON)
    asserter = Column(JSON)
    last_occurrence = Column(String(50))
    note = Column(JSON)
    reaction = Column(JSON)  # Reações (manifestação, severidade, etc.)

    meta = Column(JSON)
    resource_json = Column(JSON, nullable=False)

    patient = relationship("Patient", foreign_keys=[patient_id])

    def __repr__(self):
        return f"<AllergyIntolerance(id={self.id}, type={self.type})>"
