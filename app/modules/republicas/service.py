
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.exceptions import (
    RepublicaNaoEncontradaError,
    PermissaoNegadaError,
    ConflitoPersistenciaError
)
from app.modules.usuarios.models import Usuario
from app.modules.republicas import repository
from app.modules.republicas.schemas import (
    RepublicaCriar,
    RepublicaAtualizar
)


def verificar_locador(usuario: Usuario):
    if usuario.tipo != "locador":
        raise PermissaoNegadaError(
            "Apenas locadores podem gerenciar repúblicas"
        )


def consultar_republica(db: Session, republica_id: int):
    republica = repository.buscar_por_id(
        db,
        republica_id
    )

    if republica is None:
        raise RepublicaNaoEncontradaError(
            "República não encontrada"
        )

    return republica


def consultar_republica_do_locador(
    db: Session,
    republica_id: int,
    usuario: Usuario
):
    verificar_locador(usuario)

    republica = consultar_republica(
        db,
        republica_id
    )

    if republica.locador_id != usuario.id:
        raise PermissaoNegadaError(
            "Você não possui permissão para este anúncio"
        )

    return republica


def cadastrar_republica(
    db: Session,
    dados: RepublicaCriar,
    usuario: Usuario
):
    verificar_locador(usuario)

    try:
        return repository.criar_republica(
            db,
            dados,
            usuario.id
        )

    except IntegrityError as erro:
        raise ConflitoPersistenciaError(
            "Conflito ao cadastrar república"
        ) from erro


def listar_minhas_republicas(
    db: Session,
    usuario: Usuario
):
    verificar_locador(usuario)

    return repository.listar_por_locador(
        db,
        usuario.id
    )


def modificar_republica(
    db: Session,
    republica_id: int,
    dados: RepublicaAtualizar,
    usuario: Usuario
):
    republica = consultar_republica_do_locador(
        db,
        republica_id,
        usuario
    )

    try:
        return repository.atualizar_republica(
            db,
            republica,
            dados
        )

    except IntegrityError as erro:
        raise ConflitoPersistenciaError(
            "Conflito ao atualizar república"
        ) from erro


def remover_republica(
    db: Session,
    republica_id: int,
    usuario: Usuario
):
    republica = consultar_republica_do_locador(
        db,
        republica_id,
        usuario
    )

    repository.excluir_republica(
        db,
        republica
    )
