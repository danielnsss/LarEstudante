
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)

from sqlalchemy.orm import Session

from app.core.security import criar_token_acesso
from app.database.session import get_db
from app.modules.autenticacao import service
from app.modules.autenticacao.schemas import (
    LoginDados,
    TokenResposta
)

router = APIRouter(
    tags=["Autenticação"]
)


@router.post(
    "/login",
    response_model=TokenResposta
)
def realizar_login(
    dados: LoginDados,
    db: Session = Depends(get_db)
):
    usuario = service.autenticar_usuario(
        db=db,
        email=str(dados.email),
        senha=dados.senha
    )

    if usuario is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"}
        )

    token = criar_token_acesso(usuario.id)

    return TokenResposta(
        access_token=token
    )
