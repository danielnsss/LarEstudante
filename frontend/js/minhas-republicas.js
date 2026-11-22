
const CHAVE_TOKEN = "larestudante_token";

const avisoAcesso = document.getElementById("aviso-acesso");
const textoAcesso = document.getElementById("texto-acesso");
const conteudoGestao = document.getElementById("conteudo-gestao");

const formulario = document.getElementById("form-republica");
const tituloFormulario = document.getElementById("titulo-formulario");
const mensagemFormulario = document.getElementById("mensagem-formulario");

const botaoSalvar = document.getElementById("botao-salvar");
const botaoCancelar = document.getElementById("botao-cancelar");
const botaoAtualizar = document.getElementById("botao-atualizar");

const lista = document.getElementById("lista-minhas-republicas");
const estadoLista = document.getElementById("estado-lista");

const formatadorPreco = new Intl.NumberFormat("pt-BR", {
    style: "currency",
    currency: "BRL"
});

const camposFormulario = [
    "titulo",
    "descricao",
    "preco",
    "localizacao",
    "genero_republica",
    "numero_moradores",
    "vagas_disponiveis",
    "comodidades"
];

let idEmEdicao = null;
let anuncioOriginal = null;


function obterToken() {
    return sessionStorage.getItem(CHAVE_TOKEN);
}


async function solicitarAPI(caminho, metodo = "GET", dados = null) {
    const token = obterToken();

    if (!token) {
        throw new Error("Sua sessão não está ativa. Faça login.");
    }

    const cabecalhos = {
        Accept: "application/json",
        Authorization: `Bearer ${token}`
    };

    if (dados !== null) {
        cabecalhos["Content-Type"] = "application/json";
    }

    const opcoes = {
        method: metodo,
        headers: cabecalhos
    };

    if (dados !== null) {
        opcoes.body = JSON.stringify(dados);
    }

    const resposta = await fetch(caminho, opcoes);

    if (resposta.status === 204) {
        return null;
    }

    const resultado = await resposta.json().catch(() => null);

    if (!resposta.ok) {
        let mensagem = `Erro HTTP ${resposta.status}.`;

        if (resposta.status === 401) {
            mensagem = "Sessão inválida ou expirada. Entre novamente.";
        } else if (resposta.status === 403) {
            mensagem = "Você não possui permissão para esta operação.";
        } else if (resposta.status === 404) {
            mensagem = "República não encontrada.";
        } else if (resultado?.detail) {
            if (typeof resultado.detail === "string") {
                mensagem = resultado.detail;
            } else if (Array.isArray(resultado.detail)) {
                mensagem = resultado.detail
                    .map(item => item.msg ?? "Campo inválido")
                    .join("; ");
            }
        }

        const erro = new Error(mensagem);
        erro.status = resposta.status;
        throw erro;
    }

    return resultado;
}


function mostrarAcessoNegado(mensagem) {
    conteudoGestao.hidden = true;
    avisoAcesso.hidden = false;
    textoAcesso.textContent = mensagem;
}


function obterId(republica) {
    return republica.id ?? republica.republica_id ?? null;
}


function normalizarComodidades(valor) {
    if (!Array.isArray(valor)) {
        return [];
    }

    return valor
        .map(item => {
            if (typeof item === "string") {
                return item;
            }

            return item?.nome ?? "";
        })
        .filter(Boolean);
}


function lerComodidades() {
    const texto = document.getElementById("comodidades").value;

    const itens = texto
        .split(",")
        .map(item => item.trim())
        .filter(Boolean);

    return [...new Set(itens)];
}


function montarDados() {
    return {
        titulo: document.getElementById("titulo").value.trim(),
        descricao: document.getElementById("descricao").value.trim(),
        preco: Number(
            document.getElementById("preco").value
        ).toFixed(2),
        localizacao: document
            .getElementById("localizacao")
            .value.trim(),
        genero_republica: document
            .getElementById("genero_republica")
            .value.trim(),
        numero_moradores: Number(
            document.getElementById("numero_moradores").value
        ),
        vagas_disponiveis: Number(
            document.getElementById("vagas_disponiveis").value
        ),
        comodidades: lerComodidades()
    };
}


