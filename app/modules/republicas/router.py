
from fastapi import (
    APIRouter,
    Depends,
    Path,
    status
)

from sqlalchemy.orm import Session

from app.api.dependencies import obter_usuario_atual
from app.database.session import get_db
from app.modules.usuarios.models import Usuario
from app.modules.republicas import service
from app.modules.republicas.schemas import (
    RepublicaCriar,
    RepublicaAtualizar,
    RepublicaResposta
)

router = APIRouter(
    prefix="/republicas",
    tags=["Repúblicas"]
)


@router.post(
    "",
    response_model=RepublicaResposta,
    status_code=status.HTTP_201_CREATED
)
def cadastrar_republica(
    dados: RepublicaCriar,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(obter_usuario_atual)
):
    return service.cadastrar_republica(
        db,
        dados,
        usuario
    )


@router.get(
    "/minhas",
    response_model=list[RepublicaResposta]
)
def listar_minhas_republicas(
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(obter_usuario_atual)
):
    return service.listar_minhas_republicas(
        db,
        usuario
    )


@router.get(
    "/{republica_id}",
    response_model=RepublicaResposta
)
def consultar_republica(
    republica_id: int = Path(ge=1),
    db: Session = Depends(get_db)
):
    return service.consultar_republica(
        db,
        republica_id
    )


@router.patch(
    "/{republica_id}",
    response_model=RepublicaResposta
)
def atualizar_republica(
    dados: RepublicaAtualizar,
    republica_id: int = Path(ge=1),
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(obter_usuario_atual)
):
    return service.modificar_republica(
        db,
        republica_id,
        dados,
        usuario
    )


@router.delete(
    "/{republica_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def excluir_republica(
    republica_id: int = Path(ge=1),
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(obter_usuario_atual)
):
    service.remover_republica(
        db,
        republica_id,
        usuario
    )
