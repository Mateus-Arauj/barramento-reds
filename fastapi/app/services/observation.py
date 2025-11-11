"""
Serviço para manipulação de recursos FHIR Observation
"""
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from typing import Optional
import uuid
from datetime import datetime

from app.models.database import Patient, Observation
from app.schemas.observation import ObservationResource


class ObservationService:
    """
    Serviço para operações com Observation
    """
    
    @staticmethod
    def create_observation(db: Session, observation_data: ObservationResource) -> Observation:
        """
        Cria um novo recurso Observation no banco de dados
        """
        if not observation_data.id:
            observation_data.id = str(uuid.uuid4())
        
        if not observation_data.meta:
            observation_data.meta = {}
        
        observation_dict = observation_data.model_dump(exclude_none=True)
        observation_dict['meta'] = observation_dict.get('meta', {})
        observation_dict['meta']['versionId'] = '1'
        observation_dict['meta']['lastUpdated'] = datetime.utcnow().isoformat() + 'Z'
        
        patient_id = None
        subject_reference = None
        if observation_data.subject and observation_data.subject.reference:
            subject_reference = observation_data.subject.reference
            if subject_reference.startswith("Patient/"):
                patient_id = subject_reference.split("/", 1)[1]
                
                patient_exists = db.query(Patient).filter(Patient.id == patient_id).first()
                if not patient_exists:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Referenced patient {subject_reference} does not exist"
                    )
        
        db_observation = Observation(
            id=observation_data.id,
            identifier=observation_dict.get('identifier'),
            status=observation_dict.get('status'),
            category=observation_dict.get('category'),
            code=observation_dict.get('code'),
            subject_reference=subject_reference,
            patient_id=patient_id,
            effective_datetime=observation_dict.get('effectiveDateTime'),
            effective_period=observation_dict.get('effectivePeriod'),
            issued=observation_dict.get('issued'),
            value_quantity=observation_dict.get('valueQuantity'),
            value_codeable_concept=observation_dict.get('valueCodeableConcept'),
            value_string=observation_dict.get('valueString'),
            value_boolean=str(observation_dict.get('valueBoolean', '')).lower() if observation_dict.get('valueBoolean') is not None else None,
            value_integer=observation_dict.get('valueInteger'),
            value_range=observation_dict.get('valueRange'),
            value_ratio=observation_dict.get('valueRatio'),
            value_sampled_data=observation_dict.get('valueSampledData'),
            value_time=observation_dict.get('valueTime'),
            value_datetime=observation_dict.get('valueDateTime'),
            value_period=observation_dict.get('valuePeriod'),
            interpretation=observation_dict.get('interpretation'),
            note=observation_dict.get('note'),
            meta=observation_dict['meta'],
            resource_json=observation_dict
        )
        
        try:
            db.add(db_observation)
            db.commit()
            db.refresh(db_observation)
            return db_observation
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=409,
                detail=f"Observation with id {observation_data.id} already exists"
            )
    
    @staticmethod
    def get_observation(db: Session, observation_id: str) -> Optional[Observation]:
        """
        Busca uma Observation por ID
        """
        observation = db.query(Observation).filter(Observation.id == observation_id).first()
        if not observation:
            raise HTTPException(status_code=404, detail=f"Observation/{observation_id} not found")
        return observation
    
    @staticmethod
    def search_observations(
        db: Session,
        patient: Optional[str] = None,
        status: Optional[str] = None,
        date: Optional[str] = None,
        limit: int = 50
    ) -> list[Observation]:
        """
        Busca Observations com filtros
        """
        query = db.query(Observation)
        
        if patient:
            if not patient.startswith("Patient/"):
                patient = f"Patient/{patient}"
            query = query.filter(Observation.subject_reference == patient)
        
        if status:
            query = query.filter(Observation.status == status)
        
        if date:
            query = query.filter(Observation.effective_datetime.like(f"{date}%"))
        
        return query.limit(limit).all()
