# LarEstudante

**Plataforma web para busca e gerenciamento de vagas em repúblicas estudantis**
**Disciplina:** Engenharia de Software II — Bacharelado em Sistemas de Informação (UFPI)

## Sobre o projeto

O **LarEstudante** conecta estudantes universitários a oportunidades de moradia compartilhada. Estudantes podem pesquisar anúncios disponíveis e utilizar filtros. Locadores podem cadastrar e gerenciar seus próprios anúncios, mediante autenticação.

A primeira versão é **web**, acessível pelo navegador. O escopo funcional principal compreende **RF01 — Cadastro de usuários**, **RF03 — Gerenciamento de repúblicas**, **RF04 — Pesquisa de repúblicas** e **RF05 — Filtros de pesquisa**, com autenticação como suporte.

## Funcionalidades implementadas

| Funcionalidade | Descrição |
|---|---|
| Cadastro de usuários | Criação de contas de estudante e locador, com validações de dados |
| Login e sessão | Autenticação JWT; identificação de perfil; logout |
| Consulta pública | Pesquisa de repúblicas com vagas disponíveis |
| Filtros | Preço máximo, localização, comodidades, gênero da república, máximo de moradores e vagas mínimas |
| Minhas Repúblicas | Cadastro, listagem, edição, cancelamento de edição e exclusão de anúncios pelo locador |
| Autorização | Proteção de operações administrativas e controle de propriedade dos anúncios |

A interface dispõe de página inicial, cadastro, login, exploração de repúblicas e área de gerenciamento do locador.

> **Fora do escopo desta versão:** chat, avaliações, contratos digitais, pagamentos, tours de imóveis e verificação avançada de usuários. São ideias de evolução futura, não funcionalidades entregues.

## Tecnologias e arquitetura

- **Backend:** Python 3.12, FastAPI, Pydantic, SQLAlchemy e Alembic.
- **Banco de dados:** PostgreSQL 17 (no Docker Compose).
- **Autenticação:** JWT e hash de senha (Argon2 via `pwdlib`).
- **Frontend:** HTML, CSS e JavaScript nativos.
- **Infraestrutura:** Docker e Docker Compose.
- **Testes:** Pytest e FastAPI TestClient.

A solução utiliza **arquitetura cliente-servidor**. O backend é um **monólito modular**, organizado em módulos de usuários, autenticação, repúblicas e busca, com separação entre rotas/API, serviços, repositórios e persistência.

## Requisitos para execução

- Docker Desktop e Docker Compose disponíveis e funcionando.
- Navegador web atualizado.
- Porta TCP **8000** disponível no computador (configuração padrão).

## Como executar (PowerShell / Windows)

Na raiz do projeto, onde estão `compose.yaml`, `Dockerfile` e `requirements.txt`:

1. Crie o arquivo de configuração local a partir do exemplo:

   ```powershell
   Copy-Item .env.example .env
   ```

2. Abra `.env` e substitua os valores de exemplo, especialmente `POSTGRES_PASSWORD` e `JWT_SECRET`, por valores fortes de uso local. **Não publique o `.env`.**

3. Inicie os contêineres:

   ```powershell
   docker compose up -d --build
   ```

4. Execute as migrações do banco, principalmente no primeiro uso:

   ```powershell
   docker compose exec api alembic upgrade head
   ```

5. Acesse a aplicação e a documentação da API:

   - Interface: http://localhost:8000/web/
   - Cadastro: http://localhost:8000/web/cadastro.html
   - Login: http://localhost:8000/web/login.html
   - Explorar repúblicas: http://localhost:8000/web/explorar.html
   - Minhas Repúblicas: http://localhost:8000/web/minhas-republicas.html
   - Swagger UI: http://localhost:8000/docs
   - Saúde da API e conexão com o banco: http://localhost:8000/saude

   A URL raiz `http://localhost:8000/` responde com uma mensagem JSON da API. O site fica em **`/web/`**.

Para encerrar os contêineres sem apagar os dados:

```powershell
docker compose down
```

**Atenção:** `docker compose down -v` remove volumes, incluindo o volume persistente do banco. Não utilize esse comando se quiser preservar os dados cadastrados.

### Conflito na porta 8000

Se outro projeto já estiver utilizando a porta 8000, identifique o contêiner com:

```powershell
docker ps --format "table {{.Names}}\t{{.Ports}}"
```

Pare somente o serviço conflitante, caso seja seguro, ou altere a porta **externa** no `compose.yaml`, por exemplo de `127.0.0.1:8000:8000` para `127.0.0.1:8004:8000`, e acesse o site por `http://localhost:8004/web/`.

## Como usar

