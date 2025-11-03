import os
from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.responses import JSONResponse
import httpx

API_TOKEN = os.getenv("API_TOKEN", "troque-essa-chave")
FHIR_BASE = os.getenv("FHIR_BASE", "http://hapi:8080/fhir")
app = FastAPI(title="Meu Barramento - Edge API", version="0.1.0")

def check_auth(auth_header: str | None):
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing Bearer token")
    token = auth_header.split(" ", 1)[1]
    if token != API_TOKEN:
        raise HTTPException(status_code=403, detail="Invalid token")

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.api_route("/fhir/{path:path}", methods=["GET","POST","PUT","PATCH","DELETE"])
async def fhir_proxy(path: str, request: Request, authorization: str | None = Header(default=None)):
    # Autorização simples por token (troque depois por OIDC)
    check_auth(authorization)

    # Exemplo: negar recursos não permitidos (simples)
    # if path.startswith("AuditEvent"): ...

    # Repassa a requisição para o HAPI
    target_url = f"{FHIR_BASE.rstrip('/')}/{path}"
    method = request.method
    headers = dict(request.headers)
    # Força content-type fhir quando aplicável
    if "content-type" in headers:
        headers["content-type"] = headers["content-type"].replace("application/json", "application/fhir+json")
    else:
        headers["content-type"] = "application/fhir+json"

    body = await request.body()

    timeout = httpx.Timeout(30.0)
    async with httpx.AsyncClient(timeout=timeout) as client:
        resp = await client.request(method, target_url, headers=headers, content=body, params=dict(request.query_params))
    return JSONResponse(status_code=resp.status_code, content=resp.json() if resp.content else None)
