"""
Mini HAPI - Servidor FHIR simplificado usando FastAPI
Implementa recursos FHIR conforme BR Core (perfil brasileiro)
"""
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

from app.database import init_db
from app.models import (
    Patient, Observation, Practitioner, Encounter,
    Organization, Location, Condition, Procedure,
    AllergyIntolerance, DiagnosticReport, Immunization
)
from app.api.routes import (
    system, patient, observation, practitioner, encounter,
    organization, location, condition, procedure,
    allergy_intolerance, diagnostic_report, immunization
)


SUPPORTED_RESOURCES = [
    "Patient", "Observation", "Practitioner", "Encounter",
    "Organization", "Location", "Condition", "Procedure",
    "AllergyIntolerance", "DiagnosticReport", "Immunization"
]


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gerencia o ciclo de vida da aplicação
    Inicializa o banco de dados na startup
    """
    print("🚀 Iniciando Mini HAPI Server (BR Core)...")
    init_db()
    print("✓ Banco de dados inicializado")
    print(f"✓ Recursos FHIR suportados: {', '.join(SUPPORTED_RESOURCES)}")
    yield
    print("👋 Encerrando Mini HAPI Server...")


app = FastAPI(
    title="Mini HAPI - FHIR Server (BR Core)",
    description="Servidor FHIR simplificado com perfil brasileiro (BR Core). "
                "Suporta Patient, Observation, Practitioner, Encounter, "
                "Organization, Location, Condition, Procedure, "
                "AllergyIntolerance, DiagnosticReport e Immunization.",
    version="2.0.0",
    lifespan=lifespan
)

# Recursos existentes
app.include_router(system.router)
app.include_router(patient.router)
app.include_router(observation.router)
app.include_router(practitioner.router)
app.include_router(encounter.router)

# Novos recursos BR Core
app.include_router(organization.router)
app.include_router(location.router)
app.include_router(condition.router)
app.include_router(procedure.router)
app.include_router(allergy_intolerance.router)
app.include_router(diagnostic_report.router)
app.include_router(immunization.router)


@app.api_route("/fhir/{path:path}",
               methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
               include_in_schema=False)
async def fhir_fallback(path: str):
    """
    Endpoint de fallback para recursos não implementados
    Retorna uma mensagem informativa
    """
    return JSONResponse(
        status_code=501,
        content={
            "resourceType": "OperationOutcome",
            "issue": [
                {
                    "severity": "error",
                    "code": "not-supported",
                    "diagnostics": f"Recurso '{path}' não implementado no Mini HAPI. Recursos suportados: {', '.join(SUPPORTED_RESOURCES)}"
                }
            ]
        }
    )
