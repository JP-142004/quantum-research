"""Experimento 8, parte B: calibração de leitura qubit a qubit em muitos qubits (10 e 20).

Não monta matrizes 2**n x 2**n. Cada indicador é uma soma sobre as sequências observadas (poucas, no máximo
as medidas do circuito) de produtos de elementos das 2 x 2 inversas, então vale também para 20 qubits.
Explicação e critérios: experimentos/08_leitura_escala/b_ibm/README.md.
"""
import numpy as np

from mitigacao import leitura_independencia as li
from mitigacao.analise import e_calibracao, indicador_do_item, resumo
from mitigacao.leitura_comparacao import MARGEM, decisao
from mitigacao.tecnicas import leitura

SEMENTE, REPETICOES = 2026, 5000
LIMITE_COND = leitura.LIMITE_CONDICIONAMENTO


def _lista(contagens, n):
    """(bits de cada sequência por bit clássico k = 0..n-1, vezes)."""
    chaves = list(contagens)
    bits = np.array([[int(b[n - 1 - k]) for k in range(n)] for b in chaves], dtype=np.int8)
    return bits, np.array([contagens[c] for c in chaves], dtype=float)


def tabelas(grupo, n):
    """Uma tabela 2 x 2 por bit clássico, T[lido, preparado], com as calibrações do grupo.

    grupo: [(preparado: array de n bits, bits observados, vezes)].
    """
    saida = []
    for k in range(n):
        conta = np.zeros((2, 2))
        for preparado, bits, vezes in grupo:
            for lido in (0, 1):
                conta[lido, preparado[k]] += vezes[bits[:, k] == lido].sum()
        totais = conta.sum(axis=0)
        if np.any(totais == 0):
            raise ValueError(f'Sem medidas para uma condição do bit {k}')
        saida.append(conta / totais)
    return saida


def _inversas(ts):
    for t in ts:
        if not np.isfinite(np.linalg.cond(t)) or np.linalg.cond(t) > LIMITE_COND:
            raise ValueError('Calibração instável')
    return [np.linalg.inv(t) for t in ts]


def indicador(tipo, bits, vezes, inv, ideal=None):
    """Valor do indicador. tipo: 'PZ', 'CX' ou 'sucesso'. inv=None dá o valor observado."""
    p, n = vezes / vezes.sum(), bits.shape[1]
    if inv is None:
        a0 = (bits == 0).astype(float)
        a1 = (bits == 1).astype(float)
    else:
        a0 = np.stack([inv[k][0, bits[:, k]] for k in range(n)], axis=1)
        a1 = np.stack([inv[k][1, bits[:, k]] for k in range(n)], axis=1)
    if tipo == 'PZ':
        g = a0.prod(axis=1) + a1.prod(axis=1)
    elif tipo == 'CX':
        g = (a0 - a1).prod(axis=1) if inv is not None else 1.0 - 2.0 * (bits.sum(axis=1) % 2)
    else:
        g = np.prod([a1[:, k] if ideal[k] else a0[:, k] for k in range(n)], axis=0)
    return float(p @ g)


def _ideal(item):
    """Bits (por bit clássico k) do resultado esperado de um controle."""
    sim = {'0': 0, '1': 1, '+': 0, '-': 1}
    return [sim[c] for c in item['variante'][::-1]]


def _preparado(variante):
    return np.array([int(c) for c in variante[::-1]], dtype=np.int8)


