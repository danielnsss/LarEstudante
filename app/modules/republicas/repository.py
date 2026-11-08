from decimal import Decimal
from sqlalchemy import func
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, selectinload

from app.modules.republicas.models import Republica, Comodidade
from app.modules.republicas.schemas import (
    RepublicaCriar,
    RepublicaAtualizar
)


def buscar_por_id(db: Session, republica_id: int):
    consulta = (
        select(Republica)
        .options(selectinload(Republica.comodidades))
        .where(Republica.id == republica_id)
    )

    return db.scalar(consulta)


def listar_por_locador(db: Session, locador_id: int):
    consulta = (
        select(Republica)
        .options(selectinload(Republica.comodidades))
        .where(Republica.locador_id == locador_id)
        .order_by(Republica.id)
    )

    return db.scalars(consulta).all()


def obter_comodidades(db: Session, nomes: list[str]):
    if not nomes:
        return []

    existentes = db.scalars(
        select(Comodidade).where(Comodidade.nome.in_(nomes))
    ).all()

    por_nome = {item.nome: item for item in existentes}

    for nome in nomes:
        if nome not in por_nome:
            comodidade = Comodidade(nome=nome)
            db.add(comodidade)
            por_nome[nome] = comodidade

    return [por_nome[nome] for nome in nomes]


def criar_republica(
    db: Session,
    dados: RepublicaCriar,
    locador_id: int
):
    valores = dados.model_dump(exclude={"comodidades"})

    republica = Republica(
        **valores,
        locador_id=locador_id
    )

    try:
        republica.comodidades = obter_comodidades(
            db,
            dados.comodidades
        )

        db.add(republica)
        db.commit()
        db.refresh(republica)

        return republica

    except SQLAlchemyError:
        db.rollback()
        raise


def atualizar_republica(
    db: Session,
    republica: Republica,
    dados: RepublicaAtualizar
):
    valores = dados.model_dump(exclude_unset=True)

    try:
        if "comodidades" in valores:
            nomes = valores.pop("comodidades")

            republica.comodidades = obter_comodidades(
                db,
                nomes
            )

        for campo, valor in valores.items():
            setattr(republica, campo, valor)

        db.commit()
        db.refresh(republica)

        return republica

    except SQLAlchemyError:
        db.rollback()
        raise


def excluir_republica(
    db: Session,
    republica: Republica
):
    try:
        db.delete(republica)
        db.commit()

    except SQLAlchemyError:
        db.rollback()
        raise

def buscar_disponiveis(
    db: Session,
    *,
    preco_maximo: Decimal | None,
    localizacao: str | None,
    comodidades: list[str],
    genero_republica: str | None,
    max_moradores: int | None,
    vagas_minimas: int
):
    consulta = (
        select(Republica)
        .options(selectinload(Republica.comodidades))
        .where(
            Republica.vagas_disponiveis >= vagas_minimas
        )
    )

    if preco_maximo is not None:
        consulta = consulta.where(
            Republica.preco <= preco_maximo
        )

    if localizacao is not None:
        consulta = consulta.where(
            Republica.localizacao.icontains(
                localizacao,
                autoescape=True
            )
        )

    if genero_republica is not None:
        consulta = consulta.where(
            func.lower(Republica.genero_republica)
            == genero_republica
        )

    if max_moradores is not None:
        consulta = consulta.where(
            Republica.numero_moradores <= max_moradores
        )

    for nome in comodidades:
        consulta = consulta.where(
            Republica.comodidades.any(
                Comodidade.nome == nome
            )
        )

    consulta = consulta.order_by(Republica.id)

    return db.scalars(consulta).all()
