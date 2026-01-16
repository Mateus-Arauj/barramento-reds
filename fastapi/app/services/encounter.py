"""
Service para recurso FHIR Encounter
"""
from datetime import datetime
from fastapi import HTTPException
import uuid

from app.repositories.encounter import EncounterRepository
from app.repositories.patient import PatientRepository
from app.repositories.practitioner import PractitionerRepository
from app.models.encounter import Encounter
from app.schemas.encounter import EncounterResource


class EncounterService:
    """
    Serviço com lógica de negócio para recursos Encounter
    """

    def __init__(
        self,
        repository: EncounterRepository,
        patient_repository: PatientRepository,
        practitioner_repository: PractitionerRepository
    ):
        """
        Inicializa o service com repositories injetados
        """
        self.repository = repository
        self.patient_repository = patient_repository
        self.practitioner_repository = practitioner_repository

    def _extract_patient_id(self, subject_reference: str) -> str:
        """
        Extrai o ID do paciente da referência FHIR
        """
        if subject_reference and "/" in subject_reference:
            return subject_reference.split("/")[-1]
        return subject_reference

    def _extract_practitioner_id(self, participant_list: list) -> str:
        """
        Extrai o ID do primeiro practitioner da lista de participantes
        """
        if participant_list:
            for p in participant_list:
                if p.individual and p.individual.reference:
                    ref = p.individual.reference
                    if "Practitioner/" in ref:
                        return ref.split("/")[-1]
        return None

    def create(self, encounter: EncounterResource) -> Encounter:
        """
        Cria um novo recurso Encounter
        """
        encounter_id = encounter.id or str(uuid.uuid4())

        patient_id = None
        subject_reference = None
        if encounter.subject and encounter.subject.reference:
            subject_reference = encounter.subject.reference
            patient_id = self._extract_patient_id(subject_reference)

            patient = self.patient_repository.get_by_id(patient_id)
            if not patient:
                raise HTTPException(
                    status_code=400,
                    detail=f"Patient/{patient_id} not found"
                )

        practitioner_id = None
        if encounter.participant:
            practitioner_id = self._extract_practitioner_id(encounter.participant)
            if practitioner_id:
                practitioner = self.practitioner_repository.get_by_id(practitioner_id)
                if not practitioner:
                    practitioner_id = None

        encounter_data = encounter.model_dump(exclude_none=True, by_alias=True)
        encounter_data["id"] = encounter_id
        encounter_data["meta"] = {
            "versionId": "1",
            "lastUpdated": datetime.utcnow().isoformat() + "Z"
        }

        db_encounter = Encounter(
            id=encounter_id,
            identifier=encounter_data.get("identifier"),
            status=encounter.status,
            status_history=encounter_data.get("statusHistory"),
            encounter_class=encounter_data.get("class"),
            class_history=encounter_data.get("classHistory"),
            type=encounter_data.get("type"),
            service_type=encounter_data.get("serviceType"),
            priority=encounter_data.get("priority"),
            subject_reference=subject_reference,
            patient_id=patient_id,
            practitioner_id=practitioner_id,
            episode_of_care=encounter_data.get("episodeOfCare"),
            based_on=encounter_data.get("basedOn"),
            participant=encounter_data.get("participant"),
            appointment=encounter_data.get("appointment"),
            period=encounter_data.get("period"),
            length=encounter_data.get("length"),
            reason_code=encounter_data.get("reasonCode"),
            reason_reference=encounter_data.get("reasonReference"),
            diagnosis=encounter_data.get("diagnosis"),
            account=encounter_data.get("account"),
            hospitalization=encounter_data.get("hospitalization"),
            location=encounter_data.get("location"),
            service_provider=encounter_data.get("serviceProvider"),
            part_of=encounter_data.get("partOf"),
            meta=encounter_data.get("meta"),
            resource_json=encounter_data
        )

        return self.repository.create(db_encounter)

    def get_by_id(self, encounter_id: str) -> Encounter:
        """
        Recupera um Encounter por ID
        """
        return self.repository.get_by_id_or_404(encounter_id)

    def update(self, encounter_id: str, encounter: EncounterResource) -> Encounter:
        """
        Atualiza um Encounter existente
        """
        db_encounter = self.repository.get_by_id_or_404(encounter_id)

        patient_id = None
        subject_reference = None
        if encounter.subject and encounter.subject.reference:
            subject_reference = encounter.subject.reference
            patient_id = self._extract_patient_id(subject_reference)

        practitioner_id = None
        if encounter.participant:
            practitioner_id = self._extract_practitioner_id(encounter.participant)

        encounter_data = encounter.model_dump(exclude_none=True, by_alias=True)
        encounter_data["id"] = encounter_id

        current_version = 1
        if db_encounter.meta and "versionId" in db_encounter.meta:
            current_version = int(db_encounter.meta["versionId"]) + 1

        encounter_data["meta"] = {
            "versionId": str(current_version),
            "lastUpdated": datetime.utcnow().isoformat() + "Z"
        }

        db_encounter.identifier = encounter_data.get("identifier")
        db_encounter.status = encounter.status
        db_encounter.status_history = encounter_data.get("statusHistory")
        db_encounter.encounter_class = encounter_data.get("class")
        db_encounter.class_history = encounter_data.get("classHistory")
        db_encounter.type = encounter_data.get("type")
        db_encounter.service_type = encounter_data.get("serviceType")
        db_encounter.priority = encounter_data.get("priority")
        db_encounter.subject_reference = subject_reference
        db_encounter.patient_id = patient_id
        db_encounter.practitioner_id = practitioner_id
        db_encounter.episode_of_care = encounter_data.get("episodeOfCare")
        db_encounter.based_on = encounter_data.get("basedOn")
        db_encounter.participant = encounter_data.get("participant")
        db_encounter.appointment = encounter_data.get("appointment")
        db_encounter.period = encounter_data.get("period")
        db_encounter.length = encounter_data.get("length")
        db_encounter.reason_code = encounter_data.get("reasonCode")
        db_encounter.reason_reference = encounter_data.get("reasonReference")
        db_encounter.diagnosis = encounter_data.get("diagnosis")
        db_encounter.account = encounter_data.get("account")
        db_encounter.hospitalization = encounter_data.get("hospitalization")
        db_encounter.location = encounter_data.get("location")
        db_encounter.service_provider = encounter_data.get("serviceProvider")
        db_encounter.part_of = encounter_data.get("partOf")
        db_encounter.meta = encounter_data.get("meta")
        db_encounter.resource_json = encounter_data

        return self.repository.update(db_encounter)

    def delete(self, encounter_id: str) -> None:
        """
        Remove um Encounter
        """
        self.repository.delete_by_id(encounter_id, "Encounter")

    def search(
        self,
        patient: str = None,
        status: str = None,
        date: str = None,
        participant: str = None,
        limit: int = 50
    ) -> list:
        """
        Busca Encounters com filtros
        """
        patient_id = None
        if patient:
            patient_id = self._extract_patient_id(patient)

        return self.repository.search(
            patient_id=patient_id,
            status=status,
            date=date,
            participant=participant,
            limit=limit
        )
