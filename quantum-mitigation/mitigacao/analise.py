"""Análise de uma sessão: indicadores brutos e ajustados, incerteza por bootstrap, contrastes
entre construções e ZNE. Explicação: fundamentos/indicadores.md e fundamentos/tecnicas/.

Valor bruto: calculado das contagens, com o erro padrão da fórmula (só amostragem).
Valor ajustado: depois da calibração de leitura, com o erro padrão do bootstrap, que refaz a
conta inteira (calibração e circuitos reamostrados juntos) em cada réplica.
"""
from pathlib import Path

import numpy as np

from mitigacao import circuitos, indicadores, registro
from mitigacao.tecnicas import leitura, zne

REPETICOES = 5000
LIMITE_DENSO = 8  # até este n a distribuição inteira (2**n valores) cabe em um array


def indicador_do_item(item):
    """(nome, peso(bits), tipo): PZ ou CX para o GHZ, 'sucesso' para os demais circuitos."""
    for nome, ind in circuitos.obter(item['circuito']).INDICADORES.items():
        if ind['base'] == item['base']:
            return nome, ind['peso'], ind['tipo']
    ideal = circuitos.prob_ideal_item(item)
    return 'sucesso', (lambda bits: 1.0 if ideal(bits) > 0 else 0.0), 'fracao'


def pesos(peso, n):
    return np.array([peso(f'{s:0{n}b}') for s in range(2 ** n)])


def vetor(contagens_item, n, shots):
    v = np.zeros(2 ** n)
    for bits, vezes in contagens_item.items():
        v[int(bits, 2)] += vezes
    return v / shots


def resumo(valor, replicas=None):
    r = dict(valor=float(valor))
    if replicas is not None:
        r['ep'] = float(np.std(replicas, ddof=1))
        r['ic95'] = [float(x) for x in np.quantile(replicas, [0.025, 0.975])]
    return r


def e_calibracao(item):
    return (item['circuito'] == 'simples' and item['rotulo'] is None and item['base'] == 'Z'
            and item['n'] > 1 and set(item['variante']) <= set('01'))


def _bruto(it, contagens_item, shots):
    item = it['item']
    nome, peso, tipo = indicador_do_item(item)
    v = indicadores.valor(indicadores.fracoes(contagens_item), peso)
    return dict(indicador=nome, circuito=item['circuito'], n=item['n'], variante=item['variante'],
                base=item['base'], fator=item['fator'], rotulo=item['rotulo'], qubits=item['qubits'],
                portas_2q=it['compilado']['portas_2q'], profundidade=it['compilado']['profundidade'],
                bruto=dict(valor=v, ep=indicadores.erro_padrao(v, shots, tipo)),
                ajustado=None, ganho=None, menor_quasi=None, referencia=None)


def _ajustar(medidos, cal, contagens, shots, repeticoes, semente, itens):
    """Calibração de leitura e bootstrap para os circuitos com o mesmo n da calibração."""
    n, qubits = cal[0]['item']['n'], cal[0]['item']['qubits']
    if len(cal) != 2 ** n or n > LIMITE_DENSO:
        raise ValueError('Calibração incompleta ou grande demais para esta análise')
    densos = [it for it in medidos if it['item']['n'] == n]
    a = leitura.matriz(contagens, n, qubits)
    p = np.array([vetor(contagens[it['nome']], n, shots) for it in densos])
    w = np.array([pesos(indicador_do_item(it['item'])[1], n) for it in densos])
    perms = [leitura.permutacao([tuple(m) for m in it['compilado']['mapa_medidas']], n) for it in densos]
    q = leitura.corrigir_varios(a, p, perms)
    bruto, ajustado = (w * p).sum(1), (w * q).sum(1)
    rng = np.random.default_rng(semente)
    rb, ra = np.empty((repeticoes, len(densos))), np.empty((repeticoes, len(densos)))
    for r in range(repeticoes):
        pb = rng.multinomial(shots, p) / shots
        ab = rng.multinomial(shots, a.T).T / shots
        rb[r] = (w * pb).sum(1)
        ra[r] = (w * leitura.corrigir_varios(ab, pb, perms)).sum(1)
    for j, it in enumerate(densos):
        d = itens[it['nome']]
        d['ajustado'] = resumo(ajustado[j], ra[:, j])
        d['ganho'] = resumo(ajustado[j] - bruto[j], ra[:, j] - rb[:, j])
        d['menor_quasi'] = float(q[j].min())
    return dict(nomes=[it['nome'] for it in densos], ajustado=ajustado, replicas=ra,
                condicionamento=float(np.linalg.cond(a)), pesos=w)


