"""Análise offline das três rodadas. Não importa Qiskit nem acessa a rede."""
import argparse
import hashlib
import json
import platform
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

FONTES = [
    'GHZ_leitura_dbccq67i0auc73dumdk0.json',
    'GHZ_leitura_dbccri9gv2cc73ea3630.json',
    'rodada_03/rodada_03.json',
]


def carregar(caminho):
    dados = json.loads(caminho.read_text(encoding='utf-8'))
    if dados['qubits'] != [0, 1, 2, 3, 4] or dados['backend'] != 'ibm_fez':
        raise ValueError('Configuração diferente da comparação planejada')
    nomes = [f'cal_{i:05b}' for i in range(32)] + ['GHZ_Z', 'GHZ_X']
    if set(dados['contagens']) != set(nomes):
        raise ValueError('Conjunto de circuitos inválido')
    if len(dados['ordem_circuitos']) != 34 or set(dados['ordem_circuitos']) != set(nomes):
        raise ValueError('Ordem de circuitos inválida')
    contagens = np.zeros((32, 34), dtype=int)
    for j, nome in enumerate(nomes):
        for bits, qtd in dados['contagens'][nome].items():
            if len(bits) != 5 or set(bits) - {'0', '1'} or type(qtd) is not int or qtd < 0:
                raise ValueError(f'Contagem inválida: {nome}')
            contagens[int(bits, 2), j] = qtd
    if dados['shots_por_circuito'] != 1000 or not np.all(contagens.sum(axis=0) == 1000):
        raise ValueError('Total de shots inesperado')
    return dados, contagens / 1000


def metricas(p):
    paridade = np.array([(-1) ** i.bit_count() for i in range(32)])
    return np.array([p[0, 0] + p[-1, 0], paridade @ p[:, 1]])


def analisar(caminho, rodada, repeticoes):
    dados, probs = carregar(caminho)
    a, p = probs[:, :32], probs[:, 32:]
    cond = np.linalg.cond(a)
    if not np.isfinite(cond) or cond > 100:
        raise ValueError('Calibração instável')
    q = np.linalg.solve(a, p)
    if not np.allclose(q.sum(axis=0), 1) or not np.allclose(a @ q, p):
        raise ValueError('Falha na inversão')
    bruto, ajustado = metricas(p), metricas(q)
    if 'analise' in dados:
        for chave, valor in [('bruto', bruto), ('ajustado', ajustado)]:
            if not np.allclose(valor, dados['analise'][chave], atol=1e-12, rtol=0):
                raise ValueError('Resultado diverge da análise original salva')
    seed = 20261101 + rodada
    rng = np.random.default_rng(seed)
    b, m = np.empty((repeticoes, 2)), np.empty((repeticoes, 2))
    for i in range(repeticoes):
        ab = np.column_stack([rng.multinomial(1000, a[:, j]) for j in range(32)]) / 1000
        pb = np.column_stack([rng.multinomial(1000, p[:, j]) for j in range(2)]) / 1000
        if not np.isfinite(np.linalg.cond(ab)) or np.linalg.cond(ab) > 100:
            raise ValueError('Bootstrap instável; análise interrompida, sem descartar amostras')
        b[i], m[i] = metricas(pb), metricas(np.linalg.solve(ab, pb))
    # Controle independente: variâncias binomial e de paridade para os dados brutos.
    se_analitico = np.sqrt([bruto[0] * (1-bruto[0])/1000, (1-bruto[1]**2)/1000])
    if not np.allclose(b.std(axis=0, ddof=1), se_analitico, rtol=0.06):
        raise ValueError('Bootstrap bruto diverge do controle analítico')
    resultado = dict(rodada=rodada, job_id=dados['job_id'], backend=dados['backend'],
                     qubits=dados['qubits'], shots_por_circuito=1000, circuitos=34,
                     fonte=str(caminho.name), sha256=hashlib.sha256(caminho.read_bytes()).hexdigest(),
                     enviado_utc=dados.get('enviado_utc'), seed_bootstrap=seed,
                     condicionamento=float(cond), menor_quasi_z=float(q[:, 0].min()),
                     menor_quasi_x=float(q[:, 1].min()), metricas={})
    for j, nome in enumerate(['populacao_z', 'correlacao_x']):
        ganho = m[:, j] - b[:, j]
        resultado['metricas'][nome] = dict(
            bruto=float(bruto[j]), ajustado=float(ajustado[j]),
            se_bruto=float(b[:, j].std(ddof=1)), se_bruto_analitico=float(se_analitico[j]),
            se_ajustado=float(m[:, j].std(ddof=1)), ganho=float(ajustado[j]-bruto[j]),
            se_ganho=float(ganho.std(ddof=1)),
            ic95_ganho_percentil=np.quantile(ganho, [.025, .975]).tolist(),
            reducao_desvio_ideal=float(1-abs(1-ajustado[j])/abs(1-bruto[j])))
    return resultado


