"""Gera figuras de leitura dos dados salvos. Não consulta serviços externos."""
from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

BASE = Path(__file__).resolve().parents[1] / 'dados'
IMAGENS = BASE / 'imagens'
IMAGENS.mkdir(exist_ok=True)
plt.rcParams.update({'font.size': 10, 'axes.spines.top': False, 'axes.spines.right': False})


def ler(caminho):
    return json.loads(caminho.read_text(encoding='utf-8-sig'))


def salvar(figura, nome):
    figura.savefig(IMAGENS / nome, dpi=170, bbox_inches='tight')
    plt.close(figura)


controles = ler(BASE / 'processados/02_controles/resultados_recuperados.json')
fig, ax = plt.subplots(figsize=(10, 6), layout='constrained')
nomes = [f"{r['backend'].removeprefix('ibm_')} · {r['experimento']} · {r['circuito']}".replace('_', ' ') for r in controles]
valores = [r['acertos'] / 10 for r in controles]
barras = ax.barh(nomes, valores, color='#287d8e')
ax.bar_label(barras, labels=[f'{v:.1f}%' for v in valores], padding=4)
ax.invert_yaxis()
ax.set(xlim=(0, 112), xlabel='Medidas iguais ao estado preparado (%) · 1.000 por circuito',
       title='Controles reais · cada linha é um circuito recuperado da IBM')
ax.grid(axis='x', alpha=.2)
salvar(fig, 'controles_reais.png')

ghz = ler(BASE / 'processados/03_ghz_conectado/resultados_recuperados.json')
fig, eixos = plt.subplots(1, 2, figsize=(11, 4), layout='constrained')
for ax, base in zip(eixos, ['Z', 'X']):
    dados = [r for r in ghz if r['circuito'].endswith('_' + base)]
    nomes = [r['experimento'].replace('_', ' ') + '\n' + r['circuito'] for r in dados]
    valores = [r['indicador'] for r in dados]
    barras = ax.barh(nomes, valores, color='#287d8e')
    ax.bar_label(barras, fmt='%.3f', padding=4, bbox=dict(facecolor='white', edgecolor='none', pad=0))
    ax.axvline(1, color='gray', linestyle='--')
    ax.invert_yaxis()
    ax.set(xlim=(0, 1.12), title='População em Z' if base == 'Z' else 'Correlação em X', xlabel='Indicador bruto')
fig.suptitle('GHZ no Fez · dados históricos recuperados', fontweight='bold')
salvar(fig, 'construcoes_reais.png')

execucao = BASE / 'simulados/validacao_2026_11_01'
cenarios = [('ideal', 'Ideal'), ('leitura', 'Erro de leitura'), ('leitura_e_portas', 'Leitura e portas')]
for cenario, titulo in cenarios:
    fig, eixos = plt.subplots(1, 2, figsize=(10, 4.3), sharey=True)
    for ax, base in zip(eixos, ['Z', 'X']):
        for tipo, cor, deslocamento in [('original', '#526b91', -.09), ('conectado', '#008675', .09)]:
            dados = [ler(execucao / f'comparacao_{cenario}_bloco_{bloco:02d}_analise.json')['circuitos'][f'{tipo}_{base}'] for bloco in range(1, 4)]
            for chave, marcador, adicional in [('bruto', 's', -.025), ('ajustado', 'o', .025)]:
                ax.errorbar(np.arange(1, 4) + deslocamento + adicional,
                    [d[chave]['valor'] for d in dados], yerr=[d[chave]['erro_padrao'] for d in dados],
                    fmt=marcador, color=cor, markerfacecolor='white' if chave == 'bruto' else cor,
                    capsize=3, label=f'{tipo} · {chave}')
        ax.axhline(1, color='gray', linestyle='--', linewidth=1)
        ax.set(xticks=[1, 2, 3], xlabel='Bloco simulado', title='População Z' if base == 'Z' else 'Correlação X', ylim=(0, 1.17))
        ax.grid(axis='y', alpha=.2)
    eixos[0].set_ylabel('Indicador · ideal = 1')
    fig.suptitle(f'Comparação local · {titulo}', fontweight='bold')
    handles, labels = eixos[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc='lower center', ncol=2, fontsize=9)
    fig.tight_layout(rect=(0, .17, 1, .93))
    salvar(fig, f'simulacao_{cenario}.png')

fig, eixos = plt.subplots(1, 2, figsize=(10, 4.5), sharey=True)
for ax, base in zip(eixos, ['Z', 'X']):
    for fator, cor, deslocamento in [(1, '#526b91', -.18), (3, '#008675', -.06), (5, '#ae6a36', .06), (0, '#9b4f96', .18)]:
        dados = [ler(execucao / f'zne_leitura_e_portas_bloco_{bloco:02d}_analise.json') for bloco in range(1, 4)]
        metricas = [d['contrastes'][base]['zne'] if fator == 0 else d['circuitos'][f'zne_{fator}_{base}']['ajustado'] for d in dados]
        ax.errorbar(np.arange(1, 4) + deslocamento, [m['valor'] for m in metricas],
            yerr=[m['erro_padrao'] for m in metricas], fmt='D' if fator == 0 else 'o',
            capsize=3, color=cor, label='Extrapolação' if fator == 0 else f'Fator {fator}')
    ax.axhline(1, color='gray', linestyle='--', linewidth=1)
    ax.set(xticks=[1, 2, 3], xlabel='Bloco simulado', title='População Z' if base == 'Z' else 'Correlação X', ylim=(0, 1.2))
    ax.grid(axis='y', alpha=.2)
fig.suptitle('ZNE local · fatores após ajuste de leitura e extrapolação', fontweight='bold')
handles, labels = eixos[0].get_legend_handles_labels()
fig.legend(handles, labels, loc='lower center', ncol=4)
fig.tight_layout(rect=(0, .12, 1, .93))
salvar(fig, 'zne_blocos.png')

arquivos = sorted(execucao.glob('*_analise.json'))
nomes_controles = ['controle_zeros_Z', 'controle_uns_Z', 'controle_mais_X', 'controle_menos_X']
fig, ax = plt.subplots(figsize=(10, 7), layout='constrained')
desvios = np.array([[ler(f)['circuitos'][nome]['ajustado']['valor'] - alvo
    for nome, alvo in zip(nomes_controles, [1, 1, 1, -1])] for f in arquivos])
imagem = ax.imshow(desvios, cmap='RdBu_r', vmin=-.1, vmax=.1, aspect='auto')
ax.set_xticks(range(4), ['Zeros Z', 'Uns Z', 'Paridade + X', 'Paridade − X'])
ax.set_yticks(range(len(arquivos)), [f.stem.replace('_analise', '').replace('comparacao_', '').replace('leitura_e_portas', 'portas+leitura').replace('_bloco_', ' · bloco ').replace('_', ' ') for f in arquivos])
for i in range(len(arquivos)):
    for j in range(4):
        ax.text(j, i, f'{desvios[i,j]:+.3f}', ha='center', va='center', fontsize=9)
fig.colorbar(imagem, ax=ax, label='Indicador ajustado − alvo ideal')
ax.set_title('Controles locais · desvio em relação ao alvo', fontweight='bold', pad=14)
salvar(fig, 'controles_simulados.png')
print('Sete figuras geradas a partir dos JSONs salvos.')
