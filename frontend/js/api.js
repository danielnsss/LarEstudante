
export async function buscarRepublicas(filtros = {}) {
    const parametros = new URLSearchParams();

    for (const [chave, valor] of Object.entries(filtros)) {
        if (valor !== "" && valor !== null && valor !== undefined) {
            parametros.append(chave, valor);
        }
    }

    const consulta = parametros.toString();

    const url = consulta
        ? `/republicas?${consulta}`
        : "/republicas";

    const resposta = await fetch(url);

    if (!resposta.ok) {
        throw new Error(
            `Erro ao consultar repúblicas: HTTP ${resposta.status}`
        );
    }

    return await resposta.json();
}