**Estudante:** cadastre uma conta com o perfil estudante (ou navegue sem login para a pesquisa pública), abra **Explorar Repúblicas** e combine os filtros conforme suas preferências.

**Locador:** cadastre uma conta com o perfil locador, faça login e acesse **Minhas Repúblicas**. Nessa área, crie, edite ou exclua seus anúncios. O backend verifica se o usuário tem autorização para gerenciar cada anúncio.

Um anúncio armazena título, descrição, preço, localização, gênero da república, número de moradores, vagas disponíveis e comodidades.

## Principais rotas da API

| Método | Rota | Finalidade | Acesso |
|---|---|---|---|
| `GET` | `/` | Informação básica da API | Público |
| `GET` | `/saude` | Saúde da API e banco | Público |
| `POST` | `/usuarios` | Cadastrar usuário | Público |
| `GET` | `/usuarios/me` | Consultar perfil autenticado | Autenticado |
| `POST` | `/login` | Autenticar e obter JWT | Público |
| `GET` | `/republicas` | Pesquisar repúblicas disponíveis e filtrar | Público |
| `GET` | `/republicas/{republica_id}` | Consultar anúncio | Público |
| `GET` | `/republicas/minhas` | Listar anúncios do usuário locador | Autenticado; regra de perfil |
| `POST` | `/republicas` | Cadastrar anúncio | Locador |
| `PATCH` | `/republicas/{republica_id}` | Atualizar anúncio | Locador proprietário |
| `DELETE` | `/republicas/{republica_id}` | Excluir anúncio | Locador proprietário |

Os filtros de `/republicas` são: `preco_maximo`, `localizacao`, `comodidades` (repetível), `genero_republica`, `max_moradores` e `vagas_minimas`. Sem informar `vagas_minimas`, o padrão é **1**.

Para detalhes dos esquemas e dos códigos HTTP, consulte `/docs`.

## Testes e validação

Para executar a suíte automatizada:

```powershell
docker compose exec api python -m pytest -q tests
```

**Resultado comunicado em 21/11/2026:** `30 passed, 1 warning in 3.52s` (0 falhas). Distribuição dos testes: usuários (4), autenticação (6), repúblicas (10), busca e filtros (10).

O aviso exibido foi `StarletteDeprecationWarning`, referente à dependência `httpx` no `TestClient`. Ele não impediu a execução, mas merece atenção em futuras atualizações de dependências.

**Validação manual comunicada em 21/11/2026:** cadastro e login; gerenciamento de repúblicas (criar, listar, editar, cancelar e excluir); persistência após atualizar a página; pesquisa pública; filtros individuais e combinados; navegação entre páginas; bloqueio de acesso não autorizado; rejeição de token ausente/inválido; validação de campos; logout; responsividade em celular e computador.

Os resultados manuais foram informados pelo responsável pelo projeto durante a execução guiada, não por uma suíte automatizada de navegador. Os testes automatizados de backend utilizam uma base de teste independente; a integração PostgreSQL foi verificada separadamente durante a execução da aplicação.

## Estrutura principal

```text
LarEstudante/
├── app/
│   ├── api/                 # Dependências e registro de rotas
│   ├── core/                # Segurança e exceções
│   ├── database/            # Conexão e base do ORM
│   ├── modules/
│   │   ├── usuarios/
│   │   ├── autenticacao/
│   │   ├── republicas/
│   │   └── busca/
│   └── main.py
├── frontend/
│   ├── css/
│   ├── js/
│   └── *.html
├── alembic/                 # Migrações
├── tests/                   # Testes automatizados
├── docs/                    # Documentação complementar (quando incluída)
├── .env.example
├── Dockerfile
├── compose.yaml
├── requirements.txt
└── README.md
```

## Segurança e observações

- As rotas protegidas exigem token JWT; o backend faz a validação das permissões, independentemente da interface.
- As senhas não são armazenadas em texto puro.
- O frontend usa `sessionStorage` para manter o token durante a sessão do navegador.
- Configure credenciais e a chave JWT apropriadas em cada ambiente. Nunca envie `.env` ou outras credenciais ao GitHub.
- Este projeto foi desenvolvido como **versão acadêmica inicial**; não há indicação de preparação completa para operação pública em produção.

## Estado do projeto e próximos passos

**Versão inicial:** funcionalidades principais implementadas, com testes manuais de integração e 30 testes automatizados aprovados conforme relato de 21/11/2026.

**Preparação da entrega:** conferir o README na cópia local, anexar diagramas e documentação quando exigidos, revisar alterações Git, realizar commit/push e preparar uma demonstração dos fluxos de estudante e locador.

**Repositório:** https://github.com/danielsnss/LarEstudante
