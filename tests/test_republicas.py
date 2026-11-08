
def criar_conta_e_token(cliente, email, tipo):
    cadastro = cliente.post(
        "/usuarios",
        json={
            "nome": "Usuario de Teste",
            "email": email,
            "senha": "Teste1234!",
            "tipo": tipo
        }
    )

    assert cadastro.status_code == 201

    login = cliente.post(
        "/login",
        json={
            "email": email,
            "senha": "Teste1234!"
        }
    )

    assert login.status_code == 200

    token = login.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }


def dados_republica():
    return {
        "titulo": "República Universitária Centro",
        "descricao": "Moradia estudantil em Picos.",
        "preco": "650.00",
        "localizacao": "Picos - PI",
        "genero_republica": "mista",
        "numero_moradores": 3,
        "vagas_disponiveis": 2,
        "comodidades": ["Wi-Fi", "Lavanderia"]
    }


def test_locador_cadastra_republica(cliente_api):
    cliente, _ = cliente_api

    headers = criar_conta_e_token(
        cliente, "locador1@example.com", "locador"
    )

    resposta = cliente.post(
        "/republicas",
        json=dados_republica(),
        headers=headers
    )

    assert resposta.status_code == 201

    dados = resposta.json()

    assert dados["titulo"] == "República Universitária Centro"
    assert dados["preco"] == "650.00"
    assert dados["vagas_disponiveis"] == 2
    assert len(dados["comodidades"]) == 2


def test_estudante_nao_cadastra_republica(cliente_api):
    cliente, _ = cliente_api

    headers = criar_conta_e_token(
        cliente, "estudante2@example.com", "estudante"
    )

    resposta = cliente.post(
        "/republicas",
        json=dados_republica(),
        headers=headers
    )

    assert resposta.status_code == 403


def test_cadastro_sem_autenticacao(cliente_api):
    cliente, _ = cliente_api

    resposta = cliente.post(
        "/republicas",
        json=dados_republica()
    )

    assert resposta.status_code == 401


def test_locador_lista_apenas_suas_republicas(cliente_api):
    cliente, _ = cliente_api

    headers1 = criar_conta_e_token(
        cliente, "locador1@example.com", "locador"
    )

    headers2 = criar_conta_e_token(
        cliente, "locador2@example.com", "locador"
    )

    primeira = cliente.post(
        "/republicas",
        json=dados_republica(),
        headers=headers1
    )

    segunda = cliente.post(
        "/republicas",
        json=dados_republica(),
        headers=headers2
    )

    assert primeira.status_code == 201
    assert segunda.status_code == 201

    resposta = cliente.get(
        "/republicas/minhas",
        headers=headers1
    )

    assert resposta.status_code == 200
    assert len(resposta.json()) == 1
    assert resposta.json()[0]["id"] == primeira.json()["id"]


def test_locador_atualiza_sua_republica(cliente_api):
    cliente, _ = cliente_api

    headers = criar_conta_e_token(
        cliente, "locador1@example.com", "locador"
    )

    cadastro = cliente.post(
        "/republicas",
        json=dados_republica(),
        headers=headers
    )

    assert cadastro.status_code == 201

    republica_id = cadastro.json()["id"]

    resposta = cliente.patch(
        f"/republicas/{republica_id}",
        json={
            "preco": "700.00",
            "vagas_disponiveis": 1
        },
        headers=headers
    )

    assert resposta.status_code == 200
    assert resposta.json()["preco"] == "700.00"
    assert resposta.json()["vagas_disponiveis"] == 1
    assert resposta.json()["numero_moradores"] == 3


def test_locador_nao_atualiza_republica_de_outro(cliente_api):
    cliente, _ = cliente_api

    dono = criar_conta_e_token(
        cliente, "dono@example.com", "locador"
    )

    outro = criar_conta_e_token(
        cliente, "outro@example.com", "locador"
    )

    cadastro = cliente.post(
        "/republicas",
        json=dados_republica(),
        headers=dono
    )

    assert cadastro.status_code == 201

    republica_id = cadastro.json()["id"]

    resposta = cliente.patch(
        f"/republicas/{republica_id}",
        json={"preco": "900.00"},
        headers=outro
    )

    assert resposta.status_code == 403


def test_locador_nao_exclui_republica_de_outro(cliente_api):
    cliente, _ = cliente_api

    dono = criar_conta_e_token(
        cliente, "dono@example.com", "locador"
    )

    outro = criar_conta_e_token(
        cliente, "outro@example.com", "locador"
    )

    cadastro = cliente.post(
        "/republicas",
        json=dados_republica(),
        headers=dono
    )

    assert cadastro.status_code == 201

    republica_id = cadastro.json()["id"]

    resposta = cliente.delete(
        f"/republicas/{republica_id}",
        headers=outro
    )

    assert resposta.status_code == 403


def test_locador_exclui_sua_republica(cliente_api):
    cliente, _ = cliente_api

    headers = criar_conta_e_token(
        cliente, "locador1@example.com", "locador"
    )

    cadastro = cliente.post(
        "/republicas",
        json=dados_republica(),
        headers=headers
    )

    assert cadastro.status_code == 201

    republica_id = cadastro.json()["id"]

    exclusao = cliente.delete(
        f"/republicas/{republica_id}",
        headers=headers
    )

    assert exclusao.status_code == 204

    consulta = cliente.get(
        f"/republicas/{republica_id}"
    )

    assert consulta.status_code == 404


def test_preco_invalido(cliente_api):
    cliente, _ = cliente_api

    headers = criar_conta_e_token(
        cliente, "locador1@example.com", "locador"
    )

    dados = dados_republica()
    dados["preco"] = "-100.00"

    resposta = cliente.post(
        "/republicas",
        json=dados,
        headers=headers
    )

    assert resposta.status_code == 422


def test_consulta_republica_inexistente(cliente_api):
    cliente, _ = cliente_api

    resposta = cliente.get("/republicas/999999")

    assert resposta.status_code == 404
