"""Experimento 8, parte B: tabelas, figura e veredito dos critérios (README da parte B), das sessões da IBM."""
import json

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt  # noqa: E402

from mitigacao import registro, tabelas  # noqa: E402
from mitigacao.graficos import _salvar  # noqa: E402
from mitigacao.graficos_ibm import _dia  # noqa: E402
from mitigacao.leitura_ibm import analisar_tamanho  # noqa: E402

TAMANHOS = (10, 20)
SESSOES_PREVISTAS = 3


def veredito_independencia(ind):
    """Regra do README: não rejeitada se p > 0,01 nos dois estados; rejeitada se p <= 0,001 em algum."""
    ps = [v['p_valor'] for v in ind.values()]
    return 'rejeitada' if min(ps) <= 0.001 else 'não rejeitada' if min(ps) > 0.01 else 'inconclusiva'


def veredito_contexto(dec):
    planas = [d for linha in dec for d in linha]
    return 'diferente' if 'diferente' in planas else 'equivalente' if set(planas) == {'equivalente'} else 'inconclusivo'


def _ghz(r, g='dois'):
    return [x for x in r['metodos'][g] if x['rotulo'] is None]


def _controles(r, g='dois'):
    return [x for x in r['metodos'][g] if x['rotulo'] == 'controle']


def ganho_ok(r):
    return all(x['ganho']['ic95'][0] > 0 for x in _ghz(r))


def controles_ok(r):
    return all(abs(x['ajustado']['valor'] - 1) <= 2 * x['ajustado']['ep'] for x in _controles(r))


def t_independencia(res):
    linhas = [(s, n, nome, tabelas.fmt(i['taxa_de_erro'], 3), tabelas.fmt(i['T'], 3), tabelas.fmt(i['p_valor'], 3),
               ', '.join(f'{a}–{b}: {o}/{tabelas.fmt(e, 1)}' for a, b, o, e in i['pares'][:2]))
              for (s, n), r in res.items() for nome, i in r['independencia'].items()]
    return tabelas.tabela(['Sessão', 'n', 'Estado', 'Taxa de erro', 'T', 'p-valor', 'Pares com mais erros juntos (observado/esperado)'],
                          linhas, (1, 3, 4, 5))


def t_contexto(res):
    linhas = []
    for (s, n), r in res.items():
        c = r['contexto']
        planas = [d for linha in c['decisoes'] for d in linha]
        maior = max(abs(x) for linha in c['valor'] for x in linha)
        linhas.append((s, n, tabelas.fmt(maior, 3), *[planas.count(d) for d in ('equivalente', 'inconclusivo', 'diferente')],
                       veredito_contexto(c['decisoes'])))
    return tabelas.tabela(['Sessão', 'n', 'Maior diferença', 'Equivalentes', 'Inconclusivas', 'Diferentes', 'Resultado'],
                          linhas, (1, 2, 3, 4, 5))


def t_ghz(res):
    linhas = []
    for (s, n), r in res.items():
        for x, y in zip(_ghz(r), _ghz(r, 'quatro')):
            g = x['ganho']
            linhas.append((s, n, x['indicador'], tabelas.pm(x['observado']), tabelas.pm(x['ajustado']),
                           f"{tabelas.fmt(g['valor'], 3)} [{tabelas.fmt(g['ic95'][0], 3)}; {tabelas.fmt(g['ic95'][1], 3)}]",
                           tabelas.pm(y['ajustado'])))
    return tabelas.tabela(['Sessão', 'n', 'Indicador', 'Observado', 'Ajustado (2 estados)', 'Ganho [IC 95%]',
                           'Ajustado (4 estados)'], linhas, (1, 3, 4, 5, 6))


def t_controles(res):
    linhas = [(s, n, f"`{x['variante']}` em {x['base']}", tabelas.pm(x['observado']), tabelas.pm(x['ajustado']),
               tabelas.fmt((x['ajustado']['valor'] - 1) / x['ajustado']['ep'], 1))
              for (s, n), r in res.items() for x in _controles(r)]
    return tabelas.tabela(['Sessão', 'n', 'Controle', 'Observado', 'Ajustado (2 estados)', '(ajustado − 1) / erro padrão'],
                          linhas, (1, 3, 4, 5))


