"""
Service para recurso FHIR DiagnosticReport
"""
from datetime import datetime
from fastapi import HTTPException
import uuid

from app.repositories.diagnostic_report import DiagnosticReportRepository
from app.repositories.patient import PatientRepository
from app.models.diagnostic_report import DiagnosticReport
from app.schemas.diagnostic_report import DiagnosticReportResource


class DiagnosticReportService:
    def __init__(self, repository: DiagnosticReportRepository, patient_repository: PatientRepository):
        self.repository = repository
        self.patient_repository = patient_repository

    def _extract_id(self, reference: str) -> str:
        if reference and "/" in reference:
            return reference.split("/")[-1]
        return reference

    def create(self, report: DiagnosticReportResource) -> DiagnosticReport:
        report_id = report.id or str(uuid.uuid4())

        patient_id = None
        subject_reference = None
        if report.subject and report.subject.reference:
            subject_reference = report.subject.reference
            patient_id = self._extract_id(subject_reference)
            patient = self.patient_repository.get_by_id(patient_id)
            if not patient:
                raise HTTPException(status_code=400, detail=f"Patient/{patient_id} not found")

        encounter_id = None
        if report.encounter and report.encounter.reference:
            encounter_id = self._extract_id(report.encounter.reference)

        report_data = report.model_dump(exclude_none=True, by_alias=True)
        report_data["id"] = report_id
        report_data["meta"] = {
            "versionId": "1",
            "lastUpdated": datetime.utcnow().isoformat() + "Z"
        }

        db_report = DiagnosticReport(
            id=report_id,
            identifier=report_data.get("identifier"),
            based_on=report_data.get("basedOn"),
            status=report.status,
            category=report_data.get("category"),
            code=report_data.get("code"),
            subject_reference=subject_reference,
            patient_id=patient_id,
            encounter_id=encounter_id,
            effective_datetime=report.effectiveDateTime,
            effective_period=report_data.get("effectivePeriod"),
            issued=report.issued,
            performer=report_data.get("performer"),
            results_interpreter=report_data.get("resultsInterpreter"),
            specimen=report_data.get("specimen"),
            result=report_data.get("result"),
            imaging_study=report_data.get("imagingStudy"),
            media=report_data.get("media"),
            conclusion=report.conclusion,
            conclusion_code=report_data.get("conclusionCode"),
            presented_form=report_data.get("presentedForm"),
            meta=report_data.get("meta"),
            resource_json=report_data
        )
        return self.repository.create(db_report)

    def get_by_id(self, report_id: str) -> DiagnosticReport:
        return self.repository.get_by_id_or_404(report_id)

    def update(self, report_id: str, report: DiagnosticReportResource) -> DiagnosticReport:
        db_report = self.repository.get_by_id_or_404(report_id)
        report_data = report.model_dump(exclude_none=True, by_alias=True)
        report_data["id"] = report_id

        current_version = 1
        if db_report.meta and "versionId" in db_report.meta:
            current_version = int(db_report.meta["versionId"]) + 1
        report_data["meta"] = {
            "versionId": str(current_version),
            "lastUpdated": datetime.utcnow().isoformat() + "Z"
        }

        db_report.status = report.status
        db_report.category = report_data.get("category")
        db_report.code = report_data.get("code")
        db_report.effective_datetime = report.effectiveDateTime
        db_report.issued = report.issued
        db_report.performer = report_data.get("performer")
        db_report.result = report_data.get("result")
        db_report.conclusion = report.conclusion
        db_report.conclusion_code = report_data.get("conclusionCode")
        db_report.presented_form = report_data.get("presentedForm")
        db_report.meta = report_data.get("meta")
        db_report.resource_json = report_data
        return self.repository.update(db_report)

    def delete(self, report_id: str) -> None:
        self.repository.delete_by_id(report_id, "DiagnosticReport")

    def search(self, patient=None, status=None, code=None, category=None, date=None, limit=50):
        patient_id = self._extract_id(patient) if patient else None
        return self.repository.search(
            patient_id=patient_id, status=status,
            code=code, category=category, date=date, limit=limit
        )
