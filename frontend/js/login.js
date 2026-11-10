
import {
    autenticarUsuario,
    consultarPerfil,
    guardarToken
} from "./autenticacao.js";

const formulario = document.getElementById("form-login");
const mensagem = document.getElementById("mensagem-login");

const botao = formulario.querySelector('button[type="submit"]');

const linkSucesso =
    document.getElementById("link-sucesso-login");


function mostrarMensagem(texto, tipo) {
    mensagem.textContent = texto;
    mensagem.className = `mensagem-form ${tipo}`;
}


formulario.addEventListener("submit", async evento => {
    evento.preventDefault();

    const email = document.getElementById("email").value.trim();
    const senha = document.getElementById("senha").value;

    botao.disabled = true;
    botao.textContent = "Entrando...";
    mostrarMensagem("", "");

    try {
        const resposta = await autenticarUsuario(email, senha);

        if (!resposta?.access_token) {
            throw new Error(
                "A API não retornou um token de autenticação."
            );
        }

        const perfil = await consultarPerfil(
            resposta.access_token
        );

        guardarToken(resposta.access_token);

        mostrarMensagem(
            `Bem-vindo(a), ${perfil.nome}! Perfil: ${perfil.tipo}.`,
            "sucesso"
        );

        formulario.reset();
        formulario.hidden = true;
        linkSucesso.hidden = false;

        document.dispatchEvent(
            new Event("larestudante:sessao")
        );

    } catch (erro) {
        mostrarMensagem(
            erro.message,
            "erro"
        );

    } finally {
        botao.disabled = false;
        botao.textContent = "Entrar";
    }
});
