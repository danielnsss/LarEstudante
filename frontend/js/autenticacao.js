
const CHAVE_TOKEN = "larestudante_token";


async function requisitarJson(caminho, opcoes = {}) {
    const headers = {
        Accept: "application/json"
    };

    if (opcoes.body !== undefined) {
        headers["Content-Type"] = "application/json";
    }

    if (opcoes.token) {
        headers.Authorization = `Bearer ${opcoes.token}`;
    }

    let resposta;

    try {
        resposta = await fetch(caminho, {
            method: opcoes.method ?? "GET",
            headers,
            body: opcoes.body === undefined
                ? undefined
                : JSON.stringify(opcoes.body)
        });
    } catch {
        throw new Error(
            "Não foi possível conectar à API do LarEstudante."
        );
    }

    const dados = await resposta.json().catch(() => null);

    if (!resposta.ok) {
        const detalhe = dados?.detail;

        let mensagem = "Não foi possível concluir a operação.";

        if (typeof detalhe === "string") {
            mensagem = detalhe;
        } else if (Array.isArray(detalhe)) {
            mensagem = detalhe
                .map(item => item.msg)
                .filter(Boolean)
                .join("; ") || mensagem;
        }

        throw new Error(mensagem);
    }

    return dados;
}


export function cadastrarUsuario(dados) {
    return requisitarJson("/usuarios", {
        method: "POST",
        body: dados
    });
}


export function autenticarUsuario(email, senha) {
    return requisitarJson("/login", {
        method: "POST",
        body: { email, senha }
    });
}


export function consultarPerfil(token) {
    return requisitarJson("/usuarios/me", {
        token
    });
}


export function guardarToken(token) {
    sessionStorage.setItem(CHAVE_TOKEN, token);
}


export function obterToken() {
    return sessionStorage.getItem(CHAVE_TOKEN);
}


export function encerrarSessao() {
    sessionStorage.removeItem(CHAVE_TOKEN);
}