function montarAtualizacao(dados) {
    const alteracoes = {};

    for (const campo of camposFormulario) {
        let valorAnterior = anuncioOriginal[campo];
        let valorNovo = dados[campo];

        if (campo === "preco") {
            valorAnterior = Number(valorAnterior).toFixed(2);
        }

        if (campo === "comodidades") {
            valorAnterior = normalizarComodidades(valorAnterior)
                .map(item => item.toLowerCase());

            valorNovo = valorNovo
                .map(item => item.toLowerCase());
        }

        if (JSON.stringify(valorAnterior) !== JSON.stringify(valorNovo)) {
            alteracoes[campo] = dados[campo];
        }
    }

    return alteracoes;
}


function limparFormulario(mensagem = "") {
    formulario.reset();

    idEmEdicao = null;
    anuncioOriginal = null;

    tituloFormulario.textContent = "Cadastrar república";
    botaoSalvar.textContent = "Cadastrar república";
    botaoCancelar.hidden = true;

    mensagemFormulario.textContent = mensagem;
}


function preencherFormulario(republica) {
    for (const campo of camposFormulario) {
        if (campo === "comodidades") {
            document.getElementById(campo).value =
                normalizarComodidades(republica[campo]).join(", ");

        } else if (campo === "preco") {
            document.getElementById(campo).value =
                String(Number(republica[campo]));

        } else {
            document.getElementById(campo).value =
                republica[campo] ?? "";
        }
    }
}


function criarParagrafo(elemento, classe, texto) {
    const paragrafo = document.createElement("p");

    if (classe) {
        paragrafo.className = classe;
    }

    paragrafo.textContent = texto;
    elemento.appendChild(paragrafo);

    return paragrafo;
}


function criarCartao(republica) {
    const cartao = document.createElement("article");
    cartao.className = "gestao-cartao";

    const id = obterId(republica);

    criarParagrafo(
        cartao,
        "gestao-indicador",
        `${republica.vagas_disponiveis} vaga(s) disponível(is)`
    );

    const titulo = document.createElement("h3");
    titulo.textContent = republica.titulo ?? "República sem título";
    cartao.appendChild(titulo);

    criarParagrafo(
        cartao,
        "gestao-detalhe",
        `Localização: ${republica.localizacao ?? "Não informada"}`
    );

    criarParagrafo(
        cartao,
        "gestao-preco",
        formatadorPreco.format(Number(republica.preco))
    );

    criarParagrafo(
        cartao,
        "gestao-detalhe",
        `Gênero: ${republica.genero_republica ?? "Não informado"}`
    );

    criarParagrafo(
        cartao,
        "gestao-detalhe",
        `Moradores: ${republica.numero_moradores ?? "Não informado"}`
    );

    const comodidades = normalizarComodidades(republica.comodidades);

    criarParagrafo(
        cartao,
        "gestao-detalhe",
        comodidades.length
            ? `Comodidades: ${comodidades.join(", ")}`
            : "Comodidades: nenhuma informada"
    );

    const acoes = document.createElement("div");
    acoes.className = "gestao-acoes";

    const botaoEditar = document.createElement("button");
    botaoEditar.type = "button";
    botaoEditar.className = "gestao-botao-editar";
    botaoEditar.textContent = "Editar";

    const botaoExcluir = document.createElement("button");
    botaoExcluir.type = "button";
    botaoExcluir.className = "gestao-botao-excluir";
    botaoExcluir.textContent = "Excluir";

    if (id == null) {
        botaoEditar.disabled = true;
        botaoExcluir.disabled = true;
    } else {
        botaoEditar.addEventListener("click", () => {
            iniciarEdicao(id);
        });

        botaoExcluir.addEventListener("click", () => {
            excluirRepublica(id, republica.titulo);
        });
    }

    acoes.append(botaoEditar, botaoExcluir);
    cartao.appendChild(acoes);

    return cartao;
}


