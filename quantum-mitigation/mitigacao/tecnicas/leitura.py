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


MODELOS = ('completo', 'fatorizado', 'fatorizado_dois')


def _contagens_do_estado(contagens, n, j, qubits):
    return contagens[nome_item(_item(n, f'{j:0{n}b}', qubits))]


def tabelas_por_qubit(contagens, n, qubits=None, modelo='fatorizado'):
    """Uma tabela 2 x 2 por bit, T[lido, preparado], com T[:, x] somando 1. O índice k é o bit k (o último da sequência é o 0).

    'fatorizado': junta, para cada bit, todos os estados de calibração (as marginais das 2**n).
    'fatorizado_dois': usa só a sequência de zeros e a de uns.
    """
    if modelo == 'fatorizado':
        estados = range(2 ** n)
    elif modelo == 'fatorizado_dois':
        estados = (0, 2 ** n - 1)
    else:
        raise ValueError(f'Modelo fatorizado desconhecido: {modelo!r}')
    tabelas = []
    for k in range(n):
        conta = np.zeros((2, 2))
        for j in estados:
            preparado = (j >> k) & 1
            for bits, vezes in _contagens_do_estado(contagens, n, j, qubits).items():
                conta[(int(bits, 2) >> k) & 1, preparado] += vezes
        totais = conta.sum(axis=0)
        if np.any(totais == 0):
            raise ValueError(f'Sem medidas para uma condição do bit {k}')
        tabelas.append(conta / totais)
    return tabelas


def matriz(contagens, n, qubits=None, modelo='completo'):
    """A[observado, preparado]: cada coluna são as frações registradas para uma preparação.

    contagens: {nome do item: {bits: vezes}}, incluindo os itens de itens_calibracao.
    modelo: 'completo' (matriz medida), 'fatorizado' ou 'fatorizado_dois' (ver `tabelas_por_qubit`).
    Os modelos fatorizados devolvem o produto de Kronecker das tabelas, na mesma ordem de índices da completa.
    """
    if modelo in ('fatorizado', 'fatorizado_dois'):
        a = np.ones((1, 1))
        for tabela in reversed(tabelas_por_qubit(contagens, n, qubits, modelo)):
            a = np.kron(a, tabela)
        return a
    if modelo != 'completo':
        raise ValueError(f'Modelo desconhecido: {modelo!r}; use um de {MODELOS}')
    dim = 2 ** n
    a = np.zeros((dim, dim))
    for j in range(dim):
        c = _contagens_do_estado(contagens, n, j, qubits)
        total = sum(c.values())
        for bits, vezes in c.items():
            a[int(bits, 2), j] = vezes / total
    return a


def permutacao(mapa_medidas, n):
    """Índice (por qubit físico) -> índice (por bit clássico), para um mapa (qubit, bit)."""
    if len(mapa_medidas) != n or len({q for q, _ in mapa_medidas}) != n or len({c for _, c in mapa_medidas}) != n:
        raise ValueError('Mapa de medidas inválido')
    return np.array([sum(((s >> q) & 1) << c for q, c in mapa_medidas) for s in range(2 ** n)])


def _conferir(a):
    condicionamento = float(np.linalg.cond(a))
    if not np.isfinite(condicionamento) or condicionamento > LIMITE_CONDICIONAMENTO:
        raise ValueError(f'Calibração instável (condicionamento {condicionamento:.1f})')
    return condicionamento


def corrigir_varios(a, p, perms):
    """Corrige várias distribuições de uma vez, com a mesma matriz A.

    p: array (k, 2**n), uma distribuição por linha, na ordem dos bits clássicos.
    perms: k permutações (ver `permutacao`), uma por distribuição.
    Devolve Q com a mesma forma e a mesma ordem. Equivale a `corrigir` com o mapa de medidas.
    """
    _conferir(a)
    fisicas = np.stack([p[j][perms[j]] for j in range(len(p))], axis=1)  # ordem dos qubits físicos
    q_fisico = np.linalg.solve(a, fisicas)
    q = np.empty_like(p)
    for j in range(len(p)):
        q[j][perms[j]] = q_fisico[:, j]
    return q


def corrigir(a, p, mapa_medidas=None):
    """Resolve A q = p. p: {bits: fração}. mapa_medidas: lista (qubit físico, bit clássico).

    O compilador pode trocar qubits de lugar (SWAP), e a leitura é do qubit físico; o mapa
    de medidas permite reordenar a matriz. Devolve (q: {bits: quasiprobabilidade}, diagnóstico).
    """
    dim = a.shape[0]
    n = dim.bit_length() - 1
    if mapa_medidas is not None:
        inversa = np.argsort(permutacao(mapa_medidas, n))
        a = a[np.ix_(inversa, inversa)]
    vetor = np.zeros(dim)
    for bits, valor in p.items():
        vetor[int(bits, 2)] += valor
    condicionamento = _conferir(a)
    q = np.linalg.solve(a, vetor)
    if not np.allclose(a @ q, vetor) or not np.isclose(q.sum(), vetor.sum()):
        raise ValueError('Falha na inversão')
    diagnostico = dict(condicionamento=condicionamento, menor_quasi=float(q.min()), soma=float(q.sum()))
    return {f'{i:0{n}b}': float(v) for i, v in enumerate(q)}, diagnostico
