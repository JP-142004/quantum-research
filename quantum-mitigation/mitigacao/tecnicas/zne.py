"""Extrapolação a ruído zero. Explicação: fundamentos/tecnicas/zne.md."""
import numpy as np

NOME = 'zne'
FATORES = (1, 3, 5)


def expandir(itens, fatores=FATORES):
    """Cada item vira uma versão por fator de ruído (preparação repetida U, U inverso, U...)."""
    return [dict(item, fator=f) for item in itens for f in fatores]


def pesos_intercepto(fatores=FATORES):
    """Pesos tais que sum(pesos * valores) é o valor, no fator 0, da reta de mínimos quadrados."""
    x = np.asarray(fatores, float)
    media = x.mean()
    return 1 / len(x) - media * (x - media) / np.sum((x - media) ** 2)


def extrapolar(valores, fatores=FATORES):
    """valores: um número por fator (a última dimensão pode ter réplicas de bootstrap)."""
    valores = np.asarray(valores, float)
    if valores.shape[-1] != len(fatores):
        raise ValueError('É preciso um valor para cada fator')
    return valores @ pesos_intercepto(fatores)