def graficos(resultados, pasta):
    plt.rcParams.update({'font.size': 11, 'axes.spines.top': False, 'axes.spines.right': False})
    x = np.arange(1, 4)
    fig, eixos = plt.subplots(1, 2, figsize=(11, 4.8), sharey=True)
    for ax, nome, titulo in zip(eixos, ['populacao_z', 'correlacao_x'], ['População em Z (PZ)', 'Correlação em X (CX)']):
        for chave, erro, deslocamento, cor, rotulo in [
            ('bruto', 'se_bruto', -.08, '#526b91', 'Bruto'),
            ('ajustado', 'se_ajustado', .08, '#008675', 'Ajustado')]:
            ax.errorbar(x+deslocamento, [r['metricas'][nome][chave] for r in resultados],
                        yerr=[r['metricas'][nome][erro] for r in resultados],
                        fmt='o', capsize=5, color=cor, label=rotulo)
        ax.axhline(1, color='#555555', ls='--', lw=1, label='Ideal')
        ax.set(title=titulo, xticks=x, xlabel='Rodada', ylim=(.74, 1.03))
        ax.grid(axis='y', alpha=.2)
    eixos[0].set_ylabel('Valor do indicador (adimensional)')
    eixos[1].legend(loc='center right')
    fig.suptitle('GHZ de 5 qubits · três execuções no ibm_fez', fontweight='bold')
    fig.text(.5, .025, 'Barras: ±1 erro padrão · bootstrap de calibração e GHZ · eixo vertical ampliado', ha='center', fontsize=10)
    fig.tight_layout(rect=(0, .06, 1, .94))
    for extensao in ['png', 'svg']:
        fig.savefig(pasta / f'04_comparacao_rodadas.{extensao}', dpi=180)
    plt.close(fig)
    fig, ax = plt.subplots(figsize=(9, 4.8))
    for nome, offset, cor, rotulo in [('populacao_z', -.08, '#526b91', 'Ganho em PZ'), ('correlacao_x', .08, '#008675', 'Ganho em CX')]:
        vals = np.array([r['metricas'][nome]['ganho'] for r in resultados])
        limites = np.array([r['metricas'][nome]['ic95_ganho_percentil'] for r in resultados])
        ax.errorbar(x+offset, vals, yerr=[vals-limites[:, 0], limites[:, 1]-vals],
                    fmt='o', capsize=5, color=cor, label=rotulo)
    ax.axhline(0, color='#555555', lw=1)
    ax.set(xticks=x, xlabel='Rodada', ylabel='Ajustado − bruto (adimensional)', ylim=(-.01, .21),
           title='Ganho do ajuste com incerteza pareada')
    ax.legend(loc='lower right')
    ax.grid(axis='y', alpha=.2)
    fig.text(.5, .025, 'Barras: intervalo percentil de 95% · mesmas contagens reamostradas para bruto e ajustado', ha='center', fontsize=9)
    fig.tight_layout(rect=(0, .06, 1, 1))
    for extensao in ['png', 'svg']:
        fig.savefig(pasta / f'04_ganho_rodadas.{extensao}', dpi=180)
    plt.close(fig)


