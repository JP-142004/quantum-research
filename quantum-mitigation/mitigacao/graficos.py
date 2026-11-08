"""Figuras dos resultados da análise (matplotlib, sem janela)."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

from mitigacao.tecnicas import zne  # noqa: E402

plt.rcParams.update({'font.size': 10, 'axes.spines.top': False, 'axes.spines.right': False})
COR = {'original': '#526b91', 'conectado': '#008675'}


def _salvar(fig, caminho):
    fig.savefig(caminho, dpi=170, bbox_inches='tight')
    plt.close(fig)


def comparacao(res, cenario, caminho):
    """Original e conectado, bruto (vazado) e ajustado (cheio), por bloco, com a referência exata."""
    blocos = [r for r in res.values() if r['validacao']['cenario'] == cenario]
    fig, eixos = plt.subplots(1, 2, figsize=(10, 4.3), sharey=True)
    x = np.arange(1, len(blocos) + 1)
    for ax, indicador, base in zip(eixos, ('PZ', 'CX'), ('Z', 'X')):
        for variante, desloc in (('original', -0.09), ('conectado', 0.09)):
            itens = [next(d for d in r['itens'].values() if d['circuito'] == 'ghz' and d['variante'] == variante
                          and d['base'] == base and d['fator'] == 1) for r in blocos]
            for chave, marcador, extra in (('bruto', 's', -0.025), ('ajustado', 'o', 0.025)):
                ax.errorbar(x + desloc + extra, [d[chave]['valor'] for d in itens], yerr=[d[chave]['ep'] for d in itens],
                            fmt=marcador, color=COR[variante], capsize=3, markerfacecolor='white' if chave == 'bruto' else COR[variante],
                            label=f'{variante} · {chave}')
            ax.axhline(itens[0]['referencia']['antes_leitura'], color=COR[variante], ls=':', lw=1)
        ax.axhline(1, color='gray', ls='--', lw=1)
        ax.set(xticks=x, xlabel='Bloco', title=indicador, ylim=(0.4, 1.12))
        ax.grid(axis='y', alpha=0.2)
    eixos[0].set_ylabel('Indicador (ideal = 1)')
    fig.suptitle(f'Simulação · cenário {cenario.replace("_", " ")}', fontweight='bold')
    h, l = eixos[0].get_legend_handles_labels()
    fig.legend(h, l, loc='lower center', ncol=4, fontsize=8)
    fig.tight_layout(rect=(0, 0.1, 1, 0.94))
    _salvar(fig, caminho)


def zne_blocos(res, caminho):
    """Ajustado nos fatores 1, 3 e 5 e extrapolado a zero, por bloco; X marca a extrapolação exata."""
    fig, eixos = plt.subplots(1, 2, figsize=(10, 4.5), sharey=True)
    blocos = [r for r in res.values() if r['zne']]
    x = np.arange(1, len(blocos) + 1)
    for ax, base in zip(eixos, ('Z', 'X')):
        grupos = [next(g for g in r['zne'] if g['base'] == base) for r in blocos]
        for i, f in enumerate(zne.FATORES):
            ep = [r['itens'][g['nomes'][i]]['ajustado']['ep'] for r, g in zip(blocos, grupos)]
            ax.errorbar(x + (i - 1.5) * 0.12, [g['ajustado_por_fator'][i] for g in grupos], yerr=ep, fmt='o', capsize=3,
                        label=f'fator {f}')
        ax.errorbar(x + 0.3, [g['zne']['valor'] for g in grupos], yerr=[g['zne']['ep'] for g in grupos], fmt='D',
                    color='#9b4f96', capsize=3, label='extrapolado')
        ax.plot(x + 0.3, [g['referencia']['zne'] for g in grupos], 'x', color='black', label='extrapolação exata')
        ax.axhline(1, color='gray', ls='--', lw=1)
        ax.set(xticks=x, xlabel='Bloco', title=grupos[0]['indicador'], ylim=(0.5, 1.2))
        ax.grid(axis='y', alpha=0.2)
    eixos[0].set_ylabel('Indicador ajustado (ideal = 1)')
    h, l = eixos[0].get_legend_handles_labels()
    fig.legend(h, l, loc='lower center', ncol=5, fontsize=8)
    fig.tight_layout(rect=(0, 0.1, 1, 1))
    _salvar(fig, caminho)


def zne_fatores(res, caminho):
    """Valores exatos do modelo nos fatores de ruído e a reta lida no fator 0."""
    r = next(r for r in res.values() if r['zne'])
    fig, ax = plt.subplots(figsize=(6, 4.3))
    for g, cor in zip(sorted(r['zne'], key=lambda g: g['base']), ('#526b91', '#008675')):
        ref = g['referencia']
        pesos = zne.pesos_intercepto()
        x = np.array(zne.FATORES, float)
        inclinacao = np.sum((x - x.mean()) * np.array(ref['antes_leitura_por_fator'])) / np.sum((x - x.mean()) ** 2)
        ax.plot([0, 5], [ref['zne'], ref['zne'] + 5 * inclinacao], color=cor, lw=1, ls=':')
        ax.plot(zne.FATORES, ref['antes_leitura_por_fator'], 'o', color=cor, label=g['indicador'])
        ax.plot([0], [ref['zne']], 'D', color=cor)
        assert abs(float(pesos @ ref['antes_leitura_por_fator']) - ref['zne']) < 1e-12
    ax.axhline(1, color='gray', ls='--', lw=1)
    ax.set(xlabel='Fator de ruído (0 = extrapolado)', ylabel='Indicador exato do modelo', xticks=[0, 1, 3, 5])
    ax.legend()
    ax.grid(alpha=0.2)
    _salvar(fig, caminho)
