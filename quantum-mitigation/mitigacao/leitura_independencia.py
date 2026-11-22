"""Os erros de leitura dos qubits são independentes? Verificação com os circuitos de calibração.

Em um circuito que prepara uma sequência conhecida, o erro de cada qubit em cada medida é 0 ou 1
(lido diferente do preparado). Se os qubits erram sem influência uns nos outros, o número de erros
por medida tem variância igual à soma das variâncias de cada qubit; erros que acontecem juntos
aumentam essa variância. A estatística T é o excesso (variância do número de erros menos a soma
das variâncias por qubit). A referência vem de embaralhar cada qubit separadamente entre as medidas:
isso mantém a taxa de erro de cada qubit e desfaz qualquer ligação entre eles.
Explicação: experimentos/08_leitura_escala/b_ibm/README.md.
"""
import numpy as np


def erros(contagens, preparado):
    """Matriz (medidas x qubits) de 0/1: 1 onde o qubit foi lido diferente do preparado.

    contagens: {bits lidos: vezes}; preparado: sequência de bits, escrita como as contagens.
    """
    n = len(preparado)
    alvo = np.array([int(b) for b in preparado])
    linhas = [np.array([int(b) for b in bits]) ^ alvo for bits, vezes in contagens.items() for _ in range(vezes)]
    return np.array(linhas).reshape(-1, n)


def excesso(e):
    """T: variância do número de erros por medida menos a soma das variâncias de cada qubit."""
    p = e.mean(axis=0)
    return float(e.sum(axis=1).var() - (p * (1 - p)).sum())


def teste(e, rng, permutacoes=1000):
    """T observado, a média e o desvio de T com os qubits embaralhados, e o p-valor (T nulo >= T)."""
    t = excesso(e)
    nulo = np.empty(permutacoes)
    for i in range(permutacoes):
        nulo[i] = excesso(np.column_stack([rng.permutation(e[:, k]) for k in range(e.shape[1])]))
    return dict(T=t, nulo_media=float(nulo.mean()), nulo_dp=float(nulo.std()),
                p_valor=float((1 + (nulo >= t).sum()) / (1 + permutacoes)), taxa_de_erro=float(e.mean()))


def pares_mais_ligados(e, k=3):
    """Os k pares de qubits com mais erros juntos além do esperado por independência: (i, j, observado, esperado)."""
    medidas, p = len(e), e.mean(axis=0)
    juntos = e.T @ e
    pares = [(i, j, int(juntos[i, j]), float(medidas * p[i] * p[j])) for i in range(e.shape[1]) for j in range(i + 1, e.shape[1])]
    return sorted(pares, key=lambda x: x[2] - x[3], reverse=True)[:k]
