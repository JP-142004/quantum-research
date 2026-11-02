"""Estado GHZ: (|0...0> + |1...1>) / raiz de 2. Explicação: fundamentos/circuitos/ghz.md."""
from qiskit import QuantumCircuit

NOME = 'ghz'
VARIANTES = "'original' (o qubit 0 liga a todos) e 'conectado' (árvore que segue as ligações do computador)"
EXEMPLOS = [(3, 'original'), (5, 'original'), (5, 'conectado'), (8, 'conectado')]  # (n, variante), usados nos testes


def preparacao(n, variante='original', arestas=None):
    """arestas: lista (origem, destino) em índices lógicos; a origem da primeira é a raiz."""
    qc = QuantumCircuit(n)
    if variante == 'original':
        qc.h(0)
        for alvo in range(1, n):
            qc.cx(0, alvo)
    elif variante == 'conectado':
        if not arestas or len(arestas) != n - 1:
            raise ValueError('A variante conectado precisa de n-1 arestas (origem, destino)')
        qc.h(arestas[0][0])
        for origem, destino in arestas:
            qc.cx(origem, destino)
    else:
        raise ValueError(f'Variante desconhecida: {variante}')
    return qc


def prob_ideal(bits, n, base='Z', variante='original'):
    if len(bits) != n:
        raise ValueError('Sequência com tamanho diferente de n')
    if base == 'Z':
        return 0.5 if bits in ('0' * n, '1' * n) else 0.0
    return 2.0 ** (1 - n) if bits.count('1') % 2 == 0 else 0.0


def _pz(bits):
    return 1.0 if bits in ('0' * len(bits), '1' * len(bits)) else 0.0


def _cx(bits):
    return 1.0 if bits.count('1') % 2 == 0 else -1.0


INDICADORES = {
    'PZ': dict(base='Z', peso=_pz, tipo='fracao', ideal=1.0),
    'CX': dict(base='X', peso=_cx, tipo='correlacao', ideal=1.0),
}
