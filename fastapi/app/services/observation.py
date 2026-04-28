"""
Service para recurso FHIR Observation
"""
from datetime import datetime
from fastapi import HTTPException
import uuid

from app.repositories.observation import ObservationRepository
from app.repositories.patient import PatientRepository
from app.models.observation import Observation
from app.schemas.observation import ObservationResource


class ObservationService:
    """
    Serviço com lógica de negócio para recursos Observation
    """

    def __init__(
        self,
        repository: ObservationRepository,
        patient_repository: PatientRepository
    ):
        """
        Inicializa o service com repositories injetados
        """
        self.repository = repository
        self.patient_repository = patient_repository

    def _extract_patient_id(self, subject_reference: str) -> str:
        """
        Extrai o ID do paciente da referência FHIR
        """
        if subject_reference and "/" in subject_reference:
            return subject_reference.split("/")[-1]
        return subject_reference

    def create(self, observation: ObservationResource) -> Observation:
        """
        Cria um novo recurso Observation
        """
        observation_id = observation.id or str(uuid.uuid4())

        patient_id = None
        subject_reference = None
        if observation.subject and observation.subject.reference:
            subject_reference = observation.subject.reference
            patient_id = self._extract_patient_id(subject_reference)

            patient = self.patient_repository.get_by_id(patient_id)
            if not patient:
                raise HTTPException(
                    status_code=400,
                    detail=f"Patient/{patient_id} not found"
                )

        observation_data = observation.model_dump(exclude_none=True, by_alias=True)
        observation_data["id"] = observation_id
        observation_data["meta"] = {
            "versionId": "1",
            "lastUpdated": datetime.utcnow().isoformat() + "Z"
        }

        db_observation = Observation(
            id=observation_id,
            identifier=observation_data.get("identifier"),
            status=observation.status,
            category=observation_data.get("category"),
            code=observation_data.get("code"),
            subject_reference=subject_reference,
            patient_id=patient_id,
            effective_datetime=observation.effectiveDateTime,
            effective_period=observation_data.get("effectivePeriod"),
            issued=observation.issued,
            value_quantity=observation_data.get("valueQuantity"),
            value_codeable_concept=observation_data.get("valueCodeableConcept"),
            value_string=observation.valueString,
            value_boolean=str(observation.valueBoolean) if observation.valueBoolean is not None else None,
            value_integer=observation.valueInteger,
            value_range=observation_data.get("valueRange"),
            value_ratio=observation_data.get("valueRatio"),
            value_sampled_data=observation_data.get("valueSampledData"),
            value_time=observation.valueTime,
            value_datetime=observation.valueDateTime,
            value_period=observation_data.get("valuePeriod"),
            performer=observation_data.get("performer"),
            encounter_reference=observation.encounter.reference if observation.encounter and observation.encounter.reference else None,
            interpretation=observation_data.get("interpretation"),
            body_site=observation_data.get("bodySite"),
            method=observation_data.get("method"),
            specimen=observation_data.get("specimen"),
            device=observation_data.get("device"),
            reference_range=observation_data.get("referenceRange"),
            has_member=observation_data.get("hasMember"),
            derived_from=observation_data.get("derivedFrom"),
            component=observation_data.get("component"),
            note=observation_data.get("note"),
            meta=observation_data.get("meta"),
            resource_json=observation_data
        )

        return self.repository.create(db_observation)

    def get_by_id(self, observation_id: str) -> Observation:
        """
        Recupera uma Observation por ID
        """
        return self.repository.get_by_id_or_404(observation_id)

    def search(
        self,
        patient: str = None,
        status: str = None,
        date: str = None,
        limit: int = 50
    ) -> list:
        """
        Busca Observations com filtros
        """
        patient_id = None
        if patient:
            patient_id = self._extract_patient_id(patient)

        return self.repository.search(
            patient_id=patient_id,
            status=status,
            date=date,
            limit=limit
        )
