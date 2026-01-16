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

from app.services.patient import PatientService
from app.services.observation import ObservationService
from app.services.practitioner import PractitionerService
from app.services.encounter import EncounterService


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


def get_patient_repository(db: Session = Depends(get_db)) -> PatientRepository:
    """
    Injeta PatientRepository
    """
    return PatientRepository(db)


def get_observation_repository(db: Session = Depends(get_db)) -> ObservationRepository:
    """
    Injeta ObservationRepository
    """
    return ObservationRepository(db)


def get_practitioner_repository(db: Session = Depends(get_db)) -> PractitionerRepository:
    """
    Injeta PractitionerRepository
    """
    return PractitionerRepository(db)


def get_encounter_repository(db: Session = Depends(get_db)) -> EncounterRepository:
    """
    Injeta EncounterRepository
    """
    return EncounterRepository(db)


def get_patient_service(
    repository: PatientRepository = Depends(get_patient_repository)
) -> PatientService:
    """
    Injeta PatientService com repository
    """
    return PatientService(repository)


def get_observation_service(
    repository: ObservationRepository = Depends(get_observation_repository),
    patient_repository: PatientRepository = Depends(get_patient_repository)
) -> ObservationService:
    """
    Injeta ObservationService com repositories
    """
    return ObservationService(repository, patient_repository)


def get_practitioner_service(
    repository: PractitionerRepository = Depends(get_practitioner_repository)
) -> PractitionerService:
    """
    Injeta PractitionerService com repository
    """
    return PractitionerService(repository)


def get_encounter_service(
    repository: EncounterRepository = Depends(get_encounter_repository),
    patient_repository: PatientRepository = Depends(get_patient_repository),
    practitioner_repository: PractitionerRepository = Depends(get_practitioner_repository)
) -> EncounterService:
    """
    Injeta EncounterService com repositories
    """
    return EncounterService(repository, patient_repository, practitioner_repository)