def relatorio(resultados, repeticoes):
    texto = f'''# Comparação das três rodadas de mitigação

Análise local de 1 de novembro de 2026. Os dados brutos permanecem intactos.

## Resultado principal

O ajuste aumenta PZ e CX nas três execuções disponíveis. Isso constitui evidência de repetibilidade do efeito do estimador neste conjunto de cinco qubits; não mede fidelidade completa nem demonstra eliminação dos erros de portas. A aproximação ao valor ideal não valida, por si só, o modelo de calibração.

## Proveniência e método

Cada rodada contém 32 circuitos de calibração e dois GHZ, com 1.000 shots cada: 34.000 por rodada e 102.000 no conjunto. Backend registrado: ibm_fez; qubits físicos 0–4. A numeração 1–2 identifica os dois arquivos históricos, sem inferir datas ausentes. Somente a rodada 3 registra data, versões e circuitos compilados. A equivalência exata das compilações históricas não pode ser auditada apenas com os JSONs.

As colunas de A são as frequências de leitura de cada estado de calibração. Resolvemos A q = p, sem recortar quasiprobabilidades negativas. PZ = p(00000) + p(11111); CX é a soma das probabilidades pares menos as ímpares em X. CX não é uma porcentagem de acertos.

Usamos {repeticoes:,} reamostragens multinomiais por rodada, com calibração e GHZ reamostrados. Bruto e ajustado usam o mesmo GHZ em cada réplica, preservando a covariância na diferença. As sementes e os hashes SHA-256 estão no JSON processado. As barras principais e os valores ± são um erro padrão, não intervalos de 95%. Os intervalos do ganho são percentis 2,5% e 97,5%, por comparação, sem ajuste para comparações múltiplas.

Essa análise substitui apenas a comparação derivada; os 300 bootstraps originalmente salvos na rodada 3 não foram alterados. Diferenças nos erros padrão decorrem da nova semente e do maior número de réplicas. O bootstrap representa incerteza de amostragem sob o modelo multinomial e não incorpora deriva, erros sistemáticos de preparação ou inadequação do modelo.

## Indicadores por rodada

| Rodada | PZ bruto ± EP | PZ ajustado ± EP | CX bruto ± EP | CX ajustado ± EP |
| --- | ---: | ---: | ---: | ---: |
'''
    for r in resultados:
        z, x = r['metricas'].values()
        vals = [f"{m[k]:.4f} ± {m[e]:.4f}" for m in [z, x] for k, e in [('bruto', 'se_bruto'), ('ajustado', 'se_ajustado')]]
        texto += f"| {r['rodada']} | " + ' | '.join(vals) + ' |\n'
    texto += '\n![Indicadores e erros padrão](../figuras/04_comparacao_rodadas.png)\n\n## Ganho pareado\n\n| Rodada | Indicador | Ganho | IC percentil 95% | Redução do desvio ao ideal |\n| --- | --- | ---: | --- | ---: |\n'
    for r in resultados:
        for nome, m in r['metricas'].items():
            lo, hi = m['ic95_ganho_percentil']
            texto += f"| {r['rodada']} | {nome} | {m['ganho']:.4f} | [{lo:.4f}; {hi:.4f}] | {100*m['reducao_desvio_ideal']:.1f}% |\n"
    texto += '''
A redução é 1 − |1 − ajustado| / |1 − bruto|, uma comparação descritiva de distância ao ideal; não é a fração de erros físicos eliminados. Todos os intervalos individuais do ganho ficam acima de zero nesta análise. Eles quantificam o efeito do ajuste sob o modelo, não um efeito causal isolado da leitura.

![Ganhos e intervalos de 95%](../figuras/04_ganho_rodadas.png)

## Diagnósticos

| Rodada | Job | Condição de A (norma 2) | Menor quasi Z | Menor quasi X |
| --- | --- | ---: | ---: | ---: |
'''
    for r in resultados:
        texto += f"| {r['rodada']} | `{r['job_id']}` | {r['condicionamento']:.4f} | {r['menor_quasi_z']:.5f} | {r['menor_quasi_x']:.5f} |\n"
    texto += '''
As matrizes não apresentam mau condicionamento numérico relevante nestas amostras. As quasiprobabilidades negativas são mantidas para não mudar o estimador. A incerteza dos valores ajustados é maior que a dos valores brutos: há um custo estatístico na inversão e na calibração finita.

## Alcance da conclusão

O ganho tem o mesmo sinal nas três rodadas. A terceira apresenta os maiores valores pontuais ajustados, mas três execuções não sustentam uma tendência temporal, e as duas primeiras não têm datas registradas. Não agregamos as contagens de diferentes calibrações nem usamos um erro combinado que pressuponha hardware estável.

Preparar os estados de calibração exige operações físicas; portanto A pode absorver erros de preparação. As portas de preparação do GHZ, as rotações para medir X e a perda de coerência continuam relevantes. PZ e CX são dois observáveis, não uma tomografia ou uma medida completa da fidelidade. Os resultados históricos de roteamento sem contagens salvas ficam fora desta comparação quantitativa.

## Reprodução e verificações

Da raiz do repositório:

```powershell
python -m venv .venv-analise
.venv-analise/Scripts/python -m pip install -r quantum-mitigation/requirements-analise.txt
.venv-analise/Scripts/python quantum-mitigation/scripts/comparar_rodadas.py
```

O script só lê JSONs locais e grava tabelas Markdown, JSON e figuras PNG/SVG. Valida nomes, bitstrings, totais e configuração; verifica normalização e resíduo da inversão; compara a rodada 3 com os indicadores salvos; confronta o erro padrão bruto com as fórmulas binomial e de paridade. Interrompe se houver matriz bootstrap instável; não descarta réplicas silenciosamente.

## Referência metodológica

O modelo de canal clássico de leitura e sua matriz de atribuição estão descritos no [tutorial oficial da IBM sobre mitigação de leitura](https://quantum.cloud.ibm.com/docs/en/tutorials/readout-error-mitigation-sampler). Aqui usamos inversão completa de 32 × 32, não o algoritmo M3 do tutorial.
'''
    return texto


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--bootstrap', type=int, default=5000)
    args = parser.parse_args()
    if args.bootstrap < 5000:
        parser.error('Use pelo menos 5000 réplicas para a comparação final')
    base = args.base
    bruto = base / 'dados/brutos/04_mitigacao_leitura'
    resultados = [analisar(bruto / nome, i, args.bootstrap) for i, nome in enumerate(FONTES, 1)]
    if len({r['job_id'] for r in resultados}) != 3:
        raise ValueError('Jobs duplicados')
    for pasta in ['dados/processados/04_mitigacao_leitura', 'figuras', 'docs']:
        (base / pasta).mkdir(parents=True, exist_ok=True)
    saida = dict(bootstrap_repeticoes=args.bootstrap, versoes=dict(python=platform.python_version(), numpy=np.__version__, matplotlib=matplotlib.__version__), rodadas=resultados)
    (base / 'dados/processados/04_mitigacao_leitura/comparacao_rodadas.json').write_text(json.dumps(saida, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')
    (base / 'docs/comparacao_rodadas.md').write_text(relatorio(resultados, args.bootstrap), encoding='utf-8')
    graficos(resultados, base / 'figuras')
    print(json.dumps(saida, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
