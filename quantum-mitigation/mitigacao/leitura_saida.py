"""Experimento 7: tabelas, figura e resultados.json da comparação de leitura. Nenhum número é digitado à mão."""
import json

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

from mitigacao import registro, tabelas  # noqa: E402
from mitigacao.graficos import _salvar  # noqa: E402
from mitigacao.graficos_ibm import _dia  # noqa: E402
from mitigacao.leitura_comparacao import COMPARACOES, MARGEM, MODELOS, comparar  # noqa: E402

NOME = dict(completo='completo', fatorizado='fatorizado (a)', fatorizado_dois='fatorizado (b)')
CONTROLES = ('00000 em Z', '11111 em Z', '+++++ em X', '++++- em X')


def _ghz(r):
    return [d for d in r['itens'] if d['circuito'] == 'ghz']


def t_metodos(res):
    linhas = [(s, d['indicador'], tabelas.pm(d['observado']), *[tabelas.pm(d['ajustado'][m]) for m in MODELOS])
              for s, r in res.items() for d in _ghz(r)]
    return tabelas.tabela(['Sessão', 'Indicador', 'Observado', *[NOME[m] for m in MODELOS]], linhas, range(2, 6))


def t_diferencas(res):
    linhas = []
    for s, r in res.items():
        for d in _ghz(r):
            for a, b in COMPARACOES:
                x = d['diferencas'][f'{a}-{b}']
                linhas.append((s, d['indicador'], f'{NOME[a]} − {NOME[b]}', tabelas.fmt(x['valor'], 3),
                               f"[{tabelas.fmt(x['ic95'][0], 3)}; {tabelas.fmt(x['ic95'][1], 3)}]", x['decisao']))
    return tabelas.tabela(['Sessão', 'Indicador', 'Diferença', 'Valor', 'Intervalo de 95%', 'Decisão'], linhas, (3,))


def t_controles(res):
    """Controles independentes: ajustado menos o ideal (que é 1), por método."""
    linhas = [(s, NOME[m], *[tabelas.fmt(d['ajustado'][m]['valor'] - 1, 3) for d in r['itens'] if d['rotulo'] == 'controle'])
              for s, r in res.items() for m in MODELOS]
    return tabelas.tabela(['Sessão', 'Método', *CONTROLES], linhas, range(2, 6))


def t_previsao(res):
    """Metade das medidas monta o modelo; a outra metade é comparada com a distribuição prevista."""
    linhas = [(s, *[f"{tabelas.fmt(r['previsao'][m]['media'], 4)} ({tabelas.fmt(r['previsao'][m]['maximo'], 4)})"
                    for m in MODELOS]) for s, r in res.items()]
    return tabelas.tabela(['Sessão', *[NOME[m] for m in MODELOS]], linhas, range(1, 4))


def t_diagnostico(res):
    def tres(f):
        return ' / '.join(f(m) for m in MODELOS)
    linhas = [(s, tres(lambda m: f"{r['condicionamento'][m]:.2f}".replace('.', ',')),
               tres(lambda m: tabelas.fmt(min(d['menor_quasi'][m] for d in _ghz(r)), 4)), r['replicas_com_falha'])
              for s, r in res.items()]
    return tabelas.tabela(['Sessão', 'Condicionamento', 'Menor quasiprobabilidade do GHZ', 'Réplicas com falha'],
                          linhas, range(1, 4))


def figura(res, caminho):
    """Em cima, o indicador por método; embaixo, as diferenças com o intervalo de 95% e a faixa da margem."""
    fig, eixos = plt.subplots(2, 2, figsize=(10, 7.5))
    x = np.arange(len(res))
    cor = dict(observado='#999999', completo='#526b91', fatorizado='#008675', fatorizado_dois='#c4721a')
    for col, indicador in enumerate(('PZ', 'CX')):
        itens = [next(d for d in _ghz(r) if d['indicador'] == indicador) for r in res.values()]
        ax = eixos[0, col]
        ax.errorbar(x - 0.24, [d['observado']['valor'] for d in itens], yerr=[d['observado']['ep'] for d in itens],
                    fmt='s', color=cor['observado'], markerfacecolor='white', capsize=3, label='observado')
        for k, m in enumerate(MODELOS):
            ax.errorbar(x - 0.08 + 0.16 * k, [d['ajustado'][m]['valor'] for d in itens],
                        yerr=[d['ajustado'][m]['ep'] for d in itens], fmt='o', color=cor[m], capsize=3,
                        label=f'ajustado, {NOME[m]}')
        ax.axhline(1, color='gray', ls='--', lw=1)
        ax.set(title=indicador, ylabel='Indicador (ideal = 1)', xticks=x, xticklabels=[_dia(s) for s in res])
        ax = eixos[1, col]
        ax.axhspan(-MARGEM, MARGEM, color='#dddddd', label=f'margem ±{MARGEM}')
        ax.axhline(0, color='gray', lw=1)
        for k, (a, b) in enumerate(COMPARACOES):
            v = [d['diferencas'][f'{a}-{b}'] for d in itens]
            ax.errorbar(x - 0.16 + 0.16 * k, [e['valor'] for e in v],
                        yerr=[[e['valor'] - e['ic95'][0] for e in v], [e['ic95'][1] - e['valor'] for e in v]],
                        fmt='o', capsize=3, label=f'{NOME[a]} − {NOME[b]}')
        ax.set(ylabel='Diferença entre ajustados', xticks=x, xticklabels=[_dia(s) for s in res])
    for linha in eixos:
        h, l = linha[0].get_legend_handles_labels()
        linha[0].legend(h, l, fontsize=7, loc='lower center', bbox_to_anchor=(1.1, -0.38), ncol=3, frameon=False)
    fig.tight_layout(rect=(0, 0.02, 1, 1))
    _salvar(fig, caminho)


def gerar(pasta_exp, pasta_dados_exp, repeticoes=None):
    """Lê as sessões do experimento 4 (pasta_dados_exp, só leitura) e grava em pasta_exp/resultados."""
    sessoes = [s for s in registro.listar_sessoes(pasta_dados_exp) if (s / 'contagens.json').exists()]
    res = {}
    for s in sessoes:
        print(f'Analisando {s.name}...', flush=True)
        res[s.name] = comparar(s) if repeticoes is None else comparar(s, repeticoes)
    saida = pasta_exp / 'resultados'
    saida.mkdir(exist_ok=True)
    (saida / 'resultados.json').write_text(json.dumps(res, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    t = dict(metodos=t_metodos(res), diferencas=t_diferencas(res), controles=t_controles(res),
             previsao=t_previsao(res), diagnostico=t_diagnostico(res))
    (saida / 'tabelas.md').write_text('# Tabelas geradas dos dados (não editar à mão)\n\n'
                                      + '\n\n'.join(f'## {n}\n\n{x}' for n, x in t.items()) + '\n', encoding='utf-8')
    figura(res, saida / 'comparacao_leitura.png')
    readme = pasta_exp / 'README.md'
    texto = readme.read_text(encoding='utf-8')
    novo = tabelas.preencher(texto, t)
    if novo != texto:
        readme.write_text(novo, encoding='utf-8')
    return dict(sessoes=list(res), tabelas=list(t), figuras=['comparacao_leitura.png'])
