
import os

from datetime import datetime, timedelta, timezone

import jwt

from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()

JWT_SECRET = os.environ["JWT_SECRET"]
JWT_ALGORITHM = "HS256"
JWT_EXPIRE_MINUTES = int(
    os.environ.get("JWT_EXPIRE_MINUTES", "60")
)


def gerar_hash_senha(senha: str) -> str:
    return password_hash.hash(senha)


def verificar_senha(
    senha: str,
    hash_armazenado: str
) -> bool:
    return password_hash.verify(
        senha,
        hash_armazenado
    )


def criar_token_acesso(usuario_id: int) -> str:
    agora = datetime.now(timezone.utc)

    dados = {
        "sub": str(usuario_id),
        "iat": agora,
        "exp": agora + timedelta(
            minutes=JWT_EXPIRE_MINUTES
        )
    }

    return jwt.encode(
        dados,
        JWT_SECRET,
        algorithm=JWT_ALGORITHM
    )


def decodificar_token(token: str) -> dict:
    return jwt.decode(
        token,
        JWT_SECRET,
        algorithms=[JWT_ALGORITHM],
        options={
            "require": ["sub", "exp"]
        }
    )
