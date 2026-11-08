
from __future__ import annotations

from decimal import Decimal

from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Republica(Base):
    __tablename__ = "republicas"

    __table_args__ = (
        CheckConstraint("preco > 0", name="ck_republicas_preco"),
        CheckConstraint(
            "numero_moradores >= 0",
            name="ck_republicas_moradores"
        ),
        CheckConstraint(
            "vagas_disponiveis >= 0",
            name="ck_republicas_vagas"
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    locador_id: Mapped[int] = mapped_column(
        ForeignKey("usuarios.id"), nullable=False
    )
    titulo: Mapped[str] = mapped_column(
        String(150), nullable=False
    )
    descricao: Mapped[str | None] = mapped_column(
        Text, nullable=True
    )
    preco: Mapped[Decimal] = mapped_column(
        Numeric(10, 2), nullable=False
    )
    localizacao: Mapped[str] = mapped_column(
        String(250), nullable=False
    )
    genero_republica: Mapped[str] = mapped_column(
        String(50), nullable=False
    )
    numero_moradores: Mapped[int] = mapped_column(
        Integer, nullable=False
    )
    vagas_disponiveis: Mapped[int] = mapped_column(
        Integer, nullable=False
    )

    locador: Mapped[Usuario] = relationship(
        back_populates="republicas"
    )
    comodidades: Mapped[list[Comodidade]] = relationship(
        secondary="republica_comodidades",
        back_populates="republicas"
    )


class Comodidade(Base):
    __tablename__ = "comodidades"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(
        String(100), unique=True, nullable=False
    )

    republicas: Mapped[list[Republica]] = relationship(
        secondary="republica_comodidades",
        back_populates="comodidades"
    )


class RepublicaComodidade(Base):
    __tablename__ = "republica_comodidades"

    republica_id: Mapped[int] = mapped_column(
        ForeignKey("republicas.id", ondelete="CASCADE"),
        primary_key=True
    )
    comodidade_id: Mapped[int] = mapped_column(
        ForeignKey("comodidades.id", ondelete="CASCADE"),
        primary_key=True
    )
