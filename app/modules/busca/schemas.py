
from decimal import Decimal

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator
)

from app.modules.republicas.schemas import normalizar_comodidades


class FiltrosBusca(BaseModel):
    model_config = ConfigDict(extra="forbid")

    preco_maximo: Decimal | None = Field(
        default=None,
        gt=0,
        max_digits=10,
        decimal_places=2
    )

    localizacao: str | None = Field(
        default=None,
        min_length=1,
        max_length=250
    )

    comodidades: list[str] = Field(
        default_factory=list,
        max_length=20
    )

    genero_republica: str | None = Field(
        default=None,
        min_length=2,
        max_length=50
    )

    max_moradores: int | None = Field(
        default=None,
        ge=0
    )

    vagas_minimas: int = Field(
        default=1,
        ge=1
    )

    @field_validator("localizacao", "genero_republica")
    @classmethod
    def normalizar_texto(
        cls,
        valor: str | None
    ) -> str | None:
        if valor is None:
            return None

        valor = valor.strip()

        if not valor:
            raise ValueError("O filtro não pode estar vazio")

        return valor.casefold()

    @field_validator("comodidades")
    @classmethod
    def validar_comodidades(
        cls,
        valores: list[str]
    ) -> list[str]:
        return normalizar_comodidades(valores)