def _contrastes(itens, ajuste):
    """Conectado menos original, no mesmo n, base e fator."""
    grupos = {}
    for nome, d in itens.items():
        grupos.setdefault((d['n'], d['base'], d['fator'], d['rotulo']), {})[d['variante']] = nome
    saida = []
    ordem = lambda kv: (kv[0][0], kv[0][1] != 'Z', kv[0][2], str(kv[0][3]))  # noqa: E731  (PZ antes de CX)
    for (n, base, fator, rotulo), por in sorted(grupos.items(), key=ordem):
        if not {'original', 'conectado'} <= set(por):
            continue
        o, c = itens[por['original']], itens[por['conectado']]
        linha = dict(n=n, base=base, fator=fator, indicador=c['indicador'], ajustado=None,
                     bruto=dict(valor=c['bruto']['valor'] - o['bruto']['valor'],
                                ep=indicadores.erro_padrao_diferenca(o['bruto']['ep'], c['bruto']['ep'])))
        if ajuste and por['original'] in ajuste['nomes'] and por['conectado'] in ajuste['nomes']:
            io, ic = ajuste['nomes'].index(por['original']), ajuste['nomes'].index(por['conectado'])
            linha['ajustado'] = resumo(ajuste['ajustado'][ic] - ajuste['ajustado'][io],
                                       ajuste['replicas'][:, ic] - ajuste['replicas'][:, io])
        saida.append(linha)
    return saida


def _zne(itens, ajuste):
    """Extrapola a zero os valores ajustados nos fatores de ruído 1, 3 e 5."""
    grupos = {}
    for nome, d in itens.items():
        if d['rotulo'] is None and nome in ajuste['nomes']:
            grupos.setdefault((d['variante'], d['base'], d['n']), {})[d['fator']] = nome
    saida = []
    for (variante, base, n), por in sorted(grupos.items()):
        if not set(zne.FATORES) <= set(por):
            continue
        idx = [ajuste['nomes'].index(por[f]) for f in zne.FATORES]
        valor = zne.extrapolar(ajuste['ajustado'][idx])
        replicas = zne.extrapolar(ajuste['replicas'][:, idx])
        saida.append(dict(variante=variante, base=base, n=n, indicador=itens[por[1]]['indicador'],
                          nomes=[por[f] for f in zne.FATORES],
                          ajustado_por_fator=[float(v) for v in ajuste['ajustado'][idx]],
                          zne=resumo(valor, replicas),
                          zne_menos_fator1=resumo(valor - ajuste['ajustado'][idx[0]],
                                                  replicas - ajuste['replicas'][:, idx[0]])))
    return saida


def analisar(pasta, tecnicas=(), repeticoes=REPETICOES, semente=2026):
    """Analisa uma sessão coletada. tecnicas: nomes das técnicas da receita ('leitura', 'zne')."""
    ficha, contagens = registro.ler_sessao(pasta)
    if contagens is None:
        raise ValueError(f'{pasta}: a sessão ainda não tem contagens')
    shots = ficha['shots']
    cal = [i for i in ficha['itens'] if 'leitura' in tecnicas and e_calibracao(i['item'])]
    nomes_cal = {i['nome'] for i in cal}
    medidos = [i for i in ficha['itens'] if i['nome'] not in nomes_cal]
    itens = {it['nome']: _bruto(it, contagens[it['nome']], shots) for it in medidos}
    ajuste = _ajustar(medidos, cal, contagens, shots, repeticoes, semente, itens) if cal else None
    saida = dict(sessao=Path(pasta).name, experimento=ficha['experimento'], computador=ficha['computador'],
                 tipo=ficha['tipo'], data=ficha['data'], shots=shots, repeticoes_bootstrap=repeticoes,
                 condicionamento=ajuste['condicionamento'] if ajuste else None, itens=itens,
                 contrastes=_contrastes(itens, ajuste), zne=_zne(itens, ajuste) if ajuste and 'zne' in tecnicas else [])
    if ficha['tipo'] == 'simulador':
        from mitigacao import validacao
        saida['validacao'] = validacao.conferir(pasta, ficha, medidos, saida)
    return saida
