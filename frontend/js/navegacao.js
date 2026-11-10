
import {
    obterToken,
    encerrarSessao
} from "./autenticacao.js";

const menu = document.getElementById("menu-usuario");


function criarLink(texto, destino) {
    const link = document.createElement("a");

    link.textContent = texto;
    link.href = destino;

    return link;
}


function renderizarNavegacao() {
    if (!menu) {
        return;
    }

    menu.replaceChildren();

    if (obterToken()) {
        const indicador = document.createElement("span");

        indicador.className = "estado-sessao";
        indicador.textContent = "Sessão iniciada";

        const sair = document.createElement("button");

        sair.type = "button";
        sair.textContent = "Sair";

        sair.addEventListener("click", () => {
            encerrarSessao();
            window.location.assign("./");
        });

        menu.append(indicador, sair);

    } else {
        menu.append(
            criarLink("Entrar", "./login.html"),
            criarLink("Criar conta", "./cadastro.html")
        );
    }
}


document.addEventListener(
    "larestudante:sessao",
    renderizarNavegacao
);

renderizarNavegacao();
