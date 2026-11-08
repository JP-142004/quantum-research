"""Conferência da análise com a referência exata do modelo. Só vale no simulador, onde o erro
é conhecido: a referência é a distribuição exata, sem flutuação de shots."""
import numpy as np

from mitigacao import registro
from mitigacao.analise import LIMITE_DENSO, indicador_do_item, pesos
from mitigacao.execucao.ruido import referencia_exata
from mitigacao.tecnicas import zne

LIMITE_SANIDADE = 6  # erros padrão


def _z(diferenca, ep):
    if ep > 1e-9:
        return abs(diferenca) / ep
    return 0.0 if abs(diferenca) < 1e-8 else float('inf')


def conferir(pasta, ficha, medidos, resultado):
    """Acrescenta a referência exata a cada item e devolve o resumo da conferência.

    Bruto contra o valor exato depois da leitura (observado); ajustado contra o valor exato
    antes da leitura. Os dois desvios saem em erros padrão. É uma sanidade, não um teste de
    cobertura dos intervalos.
    """
    compilados = dict(zip(ficha['ordem'], registro.ler_circuitos(pasta)))
    pequenos = {it['nome']: it for it in medidos if it['item']['n'] <= LIMITE_DENSO}
    ref = referencia_exata({nome: compilados[nome] for nome in pequenos}, ficha['opcoes']['cenario'])
    itens, z_bruto, z_ajustado = resultado['itens'], [], []
    for nome, r in ref.items():
        d, it = itens[nome], pequenos[nome]
        w = pesos(indicador_do_item(it['item'])[1], it['item']['n'])
        antes, observado = float(w @ r['antes_leitura']), float(w @ r['observado'])
        d['referencia'] = dict(antes_leitura=antes, observado=observado)
        z_bruto.append(_z(d['bruto']['valor'] - observado, d['bruto']['ep']))
        if d['ajustado']:
            z_ajustado.append(_z(d['ajustado']['valor'] - antes, d['ajustado']['ep']))
    for grupo in resultado['zne']:
        por_fator = [itens[nome]['referencia']['antes_leitura'] for nome in grupo['nomes']]
        grupo['referencia'] = dict(antes_leitura_por_fator=por_fator, zne=float(zne.extrapolar(por_fator)))
    maior_b, maior_a = max(z_bruto), max(z_ajustado, default=0.0)
    return dict(cenario=ficha['opcoes']['cenario'], maior_desvio_bruto_em_ep=maior_b,
                maior_desvio_ajustado_em_ep=maior_a, limite=LIMITE_SANIDADE,
                aprovado=bool(maior_b <= LIMITE_SANIDADE and maior_a <= LIMITE_SANIDADE))
