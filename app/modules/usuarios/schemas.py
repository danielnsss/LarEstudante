
from typing import Literal

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    field_validator
)


class UsuarioCriar(BaseModel):
    nome: str = Field(min_length=2, max_length=120)
    email: EmailStr = Field(max_length=255)
    senha: str = Field(
        min_length=8,
        max_length=128,
        repr=False
    )
    tipo: Literal["estudante", "locador"]

    @field_validator("nome")
    @classmethod
    def validar_nome(cls, valor: str) -> str:
        nome = valor.strip()

        if len(nome) < 2:
            raise ValueError(
                "O nome deve possuir pelo menos 2 caracteres"
            )

        return nome

    @field_validator("senha")
    @classmethod
    def validar_senha(cls, valor: str) -> str:
        if not valor.strip():
            raise ValueError("A senha não pode estar vazia")

        return valor


class UsuarioResposta(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str
    email: EmailStr
    tipo: Literal["estudante", "locador"]
