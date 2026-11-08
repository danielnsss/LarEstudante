
from fastapi import APIRouter

from app.modules.autenticacao.router import (
    router as autenticacao_router
)

from app.modules.usuarios.router import (
    router as usuarios_router
)

from app.modules.republicas.router import (
    router as republicas_router
)

api_router = APIRouter()

api_router.include_router(autenticacao_router)
api_router.include_router(usuarios_router)
api_router.include_router(republicas_router)
