
from sqlalchemy.orm import Session

from app.core.security import verificar_senha
from app.modules.usuarios import repository
from app.modules.usuarios.models import Usuario


def autenticar_usuario(
    db: Session,
    email: str,
    senha: str
) -> Usuario | None:
    email_normalizado = email.strip().lower()

    usuario = repository.buscar_por_email(
        db,
        email_normalizado
    )

    if usuario is None:
        return None

    if not verificar_senha(
        senha,
        usuario.senha_hash
    ):
        return None

    return usuario
