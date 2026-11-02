"""Bootstrap. Explicação: fundamentos/indicadores.md."""
import numpy as np


def reamostrar(contagens, rng):
    """Novo sorteio multinomial com as mesmas frequências e o mesmo total de shots."""
    chaves = list(contagens)
    total = sum(contagens.values())
    novos = rng.multinomial(total, [contagens[c] / total for c in chaves])
    return {c: int(v) for c, v in zip(chaves, novos) if v}


def bootstrap(calcular, contagens, repeticoes=5000, semente=0):
    """Refaz a conta inteira em cada réplica.

    contagens: {nome: {bits: vezes}}. Em cada réplica, todos os circuitos são reamostrados
    ao mesmo tempo (por exemplo calibração e circuito de interesse) e `calcular` recebe o
    dict reamostrado e devolve um número ou um vetor. Devolve um array (repeticoes, ...).
    """
    rng = np.random.default_rng(semente)
    replicas = [np.asarray(calcular({nome: reamostrar(c, rng) for nome, c in contagens.items()}), float)
                for _ in range(repeticoes)]
    return np.array(replicas)


def resumo(replicas):
    """Erro padrão e intervalo de 95% (percentis 2,5 e 97,5) de cada coluna."""
    replicas = np.asarray(replicas, float)
    return dict(erro_padrao=np.std(replicas, axis=0, ddof=1),
                ic95=np.quantile(replicas, [0.025, 0.975], axis=0))
