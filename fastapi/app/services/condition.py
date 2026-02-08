"""
Service para recurso FHIR Condition
"""
from datetime import datetime
from fastapi import HTTPException
import uuid

from app.repositories.condition import ConditionRepository
from app.repositories.patient import PatientRepository
from app.models.condition import Condition
from app.schemas.condition import ConditionResource


class ConditionService:
    def __init__(self, repository: ConditionRepository, patient_repository: PatientRepository):
        self.repository = repository
        self.patient_repository = patient_repository

    def _extract_id(self, reference: str) -> str:
        if reference and "/" in reference:
            return reference.split("/")[-1]
        return reference

    def create(self, condition: ConditionResource) -> Condition:
        cond_id = condition.id or str(uuid.uuid4())

        patient_id = None
        subject_reference = None
        if condition.subject and condition.subject.reference:
            subject_reference = condition.subject.reference
            patient_id = self._extract_id(subject_reference)
            patient = self.patient_repository.get_by_id(patient_id)
            if not patient:
                raise HTTPException(status_code=400, detail=f"Patient/{patient_id} not found")

        encounter_id = None
        if condition.encounter and condition.encounter.reference:
            encounter_id = self._extract_id(condition.encounter.reference)

        cond_data = condition.model_dump(exclude_none=True, by_alias=True)
        cond_data["id"] = cond_id
        cond_data["meta"] = {
            "versionId": "1",
            "lastUpdated": datetime.utcnow().isoformat() + "Z"
        }

        db_condition = Condition(
            id=cond_id,
            identifier=cond_data.get("identifier"),
            clinical_status=cond_data.get("clinicalStatus"),
            verification_status=cond_data.get("verificationStatus"),
            category=cond_data.get("category"),
            severity=cond_data.get("severity"),
            code=cond_data.get("code"),
            subject_reference=subject_reference,
            patient_id=patient_id,
            encounter_id=encounter_id,
            onset_datetime=condition.onsetDateTime,
            onset_age=cond_data.get("onsetAge"),
            onset_period=cond_data.get("onsetPeriod"),
            onset_range=cond_data.get("onsetRange"),
            onset_string=condition.onsetString,
            abatement_datetime=condition.abatementDateTime,
            abatement_age=cond_data.get("abatementAge"),
            abatement_period=cond_data.get("abatementPeriod"),
            abatement_range=cond_data.get("abatementRange"),
            abatement_string=condition.abatementString,
            recorded_date=condition.recordedDate,
            recorder=cond_data.get("recorder"),
            asserter=cond_data.get("asserter"),
            stage=cond_data.get("stage"),
            evidence=cond_data.get("evidence"),
            note=cond_data.get("note"),
            body_site=cond_data.get("bodySite"),
            meta=cond_data.get("meta"),
            resource_json=cond_data
        )
        return self.repository.create(db_condition)

    def get_by_id(self, cond_id: str) -> Condition:
        return self.repository.get_by_id_or_404(cond_id)

    def update(self, cond_id: str, condition: ConditionResource) -> Condition:
        db_cond = self.repository.get_by_id_or_404(cond_id)
        cond_data = condition.model_dump(exclude_none=True, by_alias=True)
        cond_data["id"] = cond_id

        current_version = 1
        if db_cond.meta and "versionId" in db_cond.meta:
            current_version = int(db_cond.meta["versionId"]) + 1
        cond_data["meta"] = {
            "versionId": str(current_version),
            "lastUpdated": datetime.utcnow().isoformat() + "Z"
        }

        patient_id = None
        subject_reference = None
        if condition.subject and condition.subject.reference:
            subject_reference = condition.subject.reference
            patient_id = self._extract_id(subject_reference)

        db_cond.identifier = cond_data.get("identifier")
        db_cond.clinical_status = cond_data.get("clinicalStatus")
        db_cond.verification_status = cond_data.get("verificationStatus")
        db_cond.category = cond_data.get("category")
        db_cond.severity = cond_data.get("severity")
        db_cond.code = cond_data.get("code")
        db_cond.subject_reference = subject_reference
        db_cond.patient_id = patient_id
        db_cond.onset_datetime = condition.onsetDateTime
        db_cond.onset_string = condition.onsetString
        db_cond.abatement_datetime = condition.abatementDateTime
        db_cond.abatement_string = condition.abatementString
        db_cond.recorded_date = condition.recordedDate
        db_cond.recorder = cond_data.get("recorder")
        db_cond.asserter = cond_data.get("asserter")
        db_cond.stage = cond_data.get("stage")
        db_cond.evidence = cond_data.get("evidence")
        db_cond.note = cond_data.get("note")
        db_cond.body_site = cond_data.get("bodySite")
        db_cond.meta = cond_data.get("meta")
        db_cond.resource_json = cond_data
        return self.repository.update(db_cond)

    def delete(self, cond_id: str) -> None:
        self.repository.delete_by_id(cond_id, "Condition")

    def search(self, patient=None, clinical_status=None, code=None, category=None, limit=50):
        patient_id = self._extract_id(patient) if patient else None
        return self.repository.search(
            patient_id=patient_id, clinical_status=clinical_status,
            code=code, category=category, limit=limit
        )
