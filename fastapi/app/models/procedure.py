"""
Modelo SQLAlchemy para recurso FHIR Procedure (Procedimento Realizado)
"""
from sqlalchemy import Column, String, JSON, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base, TimestampMixin, generate_uuid


class Procedure(Base, TimestampMixin):
    """
    Modelo para armazenar recursos FHIR Procedure
    Representa procedimentos realizados (SIGTAP, TUSS)
    """
    __tablename__ = "procedures"

    id = Column(String(64), primary_key=True, default=generate_uuid)
    resource_type = Column(String(50), nullable=False, default="Procedure")

    identifier = Column(JSON)
    instantiates_canonical = Column(JSON)
    instantiates_uri = Column(JSON)
    based_on = Column(JSON)
    part_of = Column(JSON)
    status = Column(String(30))  # preparation | in-progress | not-done | on-hold | stopped | completed | entered-in-error | unknown
    status_reason = Column(JSON)
    category = Column(JSON)
    code = Column(JSON)  # SIGTAP, TUSS

    subject_reference = Column(String(255))
    patient_id = Column(String(64), ForeignKey("patients.id"), nullable=True)
    encounter_id = Column(String(64), ForeignKey("encounters.id"), nullable=True)

    performed_datetime = Column(String(50))
    performed_period = Column(JSON)
    performed_string = Column(String(255))
    performed_age = Column(JSON)
    performed_range = Column(JSON)

    recorder = Column(JSON)
    asserter = Column(JSON)
    performer = Column(JSON)
    location = Column(JSON)
    reason_code = Column(JSON)
    reason_reference = Column(JSON)
    body_site = Column(JSON)
    outcome = Column(JSON)
    report = Column(JSON)
    complication = Column(JSON)
    complication_detail = Column(JSON)
    follow_up = Column(JSON)
    note = Column(JSON)
    focal_device = Column(JSON)
    used_reference = Column(JSON)
    used_code = Column(JSON)

    meta = Column(JSON)
    resource_json = Column(JSON, nullable=False)

    patient = relationship("Patient", foreign_keys=[patient_id])

    def __repr__(self):
        return f"<Procedure(id={self.id}, status={self.status})>"
