from app.api.dependencies import obter_usuario_atual
from app.modules.usuarios.models import Usuario
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.exceptions import EmailJaCadastradoError
from app.database.session import get_db
from app.modules.usuarios import service
from app.modules.usuarios.schemas import (
    UsuarioCriar,
    UsuarioResposta
)

router = APIRouter(
    prefix="/usuarios",
    tags=["Usuários"]
)


@router.post(
    "",
    response_model=UsuarioResposta,
    status_code=status.HTTP_201_CREATED
)
def cadastrar_usuario(
    dados: UsuarioCriar,
    db: Session = Depends(get_db)
):
    try:
        return service.cadastrar_usuario(db, dados)
    except EmailJaCadastradoError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="E-mail já cadastrado"
        )

@router.get(
    "/me",
    response_model=UsuarioResposta
)
def consultar_meu_perfil(
    usuario: Usuario = Depends(obter_usuario_atual)
):
    return usuario
