
import { buscarRepublicas } from "./api.js";

const formulario = document.getElementById("form-busca");
const lista = document.getElementById("lista-republicas");
const mensagem = document.getElementById("mensagem");

const moeda = new Intl.NumberFormat("pt-BR", {
    style: "currency",
    currency: "BRL"
});


function adicionarTexto(elemento, classe, conteudo) {
    const campo = document.createElement(elemento);
    campo.className = classe;
    campo.textContent = conteudo;
    return campo;
}


function criarCartao(republica) {
    const cartao = document.createElement("article");
    cartao.className = "cartao";

    cartao.appendChild(
        adicionarTexto(
            "span",
            "indicador",
            `${republica.vagas_disponiveis} vaga(s) disponível(is)`
        )
    );

    cartao.appendChild(
        adicionarTexto("h3", "", republica.titulo)
    );

    cartao.appendChild(
        adicionarTexto(
            "p",
            "",
            `Localização: ${republica.localizacao}`
        )
    );

    cartao.appendChild(
        adicionarTexto(
            "p",
            "preco",
            moeda.format(Number(republica.preco))
        )
    );

    cartao.appendChild(
        adicionarTexto(
            "p",
            "",
            `Gênero: ${republica.genero_republica}`
        )
    );

    cartao.appendChild(
        adicionarTexto(
            "p",
            "",
            `Moradores: ${republica.numero_moradores}`
        )
    );

    const nomes = republica.comodidades.map(
        item => item.nome
    );

    cartao.appendChild(
        adicionarTexto(
            "p",
            "comodidades",
            nomes.length
                ? `Comodidades: ${nomes.join(", ")}`
                : "Nenhuma comodidade informada"
        )
    );

    return cartao;
}


async function carregarRepublicas(evento) {
    if (evento) {
        evento.preventDefault();
    }

    const filtros = {
        localizacao: document.getElementById("localizacao").value.trim(),
        preco_maximo: document.getElementById("preco").value
    };

    lista.replaceChildren();
    mensagem.textContent = "Carregando repúblicas...";

    try {
        const republicas = await buscarRepublicas(filtros);

        if (republicas.length === 0) {
            mensagem.textContent =
                "Nenhuma república disponível encontrada.";
            return;
        }

        mensagem.textContent =
            `${republicas.length} república(s) encontrada(s).`;

        for (const republica of republicas) {
            lista.appendChild(criarCartao(republica));
        }

    } catch (erro) {
        console.error(erro);
        mensagem.textContent =
            "Não foi possível carregar os anúncios. Tente novamente.";
    }
}


formulario.addEventListener("submit", carregarRepublicas);

carregarRepublicas();
