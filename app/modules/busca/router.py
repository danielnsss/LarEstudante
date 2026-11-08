
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.modules.busca import service
from app.modules.busca.schemas import FiltrosBusca
from app.modules.republicas.schemas import RepublicaResposta

router = APIRouter(
    prefix="/republicas",
    tags=["Busca e Filtros"]
)


@router.get(
    "",
    response_model=list[RepublicaResposta]
)
def pesquisar_republicas(
    filtros: Annotated[FiltrosBusca, Query()],
    db: Session = Depends(get_db)
):
    return service.pesquisar_republicas(
        db,
        filtros
    )
