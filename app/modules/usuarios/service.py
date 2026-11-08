
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.exceptions import EmailJaCadastradoError
from app.core.security import gerar_hash_senha
from app.modules.usuarios import repository
from app.modules.usuarios.schemas import UsuarioCriar
from app.modules.usuarios.models import Usuario


def cadastrar_usuario(
    db: Session,
    dados: UsuarioCriar
) -> Usuario:
    email = str(dados.email).strip().lower()

    usuario_existente = repository.buscar_por_email(
        db,
        email
    )

    if usuario_existente is not None:
        raise EmailJaCadastradoError()

    senha_hash = gerar_hash_senha(dados.senha)

    try:
        return repository.criar_usuario(
            db=db,
            nome=dados.nome,
            email=email,
            senha_hash=senha_hash,
            tipo=dados.tipo
        )
    except IntegrityError as erro:
        if repository.buscar_por_email(db, email) is not None:
            raise EmailJaCadastradoError() from erro

        raise
