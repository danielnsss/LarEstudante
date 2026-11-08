
from datetime import datetime, timedelta, timezone

import jwt

from app.core.security import JWT_SECRET


def criar_usuario_teste(cliente):
    resposta = cliente.post(
        "/usuarios",
        json={
            "nome": "Estudante Teste",
            "email": "login@example.com",
            "senha": "Teste1234!",
            "tipo": "estudante"
        }
    )

    assert resposta.status_code == 201

    return resposta.json()


def test_login_sucesso(cliente_api):
    cliente, _ = cliente_api

    usuario = criar_usuario_teste(cliente)

    resposta = cliente.post(
        "/login",
        json={
            "email": "login@example.com",
            "senha": "Teste1234!"
        }
    )

    assert resposta.status_code == 200

    dados = resposta.json()

    assert dados["token_type"] == "bearer"
    assert dados["access_token"]

    resposta_perfil = cliente.get(
        "/usuarios/me",
        headers={
            "Authorization": f"Bearer {dados['access_token']}"
        }
    )

    assert resposta_perfil.status_code == 200
    assert resposta_perfil.json()["id"] == usuario["id"]
    assert resposta_perfil.json()["email"] == "login@example.com"
    assert "senha_hash" not in resposta_perfil.json()


def test_login_senha_incorreta(cliente_api):
    cliente, _ = cliente_api

    criar_usuario_teste(cliente)

    resposta = cliente.post(
        "/login",
        json={
            "email": "login@example.com",
            "senha": "SenhaIncorreta123!"
        }
    )

    assert resposta.status_code == 401


def test_login_usuario_inexistente(cliente_api):
    cliente, _ = cliente_api

    resposta = cliente.post(
        "/login",
        json={
            "email": "inexistente@example.com",
            "senha": "Teste1234!"
        }
    )

    assert resposta.status_code == 401


def test_acesso_sem_token(cliente_api):
    cliente, _ = cliente_api

    resposta = cliente.get("/usuarios/me")

    assert resposta.status_code == 401


def test_token_invalido(cliente_api):
    cliente, _ = cliente_api

    resposta = cliente.get(
        "/usuarios/me",
        headers={
            "Authorization": "Bearer token.invalido.teste"
        }
    )

    assert resposta.status_code == 401


def test_token_expirado(cliente_api):
    cliente, _ = cliente_api

    usuario = criar_usuario_teste(cliente)

    token_expirado = jwt.encode(
        {
            "sub": str(usuario["id"]),
            "exp": datetime.now(timezone.utc) - timedelta(minutes=1)
        },
        JWT_SECRET,
        algorithm="HS256"
    )

    resposta = cliente.get(
        "/usuarios/me",
        headers={
            "Authorization": f"Bearer {token_expirado}"
        }
    )

    assert resposta.status_code == 401
