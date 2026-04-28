"""
Dependências para injeção de repository, service e autenticação
"""
from fastapi import Header, HTTPException, Depends
from sqlalchemy.orm import Session

from app.config import API_TOKEN
from app.database import get_db

from app.repositories.patient import PatientRepository
from app.repositories.observation import ObservationRepository
from app.repositories.practitioner import PractitionerRepository
from app.repositories.encounter import EncounterRepository
from app.repositories.organization import OrganizationRepository
from app.repositories.location import LocationRepository
from app.repositories.condition import ConditionRepository
from app.repositories.procedure import ProcedureRepository
from app.repositories.allergy_intolerance import AllergyIntoleranceRepository
from app.repositories.diagnostic_report import DiagnosticReportRepository
from app.repositories.immunization import ImmunizationRepository

from app.services.patient import PatientService
from app.services.observation import ObservationService
from app.services.practitioner import PractitionerService
from app.services.encounter import EncounterService
from app.services.organization import OrganizationService
from app.services.location import LocationService
from app.services.condition import ConditionService
from app.services.procedure import ProcedureService
from app.services.allergy_intolerance import AllergyIntoleranceService
from app.services.diagnostic_report import DiagnosticReportService
from app.services.immunization import ImmunizationService


def check_auth(authorization: str | None = Header(default=None)):
    """
    Valida o token de autorização Bearer
    """
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing Bearer token")
    token = authorization.split(" ", 1)[1]
    if token != API_TOKEN:
        raise HTTPException(status_code=403, detail="Invalid token")
    return True


# ===========================================================================
# Repository factories
# ===========================================================================

def get_patient_repository(db: Session = Depends(get_db)) -> PatientRepository:
    return PatientRepository(db)


def get_observation_repository(db: Session = Depends(get_db)) -> ObservationRepository:
    return ObservationRepository(db)


def get_practitioner_repository(db: Session = Depends(get_db)) -> PractitionerRepository:
    return PractitionerRepository(db)


def get_encounter_repository(db: Session = Depends(get_db)) -> EncounterRepository:
    return EncounterRepository(db)


def get_organization_repository(db: Session = Depends(get_db)) -> OrganizationRepository:
    return OrganizationRepository(db)


def get_location_repository(db: Session = Depends(get_db)) -> LocationRepository:
    return LocationRepository(db)


def get_condition_repository(db: Session = Depends(get_db)) -> ConditionRepository:
    return ConditionRepository(db)


def get_procedure_repository(db: Session = Depends(get_db)) -> ProcedureRepository:
    return ProcedureRepository(db)


def get_allergy_intolerance_repository(db: Session = Depends(get_db)) -> AllergyIntoleranceRepository:
    return AllergyIntoleranceRepository(db)


def get_diagnostic_report_repository(db: Session = Depends(get_db)) -> DiagnosticReportRepository:
    return DiagnosticReportRepository(db)


def get_immunization_repository(db: Session = Depends(get_db)) -> ImmunizationRepository:
    return ImmunizationRepository(db)


# ===========================================================================
# Service factories
# ===========================================================================

def get_patient_service(
    repository: PatientRepository = Depends(get_patient_repository)
) -> PatientService:
    return PatientService(repository)


def get_observation_service(
    repository: ObservationRepository = Depends(get_observation_repository),
    patient_repository: PatientRepository = Depends(get_patient_repository)
) -> ObservationService:
    return ObservationService(repository, patient_repository)


def get_practitioner_service(
    repository: PractitionerRepository = Depends(get_practitioner_repository)
) -> PractitionerService:
    return PractitionerService(repository)


def get_encounter_service(
    repository: EncounterRepository = Depends(get_encounter_repository),
    patient_repository: PatientRepository = Depends(get_patient_repository),
    practitioner_repository: PractitionerRepository = Depends(get_practitioner_repository)
) -> EncounterService:
    return EncounterService(repository, patient_repository, practitioner_repository)


def get_organization_service(
    repository: OrganizationRepository = Depends(get_organization_repository)
) -> OrganizationService:
    return OrganizationService(repository)


def get_location_service(
    repository: LocationRepository = Depends(get_location_repository)
) -> LocationService:
    return LocationService(repository)


def get_condition_service(
    repository: ConditionRepository = Depends(get_condition_repository),
    patient_repository: PatientRepository = Depends(get_patient_repository)
) -> ConditionService:
    return ConditionService(repository, patient_repository)


def get_procedure_service(
    repository: ProcedureRepository = Depends(get_procedure_repository),
    patient_repository: PatientRepository = Depends(get_patient_repository)
) -> ProcedureService:
    return ProcedureService(repository, patient_repository)


def get_allergy_intolerance_service(
    repository: AllergyIntoleranceRepository = Depends(get_allergy_intolerance_repository),
    patient_repository: PatientRepository = Depends(get_patient_repository)
) -> AllergyIntoleranceService:
    return AllergyIntoleranceService(repository, patient_repository)


def get_diagnostic_report_service(
    repository: DiagnosticReportRepository = Depends(get_diagnostic_report_repository),
    patient_repository: PatientRepository = Depends(get_patient_repository)
) -> DiagnosticReportService:
    return DiagnosticReportService(repository, patient_repository)


def get_immunization_service(
    repository: ImmunizationRepository = Depends(get_immunization_repository),
    patient_repository: PatientRepository = Depends(get_patient_repository)
) -> ImmunizationService:
    return ImmunizationService(repository, patient_repository)
