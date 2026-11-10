"""Figuras dos experimentos na IBM: cada sessão (dia) aparece separada, nunca juntada numa média."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

from mitigacao.graficos import COR, _salvar  # noqa: E402

MARCADORES = ('o', 's', '^', 'D')


def _dia(sessao):
    """2026-11-08_ibm_fez -> 08/11/2026."""
    a, m, d = sessao.split('_')[0].split('-')
    return f'{d}/{m}/{a}'


def _legenda(fig, eixo, colunas=3):
    h, l = eixo.get_legend_handles_labels()
    fig.legend(h, l, loc='lower center', ncol=colunas, fontsize=8)


def escala(res, caminho):
    """Experimento 1: PZ do GHZ original em cada tamanho, uma linha por sessão."""
    fig, ax = plt.subplots(figsize=(7.5, 4.3))
    for i, (s, r) in enumerate(res.items()):
        d = sorted((d for d in r['itens'].values()), key=lambda d: d['n'])
        ax.errorbar([x['n'] + (i - 1) * 0.6 for x in d], [x['bruto']['valor'] for x in d],
                    yerr=[x['bruto']['ep'] for x in d], fmt=MARCADORES[i] + '-', capsize=2, lw=1, ms=5, label=_dia(s))
    ax.axhline(1, color='gray', ls='--', lw=1)
    ax.set(xlabel='Número de qubits', ylabel='PZ observado (ideal = 1)', xticks=range(5, 55, 5), ylim=(-0.03, 1.05))
    ax.grid(alpha=0.2)
    _legenda(fig, ax)
    fig.tight_layout(rect=(0, 0.07, 1, 1))
    _salvar(fig, caminho)


def controles(res, caminho):
    """Experimento 2: fração de respostas certas em cada pedido, uma marca por sessão."""
    itens = list(next(iter(res.values()))['itens'].items())
    fig, ax = plt.subplots(figsize=(7, 5))
    y = np.arange(len(itens))[::-1]
    for i, (s, r) in enumerate(res.items()):
        ax.errorbar([r['itens'][n]['bruto']['valor'] for n, _ in itens], y + (i - 1) * 0.2,
                    xerr=[r['itens'][n]['bruto']['ep'] for n, _ in itens], fmt=MARCADORES[i], capsize=2, ms=5, label=_dia(s))
    ax.set_yticks(y)
    ax.set_yticklabels([_nome_controle(d) for _, d in itens], fontsize=8)
    ax.axvline(1, color='gray', ls='--', lw=1)
    ax.set(xlabel='Fração de respostas certas (ideal = 1)', xlim=(0.86, 1.01))
    ax.grid(axis='x', alpha=0.2)
    _legenda(fig, ax)
    fig.tight_layout(rect=(0, 0.07, 1, 1))
    _salvar(fig, caminho)


def _nome_controle(d):
    return f"{d['variante']} (5 qubits)" if d['n'] == 5 else f"{d['variante']} no qubit {d['qubits'][0]}"


def construcao(res, caminho):
    """Experimento 3: original e conectado em 5, 10 e 20 qubits, PZ e CX, uma marca por sessão."""
    tamanhos = sorted({d['n'] for r in res.values() for d in r['itens'].values()})
    fig, eixos = plt.subplots(1, 2, figsize=(10, 4.3), sharey=True)
    for ax, indicador, base in zip(eixos, ('PZ', 'CX'), ('Z', 'X')):
        for variante, desloc in (('original', -0.17), ('conectado', 0.17)):
            for i, (s, r) in enumerate(res.items()):
                d = [next(x for x in r['itens'].values() if x['variante'] == variante and x['base'] == base and x['n'] == n)
                     for n in tamanhos]
                ax.errorbar(np.arange(len(tamanhos)) + desloc + (i - 1) * 0.05, [x['bruto']['valor'] for x in d],
                            yerr=[x['bruto']['ep'] for x in d], fmt=MARCADORES[i], color=COR[variante], capsize=2, ms=5,
                            label=f'{variante} · {_dia(s)}')
        ax.axhline(1, color='gray', ls='--', lw=1)
        ax.set(xticks=range(len(tamanhos)), xticklabels=tamanhos, xlabel='Número de qubits', title=indicador, ylim=(-0.08, 1.05))
        ax.grid(axis='y', alpha=0.2)
    eixos[0].set_ylabel('Indicador observado (ideal = 1)')
    _legenda(fig, eixos[0], 3)
    fig.tight_layout(rect=(0, 0.14, 1, 1))
    _salvar(fig, caminho)


def calibracao(res, caminho):
    """Experimento 4: bruto (vazado) e ajustado (cheio) do GHZ e dos 4 controles, por sessão."""
    itens = list(next(iter(res.values()))['itens'].items())
    itens = [(n, d) for n, d in itens if d['ajustado']]
    rot = [f"GHZ {d['indicador']}" if d['circuito'] == 'ghz' else f"controle\n{d['variante']}" for _, d in itens]
    fig, ax = plt.subplots(figsize=(10, 4.4))
    for i, (s, r) in enumerate(res.items()):
        x = np.arange(len(itens)) + (i - 1) * 0.22
        for chave, extra, cheio in (('bruto', -0.04, False), ('ajustado', 0.04, True)):
            d = [r['itens'][n][chave] for n, _ in itens]
            ax.errorbar(x + extra, [v['valor'] for v in d], yerr=[v['ep'] for v in d], fmt=MARCADORES[i], capsize=2, ms=5,
                        color='#526b91' if not cheio else '#008675', markerfacecolor='white' if not cheio else '#008675',
                        label=f'{chave} · {_dia(s)}')
    ax.axhline(1, color='gray', ls='--', lw=1)
    ax.set(xticks=range(len(itens)), xticklabels=rot, ylabel='Indicador (ideal = 1)', ylim=(0.76, 1.07))
    ax.grid(axis='y', alpha=0.2)
    _legenda(fig, ax, 6)
    fig.tight_layout(rect=(0, 0.1, 1, 1))
    _salvar(fig, caminho)
