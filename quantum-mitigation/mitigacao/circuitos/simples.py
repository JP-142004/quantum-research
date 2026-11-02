"""Estados simples, um símbolo por qubit: '0', '1', '+' ou '-'.

A variante é a sequência de n símbolos, escrita como as contagens: o símbolo da direita é o
qubit 0. Servem de controle (resposta conhecida) e de calibração de leitura.
Explicação: fundamentos/conceitos.md.
"""
from qiskit import QuantumCircuit

NOME = 'simples'
VARIANTES = "sequência de n símbolos '0', '1', '+' ou '-' (o da direita é o qubit 0)"
INDICADORES = {}
EXEMPLOS = [(1, '1'), (3, '010'), (2, '+-'), (5, '++++-'), (4, '0+1-')]  # (n, variante), usados nos testes


def _simbolos(n, variante):
    if len(variante) != n or set(variante) - set('01+-'):
        raise ValueError("A variante deve ter n símbolos entre '0', '1', '+' e '-'")
    return variante[::-1]  # posição q = símbolo do qubit q


def preparacao(n, variante, arestas=None):
    qc = QuantumCircuit(n)
    for q, simbolo in enumerate(_simbolos(n, variante)):
        if simbolo in '1-':
            qc.x(q)
        if simbolo in '+-':
            qc.h(q)
    return qc


def prob_ideal(bits, n, base='Z', variante='0'):
    """Produto das probabilidades de cada qubit. Na base Z, '+' e '-' dão 1/2; na base X,
    '0' e '1' dão 1/2, '+' dá 0 e '-' dá 1."""
    if len(bits) != n:
        raise ValueError('Sequência com tamanho diferente de n')
    prob = 1.0
    for q, simbolo in enumerate(_simbolos(n, variante)):
        bit = bits[n - 1 - q]
        determinado = simbolo in '01' if base == 'Z' else simbolo in '+-'
        if not determinado:
            prob *= 0.5
        elif bit != (simbolo if base == 'Z' else '0' if simbolo == '+' else '1'):
            return 0.0
    return prob
