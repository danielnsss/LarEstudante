
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.modules.usuarios.models import Usuario


def buscar_por_email(
    db: Session,
    email: str
) -> Usuario | None:
    consulta = select(Usuario).where(
        Usuario.email == email
    )

    return db.scalar(consulta)


def criar_usuario(
    db: Session,
    nome: str,
    email: str,
    senha_hash: str,
    tipo: str
) -> Usuario:
    usuario = Usuario(
        nome=nome,
        email=email,
        senha_hash=senha_hash,
        tipo=tipo
    )

    db.add(usuario)

    try:
        db.commit()
        db.refresh(usuario)
    except SQLAlchemyError:
        db.rollback()
        raise

    return usuario
