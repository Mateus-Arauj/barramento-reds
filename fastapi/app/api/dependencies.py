"""
Dependências para autenticação e validação
"""
from fastapi import Header, HTTPException

from app.config import API_TOKEN


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
