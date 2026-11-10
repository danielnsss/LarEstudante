
const formulario = document.getElementById("form-filtros");
const grade = document.getElementById("grade-resultados");
const estado = document.getElementById("estado-resultados");

const botaoPesquisar = document.getElementById("botao-pesquisar");
const botaoLimpar = document.getElementById("botao-limpar");

const formatadorPreco = new Intl.NumberFormat("pt-BR", {
    style: "currency",
    currency: "BRL"
});

let controladorAtual = null;


function montarParametros() {
    const parametros = new URLSearchParams();

    const campos = [
        "localizacao",
        "preco_maximo",
        "genero_republica",
        "max_moradores",
        "vagas_minimas"
    ];

    for (const campo of campos) {
        const valor = document.getElementById(campo).value.trim();

        if (valor !== "") {
            parametros.append(campo, valor);
        }
    }

    const comodidades = document
        .getElementById("comodidades")
        .value
        .split(",")
        .map(valor => valor.trim().toLowerCase())
        .filter(Boolean);

    for (const comodidade of new Set(comodidades)) {
        parametros.append("comodidades", comodidade);
    }

    return parametros;
}


function adicionarTexto(elemento, classe, texto) {
    const paragrafo = document.createElement("p");

    if (classe) {
        paragrafo.className = classe;
    }

    paragrafo.textContent = texto;
    elemento.appendChild(paragrafo);
}


function formatarPreco(valor) {
    const numero = Number(valor);

    if (valor == null || !Number.isFinite(numero)) {
        return "Preço não informado";
    }

    return formatadorPreco.format(numero);
}


function obterComodidades(republica) {
    if (!Array.isArray(republica.comodidades)) {
        return [];
    }

    return republica.comodidades
        .map(item => {
            if (typeof item === "string") {
                return item;
            }

            return item?.nome ?? "";
        })
        .filter(Boolean);
}


function criarCartao(republica) {
    const cartao = document.createElement("article");
    cartao.className = "cartao";

    adicionarTexto(
        cartao,
        "indicador",
        `${republica.vagas_disponiveis} vaga(s) disponível(is)`
    );

    const titulo = document.createElement("h3");
    titulo.textContent = republica.titulo ?? "República sem título";
    cartao.appendChild(titulo);

    adicionarTexto(
        cartao,
        "",
        `Localização: ${republica.localizacao ?? "Não informada"}`
    );

    adicionarTexto(
        cartao,
        "preco",
        formatarPreco(republica.preco)
    );

    adicionarTexto(
        cartao,
        "",
        `Gênero: ${republica.genero_republica ?? "Não informado"}`
    );

    adicionarTexto(
        cartao,
        "",
        `Moradores: ${republica.numero_moradores ?? "Não informado"}`
    );

    const comodidades = obterComodidades(republica);

    adicionarTexto(
        cartao,
        "comodidades",
        comodidades.length
            ? `Comodidades: ${comodidades.join(", ")}`
            : "Comodidades: não informadas"
    );

    return cartao;
}


function apresentarResultados(republicas) {
    grade.replaceChildren();

    if (republicas.length === 0) {
        estado.textContent = "Nenhuma república disponível encontrada.";
        return;
    }

    estado.textContent =
        `${republicas.length} república(s) encontrada(s).`;

    const fragmento = document.createDocumentFragment();

    for (const republica of republicas) {
        fragmento.appendChild(criarCartao(republica));
    }

    grade.appendChild(fragmento);
}


async function buscarRepublicas() {
    if (controladorAtual) {
        controladorAtual.abort();
    }

    controladorAtual = new AbortController();
    const sinal = controladorAtual.signal;

    const parametros = montarParametros();
    const consulta = parametros.toString();

    const endereco = consulta
        ? `/republicas?${consulta}`
        : "/republicas";

    grade.replaceChildren();
    estado.textContent = "Buscando repúblicas...";
    botaoPesquisar.disabled = true;

    try {
        const resposta = await fetch(endereco, {
            method: "GET",
            headers: {
                Accept: "application/json"
            },
            signal: sinal
        });

        if (!resposta.ok) {
            throw new Error(
                `Não foi possível realizar a pesquisa (HTTP ${resposta.status}).`
            );
        }

        const dados = await resposta.json();

        if (!Array.isArray(dados)) {
            throw new Error("Resposta inesperada da API.");
        }

        apresentarResultados(dados);

    } catch (erro) {
        if (erro.name === "AbortError") {
            return;
        }

        grade.replaceChildren();
        estado.textContent = erro.message;

    } finally {
        if (!sinal.aborted) {
            botaoPesquisar.disabled = false;
            controladorAtual = null;
        }
    }
}


formulario.addEventListener("submit", evento => {
    evento.preventDefault();

    if (formulario.reportValidity()) {
        buscarRepublicas();
    }
});


botaoLimpar.addEventListener("click", () => {
    formulario.reset();
    buscarRepublicas();
});


buscarRepublicas();
