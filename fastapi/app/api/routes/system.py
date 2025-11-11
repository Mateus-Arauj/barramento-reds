"""
Rotas de sistema e metadata
"""
from fastapi import APIRouter

router = APIRouter(tags=["System"])


@router.get("/health")
async def health_check():
    """
    Verifica o status do servidor
    """
    return {"status": "ok", "service": "Mini HAPI FHIR Server"}


@router.get("/metadata")
async def get_metadata():
    """
    Retorna CapabilityStatement (simplificado)
    Documenta as capacidades do servidor FHIR
    """
    return {
        "resourceType": "CapabilityStatement",
        "status": "active",
        "date": "2024-01-15",
        "kind": "instance",
        "software": {
            "name": "Mini HAPI",
            "version": "1.0.0"
        },
        "implementation": {
            "description": "Servidor FHIR simplificado - TCC",
            "url": "http://localhost:8000/fhir"
        },
        "fhirVersion": "4.0.1",
        "format": ["application/fhir+json", "application/json"],
        "rest": [
            {
                "mode": "server",
                "resource": [
                    {
                        "type": "Patient",
                        "interaction": [
                            {"code": "read"},
                            {"code": "create"},
                            {"code": "update"},
                            {"code": "delete"},
                            {"code": "search-type"}
                        ],
                        "searchParam": [
                            {"name": "name", "type": "string"},
                            {"name": "gender", "type": "token"},
                            {"name": "birthdate", "type": "date"}
                        ]
                    },
                    {
                        "type": "Observation",
                        "interaction": [
                            {"code": "read"},
                            {"code": "create"},
                            {"code": "search-type"}
                        ],
                        "searchParam": [
                            {"name": "patient", "type": "reference"},
                            {"name": "status", "type": "token"},
                            {"name": "date", "type": "date"}
                        ]
                    }
                ]
            }
        ]
    }
