
from __future__ import annotations

from sqlalchemy import CheckConstraint, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    __table_args__ = (
        CheckConstraint(
            "tipo IN ('estudante', 'locador')",
            name="ck_usuarios_tipo"
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(
        String(255), unique=True, index=True, nullable=False
    )
    senha_hash: Mapped[str] = mapped_column(
        String(255), nullable=False
    )
    tipo: Mapped[str] = mapped_column(
        String(15), nullable=False
    )

    republicas: Mapped[list[Republica]] = relationship(
        back_populates="locador"
    )
