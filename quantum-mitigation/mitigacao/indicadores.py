"""Indicadores gerais e conta do erro padrão. Explicação: fundamentos/indicadores.md.

Uma distribuição é um dict sequência_de_bits -> fração (ou quasiprobabilidade, depois de
um ajuste). Os indicadores específicos de cada circuito são somas ponderadas dessa
distribuição, por isso valem para contagens brutas e para estimativas ajustadas.
"""
from math import sqrt


def fracoes(contagens):
    """Contagens (bits -> número de vezes) em frações que somam 1."""
    total = sum(contagens.values())
    return {bits: vezes / total for bits, vezes in contagens.items()}


def valor(prob, peso):
    """Soma de peso(bits) * prob(bits). Dá PZ, CX e qualquer indicador linear."""
    return float(sum(peso(bits) * p for bits, p in prob.items()))


def probabilidade_sucesso(prob, prob_ideal):
    """Fração que caiu em resultados que o circuito ideal pode produzir."""
    return float(sum(p for bits, p in prob.items() if prob_ideal(bits) > 0))


def distancia_ideal(prob, prob_ideal):
    """Metade da soma de |observado - ideal| sobre todas as sequências.

    Só percorre as sequências observadas: a massa ideal das não observadas é
    1 menos a massa ideal das observadas.
    """
    q = {bits: prob_ideal(bits) for bits in prob}
    return float(0.5 * (sum(abs(p - q[bits]) for bits, p in prob.items()) + 1 - sum(q.values())))


def erro_padrao(v, n, tipo):
    """Erro padrão só pela amostragem. tipo: 'fracao' ou 'correlacao'."""
    if tipo == 'fracao':
        variancia = v * (1 - v)
    elif tipo == 'correlacao':
        variancia = 1 - v ** 2
    else:
        raise ValueError("tipo deve ser 'fracao' ou 'correlacao'")
    return sqrt(max(0.0, variancia) / n)


def erro_padrao_diferenca(e1, e2):
    """Erro padrão da diferença de dois valores independentes."""
    return sqrt(e1 ** 2 + e2 ** 2)
