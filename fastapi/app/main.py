"""
Mini HAPI - Servidor FHIR simplificado usando FastAPI
Implementa endpoints para Patient e Observation
"""
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

from app.database import init_db
from app.models import Patient, Observation, Practitioner, Encounter
from app.api.routes import system, patient, observation, practitioner, encounter


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gerencia o ciclo de vida da aplicação
    Inicializa o banco de dados na startup
    """
    print("🚀 Iniciando Mini HAPI Server...")
    init_db()
    print("✓ Banco de dados inicializado")
    yield
    print("👋 Encerrando Mini HAPI Server...")


app = FastAPI(
    title="Mini HAPI - FHIR Server",
    description="Servidor FHIR simplificado com suporte a Patient e Observation",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(system.router)
app.include_router(patient.router)
app.include_router(observation.router)
app.include_router(practitioner.router)
app.include_router(encounter.router)


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
                    "diagnostics": f"Recurso '{path}' não implementado no Mini HAPI. Recursos suportados: Patient, Observation, Practitioner, Encounter"
                }
            ]
        }
    )
