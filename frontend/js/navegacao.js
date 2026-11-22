
import {
    obterToken,
    encerrarSessao
} from "./autenticacao.js";

const menu = document.getElementById("menu-usuario");

let versaoNavegacao = 0;


function criarLink(texto, destino) {
    const link = document.createElement("a");

    link.textContent = texto;
    link.href = destino;

    return link;
}


function criarBotaoSair() {
    const sair = document.createElement("button");

    sair.type = "button";
    sair.textContent = "Sair";

    sair.addEventListener("click", () => {
        encerrarSessao();
        window.location.assign("./");
    });

    return sair;
}


async function renderizarNavegacao() {
    if (!menu) {
        return;
    }

    const versaoAtual = ++versaoNavegacao;

    menu.replaceChildren();

    const token = obterToken();

    if (!token) {
        menu.append(
            criarLink("Entrar", "./login.html"),
            criarLink("Criar conta", "./cadastro.html")
        );

        return;
    }

    const indicador = document.createElement("span");

    indicador.className = "estado-sessao";
    indicador.textContent = "Sessão iniciada";

    menu.append(
        indicador,
        criarBotaoSair()
    );

    try {
        const resposta = await fetch("/usuarios/me", {
            method: "GET",
            headers: {
                Accept: "application/json",
                Authorization: `Bearer ${token}`
            }
        });

        if (!resposta.ok) {
            return;
        }

        const usuario = await resposta.json();

        if (
            versaoAtual !== versaoNavegacao ||
            token !== obterToken()
        ) {
            return;
        }

        if (usuario.tipo === "locador") {
            const link = criarLink(
                "Minhas repúblicas",
                "./minhas-republicas.html"
            );

            menu.prepend(link);
        }

    } catch (erro) {
        console.error(
            "Não foi possível consultar o perfil:",
            erro
        );
    }
}


document.addEventListener(
    "larestudante:sessao",
    renderizarNavegacao
);

renderizarNavegacao();
