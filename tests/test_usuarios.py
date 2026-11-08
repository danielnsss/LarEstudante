
from sqlalchemy import select

from app.core.security import verificar_senha
from app.modules.usuarios.models import Usuario


def dados_validos():
    return {
        "nome": "Estudante Exemplo",
        "email": "estudante@example.com",
        "senha": "Teste1234!",
        "tipo": "estudante"
    }


def test_cadastro_usuario(cliente_api):
    cliente, fabrica_sessao = cliente_api

    resposta = cliente.post(
        "/usuarios",
        json=dados_validos()
    )

    assert resposta.status_code == 201

    dados = resposta.json()

    assert dados["nome"] == "Estudante Exemplo"
    assert dados["tipo"] == "estudante"
    assert "senha" not in dados
    assert "senha_hash" not in dados

    with fabrica_sessao() as db:
        usuario = db.scalar(
            select(Usuario).where(
                Usuario.email == "estudante@example.com"
            )
        )

        assert usuario is not None
        assert usuario.senha_hash != "Teste1234!"
        assert verificar_senha(
            "Teste1234!",
            usuario.senha_hash
        )


def test_email_duplicado(cliente_api):
    cliente, _ = cliente_api

    dados = dados_validos()

    primeira = cliente.post("/usuarios", json=dados)

    assert primeira.status_code == 201

    dados["email"] = "ESTUDANTE@EXAMPLE.COM"

    segunda = cliente.post("/usuarios", json=dados)

    assert segunda.status_code == 409


def test_email_invalido(cliente_api):
    cliente, _ = cliente_api

    dados = dados_validos()
    dados["email"] = "email-invalido"

    resposta = cliente.post("/usuarios", json=dados)

    assert resposta.status_code == 422


def test_tipo_invalido(cliente_api):
    cliente, _ = cliente_api

    dados = dados_validos()
    dados["tipo"] = "administrador"

    resposta = cliente.post("/usuarios", json=dados)

    assert resposta.status_code == 422
