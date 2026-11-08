
from sqlalchemy.orm import Session

from app.modules.busca.schemas import FiltrosBusca
from app.modules.republicas import repository


def pesquisar_republicas(
    db: Session,
    filtros: FiltrosBusca
):
    return repository.buscar_disponiveis(
        db=db,
        preco_maximo=filtros.preco_maximo,
        localizacao=filtros.localizacao,
        comodidades=filtros.comodidades,
        genero_republica=filtros.genero_republica,
        max_moradores=filtros.max_moradores,
        vagas_minimas=filtros.vagas_minimas
    )
