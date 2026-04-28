"""
Service para recurso FHIR AllergyIntolerance
"""
from datetime import datetime
from fastapi import HTTPException
import uuid

from app.repositories.allergy_intolerance import AllergyIntoleranceRepository
from app.repositories.patient import PatientRepository
from app.models.allergy_intolerance import AllergyIntolerance
from app.schemas.allergy_intolerance import AllergyIntoleranceResource


class AllergyIntoleranceService:
    def __init__(self, repository: AllergyIntoleranceRepository, patient_repository: PatientRepository):
        self.repository = repository
        self.patient_repository = patient_repository

    def _extract_id(self, reference: str) -> str:
        if reference and "/" in reference:
            return reference.split("/")[-1]
        return reference

    def create(self, allergy: AllergyIntoleranceResource) -> AllergyIntolerance:
        allergy_id = allergy.id or str(uuid.uuid4())

        patient_id = None
        subject_reference = None
        if allergy.patient and allergy.patient.reference:
            subject_reference = allergy.patient.reference
            patient_id = self._extract_id(subject_reference)
            patient = self.patient_repository.get_by_id(patient_id)
            if not patient:
                raise HTTPException(status_code=400, detail=f"Patient/{patient_id} not found")

        encounter_id = None
        if allergy.encounter and allergy.encounter.reference:
            encounter_id = self._extract_id(allergy.encounter.reference)

        allergy_data = allergy.model_dump(exclude_none=True, by_alias=True)
        allergy_data["id"] = allergy_id
        allergy_data["meta"] = {
            "versionId": "1",
            "lastUpdated": datetime.utcnow().isoformat() + "Z"
        }

        db_allergy = AllergyIntolerance(
            id=allergy_id,
            identifier=allergy_data.get("identifier"),
            clinical_status=allergy_data.get("clinicalStatus"),
            verification_status=allergy_data.get("verificationStatus"),
            type=allergy.type,
            category=allergy_data.get("category"),
            criticality=allergy.criticality,
            code=allergy_data.get("code"),
            subject_reference=subject_reference,
            patient_id=patient_id,
            encounter_id=encounter_id,
            onset_datetime=allergy.onsetDateTime,
            onset_age=allergy_data.get("onsetAge"),
            onset_period=allergy_data.get("onsetPeriod"),
            onset_range=allergy_data.get("onsetRange"),
            onset_string=allergy.onsetString,
            recorded_date=allergy.recordedDate,
            recorder=allergy_data.get("recorder"),
            asserter=allergy_data.get("asserter"),
            last_occurrence=allergy.lastOccurrence,
            note=allergy_data.get("note"),
            reaction=allergy_data.get("reaction"),
            meta=allergy_data.get("meta"),
            resource_json=allergy_data
        )
        return self.repository.create(db_allergy)

    def get_by_id(self, allergy_id: str) -> AllergyIntolerance:
        return self.repository.get_by_id_or_404(allergy_id)

    def update(self, allergy_id: str, allergy: AllergyIntoleranceResource) -> AllergyIntolerance:
        db_allergy = self.repository.get_by_id_or_404(allergy_id)
        allergy_data = allergy.model_dump(exclude_none=True, by_alias=True)
        allergy_data["id"] = allergy_id

        current_version = 1
        if db_allergy.meta and "versionId" in db_allergy.meta:
            current_version = int(db_allergy.meta["versionId"]) + 1
        allergy_data["meta"] = {
            "versionId": str(current_version),
            "lastUpdated": datetime.utcnow().isoformat() + "Z"
        }

        db_allergy.clinical_status = allergy_data.get("clinicalStatus")
        db_allergy.verification_status = allergy_data.get("verificationStatus")
        db_allergy.type = allergy.type
        db_allergy.category = allergy_data.get("category")
        db_allergy.criticality = allergy.criticality
        db_allergy.code = allergy_data.get("code")
        db_allergy.note = allergy_data.get("note")
        db_allergy.reaction = allergy_data.get("reaction")
        db_allergy.meta = allergy_data.get("meta")
        db_allergy.resource_json = allergy_data
        return self.repository.update(db_allergy)

    def delete(self, allergy_id: str) -> None:
        self.repository.delete_by_id(allergy_id, "AllergyIntolerance")

    def search(self, patient=None, clinical_status=None, type_filter=None, criticality=None, limit=50):
        patient_id = self._extract_id(patient) if patient else None
        return self.repository.search(
            patient_id=patient_id, clinical_status=clinical_status,
            type_filter=type_filter, criticality=criticality, limit=limit
        )
