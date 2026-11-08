
import pytest


@pytest.fixture
def cenario_busca(cliente_api):
    cliente, _ = cliente_api

    cadastro = cliente.post(
        "/usuarios",
        json={
            "nome": "Locador Teste",
            "email": "busca@example.com",
            "senha": "Teste1234!",
            "tipo": "locador"
        }
    )

    assert cadastro.status_code == 201

    login = cliente.post(
        "/login",
        json={
            "email": "busca@example.com",
            "senha": "Teste1234!"
        }
    )

    assert login.status_code == 200

    headers = {
        "Authorization": (
            f"Bearer {login.json()['access_token']}"
        )
    }

    republicas = [
        {
            "titulo": "Republica Centro",
            "descricao": "Moradia no centro.",
            "preco": "650.00",
            "localizacao": "Picos - PI",
            "genero_republica": "mista",
            "numero_moradores": 3,
            "vagas_disponiveis": 2,
            "comodidades": ["Wi-Fi", "Lavanderia"]
        },
        {
            "titulo": "Republica Norte",
            "descricao": "Moradia na zona norte.",
            "preco": "750.00",
            "localizacao": "Picos - PI",
            "genero_republica": "masculina",
            "numero_moradores": 1,
            "vagas_disponiveis": 3,
            "comodidades": ["Wi-Fi", "Garagem"]
        },
        {
            "titulo": "Republica Teresina",
            "descricao": "Moradia estudantil.",
            "preco": "950.00",
            "localizacao": "Teresina - PI",
            "genero_republica": "feminina",
            "numero_moradores": 5,
            "vagas_disponiveis": 1,
            "comodidades": ["Wi-Fi", "Garagem"]
        },
        {
            "titulo": "Republica Sem Vagas",
            "descricao": "Todas as vagas ocupadas.",
            "preco": "500.00",
            "localizacao": "Picos - PI",
            "genero_republica": "mista",
            "numero_moradores": 2,
            "vagas_disponiveis": 0,
            "comodidades": ["Wi-Fi"]
        }
    ]

    for dados in republicas:
        resposta = cliente.post(
            "/republicas",
            json=dados,
            headers=headers
        )

        assert resposta.status_code == 201, resposta.text

    return cliente


def test_lista_apenas_disponiveis(cenario_busca):
    resposta = cenario_busca.get("/republicas")

    assert resposta.status_code == 200
    assert len(resposta.json()) == 3

    titulos = [
        item["titulo"] for item in resposta.json()
    ]

    assert "Republica Sem Vagas" not in titulos


def test_filtro_preco(cenario_busca):
    resposta = cenario_busca.get(
        "/republicas",
        params={"preco_maximo": "700.00"}
    )

    assert resposta.status_code == 200
    assert len(resposta.json()) == 1
    assert resposta.json()[0]["titulo"] == "Republica Centro"


def test_filtro_localizacao(cenario_busca):
    resposta = cenario_busca.get(
        "/republicas",
        params={"localizacao": "pIcOs"}
    )

    assert resposta.status_code == 200
    assert len(resposta.json()) == 2


def test_filtro_comodidades(cenario_busca):
    resposta = cenario_busca.get(
        "/republicas",
        params=[
            ("comodidades", "Wi-Fi"),
            ("comodidades", "Lavanderia")
        ]
    )

    assert resposta.status_code == 200
    assert len(resposta.json()) == 1
    assert resposta.json()[0]["titulo"] == "Republica Centro"


def test_filtro_genero(cenario_busca):
    resposta = cenario_busca.get(
        "/republicas",
        params={"genero_republica": "FEMININA"}
    )

    assert resposta.status_code == 200
    assert len(resposta.json()) == 1
    assert resposta.json()[0]["titulo"] == "Republica Teresina"


def test_filtro_moradores(cenario_busca):
    resposta = cenario_busca.get(
        "/republicas",
        params={"max_moradores": 1}
    )

    assert resposta.status_code == 200
    assert len(resposta.json()) == 1
    assert resposta.json()[0]["titulo"] == "Republica Norte"


def test_filtro_vagas(cenario_busca):
    resposta = cenario_busca.get(
        "/republicas",
        params={"vagas_minimas": 3}
    )

    assert resposta.status_code == 200
    assert len(resposta.json()) == 1
    assert resposta.json()[0]["titulo"] == "Republica Norte"


def test_combinacao_de_filtros(cenario_busca):
    resposta = cenario_busca.get(
        "/republicas",
        params=[
            ("preco_maximo", "700.00"),
            ("localizacao", "Picos"),
            ("comodidades", "Wi-Fi"),
            ("comodidades", "Lavanderia"),
            ("genero_republica", "mista"),
            ("max_moradores", "3"),
            ("vagas_minimas", "2")
        ]
    )

    assert resposta.status_code == 200
    assert len(resposta.json()) == 1
    assert resposta.json()[0]["titulo"] == "Republica Centro"


def test_pesquisa_sem_resultados(cenario_busca):
    resposta = cenario_busca.get(
        "/republicas",
        params={"preco_maximo": "100.00"}
    )

    assert resposta.status_code == 200
    assert resposta.json() == []


def test_filtros_invalidos(cenario_busca):
    filtros_invalidos = [
        {"preco_maximo": "-100"},
        {"max_moradores": "-1"},
        {"vagas_minimas": "0"}
    ]

    for filtros in filtros_invalidos:
        resposta = cenario_busca.get(
            "/republicas",
            params=filtros
        )

        assert resposta.status_code == 422
