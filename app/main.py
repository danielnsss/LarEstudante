from fastapi.staticfiles import StaticFiles
from fastapi import Request
from fastapi.responses import JSONResponse

from app.core.exceptions import (
    RepublicaNaoEncontradaError,
    PermissaoNegadaError,
    ConflitoPersistenciaError
)

from fastapi import FastAPI, HTTPException
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.modules.republicas import models as republicas_models
from app.api.router import api_router
from app.database.session import engine

app = FastAPI(
    title="LarEstudante API",
    description="Backend da plataforma web LarEstudante",
    version="1.0.0"
)

app.include_router(api_router)


@app.get("/")
def inicio():
    return {
        "mensagem": "API LarEstudante em execução"
    }


@app.get("/saude")
def verificar_banco():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

    except SQLAlchemyError:
        raise HTTPException(
            status_code=503,
            detail="Banco de dados indisponível"
        )

    return {
        "api": "funcionando",
        "banco": "conectado"
    }

@app.exception_handler(RepublicaNaoEncontradaError)
async def tratar_republica_nao_encontrada(
    request: Request,
    erro: RepublicaNaoEncontradaError
):
    return JSONResponse(
        status_code=404,
        content={"detail": str(erro)}
    )


@app.exception_handler(PermissaoNegadaError)
async def tratar_permissao_negada(
    request: Request,
    erro: PermissaoNegadaError
):
    return JSONResponse(
        status_code=403,
        content={"detail": str(erro)}
    )


@app.exception_handler(ConflitoPersistenciaError)
async def tratar_conflito_persistencia(
    request: Request,
    erro: ConflitoPersistenciaError
):
    return JSONResponse(
        status_code=409,
        content={"detail": str(erro)}
    )
app.mount(
    "/web",
    StaticFiles(directory="frontend", html=True),
    name="frontend"
)