def t_criterios(res):
    linhas = []
    for n in TAMANHOS:
        rs = [r for (s, m), r in res.items() if m == n]
        if not rs:
            continue
        falta = '' if len(rs) == SESSOES_PREVISTAS else f' (só {len(rs)} de {SESSOES_PREVISTAS} sessões)'
        linhas.append((n, ' / '.join(veredito_independencia(r['independencia']) for r in rs),
                       ' / '.join(veredito_contexto(r['contexto']['decisoes']) for r in rs),
                       ' / '.join('sim' if ganho_ok(r) else 'não' for r in rs),
                       ' / '.join('sim' if controles_ok(r) else 'não' for r in rs) + falta))
    return tabelas.tabela(['n', 'Erros conjuntos', 'Dependência dos vizinhos', 'GHZ melhorou (PZ e CX)', 'Controles a 2 erros padrão'],
                          linhas)


def figura(res, caminho):
    fig, eixos = plt.subplots(1, 2, figsize=(11, 4.5))
    chaves = list(res)
    for ax, indicador in zip(eixos, ('PZ', 'CX')):
        for i, chave in enumerate(chaves):
            x = next(x for x in _ghz(res[chave]) if x['indicador'] == indicador)
            ax.errorbar(i - 0.1, x['observado']['valor'], yerr=x['observado']['ep'], fmt='s', color='#999999',
                        markerfacecolor='white', capsize=3, label='observado' if i == 0 else None)
            ax.errorbar(i + 0.1, x['ajustado']['valor'], yerr=x['ajustado']['ep'], fmt='o', color='#008675', capsize=3,
                        label='ajustado (calibração por qubit)' if i == 0 else None)
        ax.axhline(1, color='gray', ls='--', lw=1)
        ax.set(title=f'GHZ conectado, {indicador}', ylabel='Indicador (ideal = 1)', xticks=range(len(chaves)),
               xticklabels=[f'{n} qubits\n{_dia(s)}' for s, n in chaves])
    eixos[0].legend(fontsize=8)
    fig.tight_layout()
    _salvar(fig, caminho)


def gerar(pasta_b, repeticoes=None):
    """Lê as sessões de pasta_b/dados e grava pasta_b/resultados e as tabelas do README."""
    res = {}
    for sessao in registro.listar_sessoes(pasta_b):
        ficha, contagens = registro.ler_sessao(sessao)
        if contagens is None:
            continue
        for n in (m for m in TAMANHOS if any(i['item']['n'] == m for i in ficha['itens'])):
            print(f'Analisando {sessao.name}, {n} qubits...', flush=True)
            res[(sessao.name, n)] = analisar_tamanho(ficha, contagens, n, *([repeticoes] if repeticoes else []))
    if not res:
        raise ValueError('Nenhuma sessão coletada em dados/')
    saida = pasta_b / 'resultados'
    saida.mkdir(exist_ok=True)
    (saida / 'resultados_ibm.json').write_text(json.dumps({f'{s}|{n}': r for (s, n), r in res.items()},
                                                          ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    t = dict(independencia=t_independencia(res), contexto=t_contexto(res), ghz=t_ghz(res), controles=t_controles(res),
             criterios=t_criterios(res))
    (saida / 'tabelas_ibm.md').write_text('# Tabelas geradas dos dados (não editar à mão)\n\n'
                                          + '\n\n'.join(f'## {k}\n\n{v}' for k, v in t.items()) + '\n', encoding='utf-8')
    figura(res, saida / 'ghz_10_e_20_qubits.png')
    readme = pasta_b / 'README.md'
    texto = readme.read_text(encoding='utf-8')
    novo = tabelas.preencher(texto, t, parcial=True)   # a tabela `piloto` vem do piloto.py
    if novo != texto:
        readme.write_text(novo, encoding='utf-8')
    return dict(sessoes=sorted({s for s, _ in res}), tabelas=list(t), figuras=['ghz_10_e_20_qubits.png'])
