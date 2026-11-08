"""Tabelas que só fazem sentido no simulador: referência exata do modelo, validação e ZNE."""
from mitigacao.tabelas import fmt, pm, tabela


def t_validacao(res):
    linhas = [(s, r['validacao']['cenario'], fmt(r['validacao']['maior_desvio_bruto_em_ep'], 2),
               fmt(r['validacao']['maior_desvio_ajustado_em_ep'], 2), 'sim' if r['validacao']['aprovado'] else 'NÃO')
              for s, r in res.items()]
    return tabela(['Sessão', 'Cenário', 'Maior desvio do bruto (EP)', 'Maior desvio do ajustado (EP)', 'Dentro do limite'],
                  linhas, (2, 3))


def t_cenarios(res):
    """Referência exata do modelo, antes e depois da leitura (um bloco por cenário)."""
    vistos, linhas = set(), []
    for r in res.values():
        cenario = r['validacao']['cenario']
        if cenario in vistos:
            continue
        vistos.add(cenario)
        for variante in ('original', 'conectado'):
            ref = {d['indicador']: d['referencia'] for d in r['itens'].values()
                   if d['circuito'] == 'ghz' and d['variante'] == variante and d['fator'] == 1}
            linhas.append((cenario, variante, *[fmt(ref[i][k]) for i in ('PZ', 'CX') for k in ('antes_leitura', 'observado')]))
    return tabela(['Cenário', 'Construção', 'PZ antes da leitura', 'PZ após a leitura', 'CX antes da leitura',
                   'CX após a leitura'], linhas, range(2, 6))


def t_zne_exato(res):
    """Referência exata nos fatores 1, 3 e 5 e a extrapolação, a partir do primeiro bloco."""
    z = {g['base']: g for g in next(r for r in res.values() if r['zne'])['zne']}
    itens = next(r for r in res.values() if r['zne'])['itens']
    linhas = [(f, itens[z['Z']['nomes'][i]]['portas_2q'], fmt(z['Z']['referencia']['antes_leitura_por_fator'][i]),
               fmt(z['X']['referencia']['antes_leitura_por_fator'][i])) for i, f in enumerate((1, 3, 5))]
    linhas.append(('0 (extrapolado)', '—', f"**{fmt(z['Z']['referencia']['zne'])}**", f"**{fmt(z['X']['referencia']['zne'])}**"))
    return tabela(['Fator de ruído', 'Portas de 2 qubits', 'PZ (referência exata)', 'CX (referência exata)'], linhas, (1, 2, 3))


def t_zne_blocos(res):
    linhas = []
    for s, r in res.items():
        for g in r['zne']:
            f1 = r['itens'][g['nomes'][0]]['ajustado']
            linhas.append((s, g['indicador'], pm(f1), pm(g['zne']), fmt(g['referencia']['antes_leitura_por_fator'][0]),
                           fmt(g['referencia']['zne'])))
    return tabela(['Sessão', 'Indicador', 'Ajustado, fator 1', 'Após ZNE', 'Exato, fator 1', 'Exato após ZNE'],
                  linhas, range(2, 6))
