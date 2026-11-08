
from fastapi import (
    Depends,
    HTTPException,
    status
)

from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer
)

from jwt.exceptions import InvalidTokenError
from sqlalchemy.orm import Session

from app.core.security import decodificar_token
from app.database.session import get_db
from app.modules.usuarios.models import Usuario

autenticacao_bearer = HTTPBearer(
    auto_error=False
)


def obter_usuario_atual(
    credenciais: HTTPAuthorizationCredentials | None = Depends(
        autenticacao_bearer
    ),
    db: Session = Depends(get_db)
) -> Usuario:
    erro_autenticacao = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Autenticação inválida ou expirada",
        headers={"WWW-Authenticate": "Bearer"}
    )

    if credenciais is None:
        raise erro_autenticacao

    try:
        dados = decodificar_token(
            credenciais.credentials
        )

        usuario_id = int(dados["sub"])

        if usuario_id <= 0:
            raise ValueError()

    except (
        InvalidTokenError,
        ValueError,
        TypeError,
        KeyError
    ):
        raise erro_autenticacao

    usuario = db.get(
        Usuario,
        usuario_id
    )

    if usuario is None:
        raise erro_autenticacao

    return usuario
