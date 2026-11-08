
from typing import Literal

from pydantic import BaseModel, EmailStr, Field


class LoginDados(BaseModel):
    email: EmailStr
    senha: str = Field(min_length=1)


class TokenResposta(BaseModel):
    access_token: str
    token_type: Literal["bearer"] = "bearer"
