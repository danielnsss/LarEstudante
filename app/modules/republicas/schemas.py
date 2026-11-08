
from decimal import Decimal

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
    model_validator
)


def normalizar_comodidades(valores: list[str]) -> list[str]:
    resultado = []

    for valor in valores:
        nome = valor.strip().casefold()

        if not nome or len(nome) > 100:
            raise ValueError("Comodidade inválida")

        if nome not in resultado:
            resultado.append(nome)

    return resultado


class RepublicaCriar(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True
    )

    titulo: str = Field(min_length=3, max_length=150)
    descricao: str | None = Field(default=None, max_length=2000)
    preco: Decimal = Field(
        gt=0,
        max_digits=10,
        decimal_places=2
    )
    localizacao: str = Field(min_length=3, max_length=250)
    genero_republica: str = Field(min_length=2, max_length=50)
    numero_moradores: int = Field(ge=0)
    vagas_disponiveis: int = Field(ge=0)
    comodidades: list[str] = Field(
        default_factory=list,
        max_length=20
    )

    @field_validator("comodidades")
    @classmethod
    def validar_comodidades(cls, valores: list[str]) -> list[str]:
        return normalizar_comodidades(valores)


class RepublicaAtualizar(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True
    )

    titulo: str | None = Field(
        default=None, min_length=3, max_length=150
    )
    descricao: str | None = Field(
        default=None, max_length=2000
    )
    preco: Decimal | None = Field(
        default=None, gt=0, max_digits=10, decimal_places=2
    )
    localizacao: str | None = Field(
        default=None, min_length=3, max_length=250
    )
    genero_republica: str | None = Field(
        default=None, min_length=2, max_length=50
    )
    numero_moradores: int | None = Field(default=None, ge=0)
    vagas_disponiveis: int | None = Field(default=None, ge=0)
    comodidades: list[str] | None = Field(
        default=None, max_length=20
    )

    @field_validator("comodidades")
    @classmethod
    def validar_comodidades(
        cls,
        valores: list[str] | None
    ) -> list[str] | None:
        if valores is None:
            return None

        return normalizar_comodidades(valores)

    @model_validator(mode="after")
    def validar_atualizacao(self):
        campos = self.model_fields_set

        if not campos:
            raise ValueError("Informe pelo menos um campo")

        for campo in campos:
            if campo != "descricao" and getattr(self, campo) is None:
                raise ValueError(
                    f"O campo {campo} não pode ser nulo"
                )

        return self


class ComodidadeResposta(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str


class RepublicaResposta(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    locador_id: int
    titulo: str
    descricao: str | None
    preco: Decimal
    localizacao: str
    genero_republica: str
    numero_moradores: int
    vagas_disponiveis: int
    comodidades: list[ComodidadeResposta]