def analisar_tamanho(ficha, contagens, n, repeticoes=REPETICOES, semente=SEMENTE):
    """Resultados de uma sessão para um tamanho n."""
    itens = [i for i in ficha['itens'] if i['item']['n'] == n]
    cal = [i for i in itens if e_calibracao(i['item'])]
    alvos = [i for i in itens if i not in cal]
    estados = {i['item']['variante']: i for i in cal}
    zeros, uns = '0' * n, '1' * n
    alt1, alt2 = ('01' * n)[:n], ('10' * n)[:n]
    ref = estados[zeros]
    for i in itens:   # a tabela vale por bit clássico: as calibrações e os circuitos precisam usar os mesmos qubits
        if i['qubits_fisicos'] != ref['qubits_fisicos'] or i['compilado']['mapa_medidas'] != ref['compilado']['mapa_medidas']:
            raise ValueError(f'{i["nome"]} usa outros qubits que a calibração; a análise por bit não vale')
    dados = {v: _lista(contagens[estados[v]['nome']], n) for v in (zeros, uns, alt1, alt2)}
    alvo_dados = {i['nome']: _lista(contagens[i['nome']], n) for i in alvos}
    grupos = dict(dois=(zeros, uns), quatro=(zeros, uns, alt1, alt2))

    def estima(rng):
        """Uma réplica (ou a conta original, com rng=None): tabelas, indicadores observados e ajustados."""
        def amostra(bits_vezes):
            bits, vezes = bits_vezes
            return bits, (vezes if rng is None else rng.multinomial(int(vezes.sum()), vezes / vezes.sum()).astype(float))
        cal_r = {v: amostra(d) for v, d in dados.items()}
        alvo_r = {nome: amostra(d) for nome, d in alvo_dados.items()}
        saida = {}
        for g, vs in grupos.items():
            inv = _inversas(tabelas([(_preparado(v), *cal_r[v]) for v in vs], n))
            saida[g] = {}
            for i in alvos:
                nome_ind, _, _ = indicador_do_item(i['item'])
                bits, vezes = alvo_r[i['nome']]
                ideal = _ideal(i['item']) if nome_ind == 'sucesso' else None
                obs, aj = indicador(nome_ind, bits, vezes, None, ideal), indicador(nome_ind, bits, vezes, inv, ideal)
                saida[g][i['nome']] = (obs, aj)
        tu, ta = (tabelas([(_preparado(v), *cal_r[v]) for v in vs], n) for vs in ((zeros, uns), (alt1, alt2)))
        contexto = np.array([[b[1, 0] - a[1, 0], b[0, 1] - a[0, 1]] for a, b in zip(tu, ta)])  # (n, 2): e01, e10
        return saida, contexto

    ponto, ctx0 = estima(None)
    rng, replicas, ctx, falhas = np.random.default_rng(semente), [], [], 0
    for _ in range(repeticoes):
        try:
            s, c = estima(rng)
        except ValueError:
            falhas += 1
            continue
        replicas.append(s), ctx.append(c)
    ctx = np.array(ctx)
    saida = dict(n=n, replicas_com_falha=falhas, metodos={}, margem=MARGEM)
    for g in grupos:
        lista = []
        for i in alvos:
            nome_ind, _, tipo = indicador_do_item(i['item'])
            obs0, aj0 = ponto[g][i['nome']]
            r = np.array([[x[g][i['nome']][0], x[g][i['nome']][1]] for x in replicas])
            ganho = np.abs(r[:, 0] - 1) - np.abs(r[:, 1] - 1)
            lista.append(dict(nome=i['nome'], indicador=nome_ind, rotulo=i['item']['rotulo'], base=i['item']['base'],
                              variante=i['item']['variante'], observado=resumo(obs0, r[:, 0]), ajustado=resumo(aj0, r[:, 1]),
                              ganho=resumo(abs(obs0 - 1) - abs(aj0 - 1), ganho)))
        saida['metodos'][g] = lista
    dif = np.quantile(ctx, [0.025, 0.975], axis=0)   # (2, n, 2)
    saida['contexto'] = dict(valor=ctx0.tolist(), ic95=[dif[0].tolist(), dif[1].tolist()], margem=MARGEM,
                             decisoes=[[decisao([dif[0][k, j], dif[1][k, j]]) for j in range(2)] for k in range(n)])
    saida['independencia'] = {}
    for nome, v in (('zeros', zeros), ('uns', uns)):
        e = li.erros(contagens[estados[v]['nome']], v)
        r = li.teste(e, np.random.default_rng(semente), 1000)
        saida['independencia'][nome] = dict(r, pares=li.pares_mais_ligados(e, 3))
    return saida
