"""
Modelo SQLAlchemy para recurso FHIR Observation
"""
from sqlalchemy import Column, String, Text, Integer, JSON, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base, TimestampMixin, generate_uuid


class Observation(Base, TimestampMixin):
    """
    Modelo para armazenar recursos FHIR Observation
    """
    __tablename__ = "observations"

    id = Column(String(64), primary_key=True, default=generate_uuid)
    resource_type = Column(String(50), nullable=False, default="Observation")

    identifier = Column(JSON)
    status = Column(String(20))
    category = Column(JSON)
    code = Column(JSON)

    subject_reference = Column(String(255))
    patient_id = Column(String(64), ForeignKey("patients.id"), nullable=True)

    effective_datetime = Column(String(50))
    effective_period = Column(JSON)
    issued = Column(String(50))

    value_quantity = Column(JSON)
    value_codeable_concept = Column(JSON)
    value_string = Column(Text)
    value_boolean = Column(String(10))
    value_integer = Column(Integer)
    value_range = Column(JSON)
    value_ratio = Column(JSON)
    value_sampled_data = Column(JSON)
    value_time = Column(String(20))
    value_datetime = Column(String(50))
    value_period = Column(JSON)

    performer = Column(JSON)
    encounter_reference = Column(String(255))
    interpretation = Column(JSON)
    body_site = Column(JSON)
    method = Column(JSON)
    specimen = Column(JSON)
    device = Column(JSON)
    reference_range = Column(JSON)
    has_member = Column(JSON)
    derived_from = Column(JSON)
    component = Column(JSON)
    note = Column(JSON)

    meta = Column(JSON)
    resource_json = Column(JSON, nullable=False)

    patient = relationship("Patient", back_populates="observations")

    def __repr__(self):
        return f"<Observation(id={self.id}, status={self.status})>"
