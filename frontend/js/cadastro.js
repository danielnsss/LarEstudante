
import { cadastrarUsuario } from "./autenticacao.js";

const formulario = document.getElementById("form-cadastro");
const mensagem = document.getElementById("mensagem-cadastro");
const botao = formulario.querySelector('button[type="submit"]');


function mostrarMensagem(texto, tipo) {
    mensagem.textContent = texto;
    mensagem.className = `mensagem-form ${tipo}`;
}


formulario.addEventListener("submit", async evento => {
    evento.preventDefault();

    const nome = document.getElementById("nome").value.trim();
    const email = document.getElementById("email").value.trim();
    const tipo = document.getElementById("tipo").value;
    const senha = document.getElementById("senha").value;

    const confirmarSenha =
        document.getElementById("confirmar-senha").value;

    if (senha !== confirmarSenha) {
        mostrarMensagem(
            "As senhas informadas não coincidem.",
            "erro"
        );
        return;
    }

    botao.disabled = true;
    botao.textContent = "Cadastrando...";
    mostrarMensagem("", "");

    try {
        await cadastrarUsuario({
            nome,
            email,
            senha,
            tipo
        });

        mostrarMensagem(
            "Conta criada com sucesso! Agora você pode entrar.",
            "sucesso"
        );

        formulario.reset();

    } catch (erro) {
        mostrarMensagem(
            erro.message,
            "erro"
        );

    } finally {
        botao.disabled = false;
        botao.textContent = "Criar conta";
    }
});
