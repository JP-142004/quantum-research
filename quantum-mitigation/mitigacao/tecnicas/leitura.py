"""Calibração de leitura. Explicação: fundamentos/tecnicas/leitura.md."""
import numpy as np

from mitigacao.circuitos import nome_item

NOME = 'leitura'
LIMITE_CONDICIONAMENTO = 100


def _item(n, bits, qubits=None, raiz=None):
    return dict(circuito='simples', n=n, variante=bits, base='Z', qubits=qubits, raiz=raiz)


def itens_calibracao(n, qubits=None, raiz=None):
    """Um item por sequência de n bits (2**n itens): prepara essa sequência e mede."""
    return [_item(n, f'{i:0{n}b}', qubits, raiz) for i in range(2 ** n)]


def matriz(contagens, n, qubits=None, modelo='completo'):
    """A[observado, preparado]: cada coluna são as frações registradas para uma preparação.

    contagens: {nome do item: {bits: vezes}}, incluindo os itens de itens_calibracao.
    """
    if modelo != 'completo':
        raise NotImplementedError("Só o modelo 'completo' está implementado; o 'fatorizado' ainda não")
    dim = 2 ** n
    a = np.zeros((dim, dim))
    for j in range(dim):
        c = contagens[nome_item(_item(n, f'{j:0{n}b}', qubits))]
        total = sum(c.values())
        for bits, vezes in c.items():
            a[int(bits, 2), j] = vezes / total
    return a


def _permutacao(mapa_medidas, n):
    """Índice (por qubit físico) -> índice (por bit clássico), para um mapa (qubit, bit)."""
    if len(mapa_medidas) != n or len({q for q, _ in mapa_medidas}) != n or len({c for _, c in mapa_medidas}) != n:
        raise ValueError('Mapa de medidas inválido')
    return np.array([sum(((s >> q) & 1) << c for q, c in mapa_medidas) for s in range(2 ** n)])


def corrigir(a, p, mapa_medidas=None):
    """Resolve A q = p. p: {bits: fração}. mapa_medidas: lista (qubit físico, bit clássico).

    O compilador pode trocar qubits de lugar (SWAP), e a leitura é do qubit físico; o mapa
    de medidas permite reordenar a matriz. Devolve (q: {bits: quasiprobabilidade}, diagnóstico).
    """
    dim = a.shape[0]
    n = dim.bit_length() - 1
    if mapa_medidas is not None:
        inversa = np.argsort(_permutacao(mapa_medidas, n))
        a = a[np.ix_(inversa, inversa)]
    vetor = np.zeros(dim)
    for bits, valor in p.items():
        vetor[int(bits, 2)] += valor
    condicionamento = float(np.linalg.cond(a))
    if not np.isfinite(condicionamento) or condicionamento > LIMITE_CONDICIONAMENTO:
        raise ValueError(f'Calibração instável (condicionamento {condicionamento:.1f})')
    q = np.linalg.solve(a, vetor)
    if not np.allclose(a @ q, vetor) or not np.isclose(q.sum(), vetor.sum()):
        raise ValueError('Falha na inversão')
    diagnostico = dict(condicionamento=condicionamento, menor_quasi=float(q.min()), soma=float(q.sum()))
    return {f'{i:0{n}b}': float(v) for i, v in enumerate(q)}, diagnostico