function apresentarRepublicas(republicas) {
    lista.replaceChildren();

    if (republicas.length === 0) {
        estadoLista.textContent =
            "Você ainda não cadastrou nenhuma república.";
        return;
    }

    estadoLista.textContent =
        `${republicas.length} anúncio(s) cadastrado(s).`;

    const fragmento = document.createDocumentFragment();

    for (const republica of republicas) {
        fragmento.appendChild(criarCartao(republica));
    }

    lista.appendChild(fragmento);
}


async function carregarRepublicas() {
    estadoLista.textContent = "Carregando seus anúncios...";
    botaoAtualizar.disabled = true;

    try {
        const republicas = await solicitarAPI("/republicas/minhas");

        if (!Array.isArray(republicas)) {
            throw new Error("A API retornou uma lista inesperada.");
        }

        apresentarRepublicas(republicas);

    } catch (erro) {
        lista.replaceChildren();
        estadoLista.textContent = erro.message;

        if (erro.status === 401 || erro.status === 403) {
            mostrarAcessoNegado(erro.message);
        }

    } finally {
        botaoAtualizar.disabled = false;
    }
}


async function iniciarEdicao(id) {
    mensagemFormulario.textContent = "Carregando anúncio...";

    try {
        const republica = await solicitarAPI(`/republicas/${id}`);

        preencherFormulario(republica);

        anuncioOriginal = republica;
        idEmEdicao = id;

        tituloFormulario.textContent = "Editar república";
        botaoSalvar.textContent = "Salvar alterações";
        botaoCancelar.hidden = false;

        mensagemFormulario.textContent =
            "Altere os dados desejados e clique em Salvar alterações.";

        tituloFormulario.scrollIntoView({
            behavior: "smooth",
            block: "start"
        });

    } catch (erro) {
        mensagemFormulario.textContent = erro.message;
    }
}


async function excluirRepublica(id, titulo) {
    const confirmado = window.confirm(
        `Deseja realmente excluir "${titulo}"?\n\n` +
        "Essa operação não poderá ser desfeita."
    );

    if (!confirmado) {
        return;
    }

    try {
        await solicitarAPI(`/republicas/${id}`, "DELETE");

        if (idEmEdicao === id) {
            limparFormulario();
        }

        mensagemFormulario.textContent =
            "República excluída com sucesso.";

        await carregarRepublicas();

    } catch (erro) {
        mensagemFormulario.textContent = erro.message;
    }
}


async function salvarRepublica(evento) {
    evento.preventDefault();

    if (!formulario.reportValidity()) {
        return;
    }

    const dados = montarDados();

    botaoSalvar.disabled = true;
    mensagemFormulario.textContent = "Salvando anúncio...";

    try {
        if (idEmEdicao === null) {
            await solicitarAPI("/republicas", "POST", dados);

            limparFormulario(
                "República cadastrada com sucesso."
            );

        } else {
            const alteracoes = montarAtualizacao(dados);

            if (Object.keys(alteracoes).length === 0) {
                mensagemFormulario.textContent =
                    "Nenhuma alteração foi realizada.";
                return;
            }

            await solicitarAPI(
                `/republicas/${idEmEdicao}`,
                "PATCH",
                alteracoes
            );

            limparFormulario(
                "República atualizada com sucesso."
            );
        }

        await carregarRepublicas();

    } catch (erro) {
        mensagemFormulario.textContent = erro.message;

    } finally {
        botaoSalvar.disabled = false;
    }
}


async function inicializar() {
    if (!obterToken()) {
        mostrarAcessoNegado(
            "Faça login com uma conta de locador para gerenciar anúncios."
        );
        return;
    }

    try {
        const usuario = await solicitarAPI("/usuarios/me");

        if (usuario.tipo !== "locador") {
            mostrarAcessoNegado(
                "Esta área é exclusiva para locadores. " +
                "Entre com uma conta de locador para continuar."
            );
            return;
        }

        avisoAcesso.hidden = true;
        conteudoGestao.hidden = false;

        await carregarRepublicas();

    } catch (erro) {
        mostrarAcessoNegado(erro.message);
    }
}


formulario.addEventListener("submit", salvarRepublica);

botaoCancelar.addEventListener("click", () => {
    limparFormulario("Edição cancelada.");
});

botaoAtualizar.addEventListener("click", carregarRepublicas);

inicializar();
