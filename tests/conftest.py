
import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database.base import Base
from app.database.session import get_db
from app.main import app


@pytest.fixture
def cliente_api():
    engine_teste = create_engine(
        "sqlite+pysqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
    )

    Base.metadata.create_all(bind=engine_teste)

    SessionTeste = sessionmaker(
        bind=engine_teste,
        autoflush=False
    )

    def obter_banco_teste():
        with SessionTeste() as db:
            yield db

    app.dependency_overrides[get_db] = obter_banco_teste

    try:
        with TestClient(app) as cliente:
            yield cliente, SessionTeste
    finally:
        app.dependency_overrides.clear()
        Base.metadata.drop_all(bind=engine_teste)
        engine_teste.dispose()
