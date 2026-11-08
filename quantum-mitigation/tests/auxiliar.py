"""Itens e funções que mais de um teste usa."""
from mitigacao.execucao import simulador
from mitigacao.tecnicas import leitura, zne

Q5 = [0, 1, 2, 3, 4]


def itens_basicos(zne_fatores=False):
    """GHZ (original e conectado, em Z e X), as 32 calibrações e 4 controles, como nos experimentos 4 a 6."""
    ghz = [dict(circuito='ghz', n=5, variante=v, base=b, regiao=Q5) for v in ('original', 'conectado') for b in 'ZX']
    if zne_fatores:
        ghz = zne.expandir([dict(circuito='ghz', n=5, variante='conectado', base=b, regiao=Q5) for b in 'ZX'])
    controles = [dict(circuito='simples', n=5, variante=v, base=b, qubits=Q5, rotulo='controle')
                 for v, b in (('00000', 'Z'), ('11111', 'Z'), ('+++++', 'X'), ('++++-', 'X'))]
    return ghz + leitura.itens_calibracao(5, qubits=Q5) + controles


def vizinhos_sim(n):
    return simulador.vizinhos('simulador', n)
