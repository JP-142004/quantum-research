"""Executa e registra simulações locais; não contém submissão a hardware."""
import argparse
import hashlib
import importlib.metadata
import json
import platform
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
from qiskit import qpy
from qiskit_aer import AerSimulator

from protocolo_local import (N, ARESTAS, BASIS, E01, E10, circuitos, compilar,
    validar_circuitos, ruido, referencia_exata, analisar, pesos, medidas, corrigir,
    intercepto)


def salvar(caminho, dados):
    caminho.write_text(json.dumps(dados, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')


def conferir_referencia(compilados, referencias, cenario):
    a = np.column_stack([referencias[f'cal_{i:05b}']['observado'] for i in range(32)])
    max_erro = 0
    for nome, qc in compilados.items():
        if nome.startswith('cal_'):
            if medidas(qc) != [(i, i) for i in range(N)]:
                raise ValueError('Layout de calibração inesperado')
            continue
        perm = np.array([sum(((estado >> q) & 1) << c for q, c in medidas(qc)) for estado in range(32)])
        inv = np.argsort(perm)
        q = corrigir(a[np.ix_(inv, inv)], np.array(referencias[nome]['observado']))
        erro = float(np.max(np.abs(q - referencias[nome]['antes_leitura'])))
        max_erro = max(max_erro, erro)
    if max_erro > 1e-12:
        raise ValueError(f'Inversão não recupera a referência exata: {cenario}')
    return max_erro


def relatorio(manifesto, registros):
    texto = f'''# Validação local do protocolo de cinco qubits

**Execução:** `{manifesto['execucao']}`. **Origem:** simulação clássica local em CPU, não hardware IBM.

Foram executados três blocos de 40 circuitos em cada um dos três cenários (ideal, leitura, leitura + portas) e três blocos de 42 circuitos para o piloto local de ZNE. Cada circuito recebeu {manifesto['shots']} shots simulados. Total: {manifesto['shots_simulados']:,} shots simulados, separados das 102.000 medidas reais históricas.

## Modelo e verificações

O mapa sintético de cinco qubits contém as arestas {ARESTAS}, em ambos os sentidos. Não é um snapshot atual do Fez. A base de portas é {BASIS}; compilação nível 1, semente 42. O GHZ original permite roteamento e o conectado usa as quatro arestas diretamente. A calibração é permutada conforme o mapa físico → clássico de cada circuito antes da inversão.

O canal de leitura é independente por qubit: P(1|0) = {E01} e P(0|1) = {E10}, na ordem física 0–4. O terceiro cenário acrescenta o canal despolarizante do Aer com parâmetro 0,02 após cada CX; esse parâmetro não é uma taxa de infidelidade de porta medida. Portas de um qubit são perfeitas no modelo. Não foram importadas calibrações reais da IBM ou modelados T1/T2, deriva e crosstalk.

Todas as distribuições ideais foram verificadas antes e depois da compilação, incluindo os controles e o dobramento ZNE. Os controles usam amostras independentes da calibração. O controle negativo tem |−〉 no qubit 0 (bit à direita). A inversão exata recupera as distribuições anteriores à leitura, inclusive após roteamento, com erro máximo inferior a 10⁻¹². O resíduo de ruído de portas permanece após essa recuperação.

As contagens foram produzidas pelo Aer em CPU com matriz densidade. A referência sem shots usa evolução por matriz densidade para as portas e aplicação analítica do canal de leitura. O bootstrap usa {manifesto['bootstrap']} réplicas por bloco, uma matriz de calibração compartilhada pelos circuitos e reamostragens GHZ independentes. Sementes, versões, contagens, QPY, mapas finais e hashes estão nos registros. Os valores ± abaixo são um erro padrão.

## Comparação original versus conectado

Valores ajustados; as estimativas brutas e os intervalos percentis de 95% estão em cada arquivo `*_analise.json`. A diferença usa bootstrap compartilhando a calibração.

| Cenário | Bloco | PZ original | PZ conectado | Diferença PZ | CX original | CX conectado | Diferença CX |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
'''
    def f(m):
        return f"{m['valor']:.4f} ± {m['erro_padrao']:.4f}"
    for item in registros:
        if item['protocolo'] != 'comparacao':
            continue
        a = item['analise']
        valores = []
        for base in ('Z', 'X'):
            valores += [f(a['circuitos'][f'{tipo}_{base}']['ajustado']) for tipo in ('original', 'conectado')]
            valores.append(f(a['contrastes'][base]['ajustado']))
        texto += f"| {item['cenario']} | {item['bloco']} | " + ' | '.join(valores) + ' |\n'
    texto += '\n## Controles independentes\n\nValores ajustados. Os alvos são 1 para os três primeiros controles e −1 para o último. Desvios em amostras finitas são registrados, sem selecionar apenas blocos favoráveis.\n\n| Cenário/protocolo | Bloco | 00000 em Z | 11111 em Z | +++++ em X | ++++− em X |\n| --- | ---: | ---: | ---: | ---: | ---: |\n'
    for item in registros:
        nomes = ['controle_zeros_Z', 'controle_uns_Z', 'controle_mais_X', 'controle_menos_X']
        vals = [f(item['analise']['circuitos'][nome]['ajustado']) for nome in nomes]
        texto += f"| {item['cenario']}/{item['protocolo']} | {item['bloco']} | " + ' | '.join(vals) + ' |\n'
    texto += '\n## Referências exatas do modelo\n\nSem erro de shots. Estes valores permitem separar o ruído de portas do ruído de leitura dentro do modelo escolhido.\n\n| Cenário | Construção | PZ antes da leitura | PZ observado | CX antes da leitura | CX observado |\n| --- | --- | ---: | ---: | ---: | ---: |\n'
    for cenario, ref in manifesto['referencias']['comparacao'].items():
        for tipo in ('original', 'conectado'):
            valores = [float(pesos(f'{tipo}_{base}') @ np.array(ref[f'{tipo}_{base}'][chave]))
                       for base in ('Z', 'X') for chave in ('antes_leitura', 'observado')]
            texto += f'| {cenario} | {tipo} | ' + ' | '.join(f'{v:.6f}' for v in valores) + ' |\n'
    texto += '''
## Piloto local de ZNE

Usamos dobramento global U(U†U)^k na preparação conectada, fatores 1, 3 e 5. Barreiras preservam os blocos durante a compilação; foram conferidas 4, 12 e 20 CX, respectivamente. As rotações finais de X e a leitura não são dobradas. O ajuste principal é uma reta por mínimos quadrados ordinários em função do fator nominal, extrapolada a zero, após mitigação de leitura. O bootstrap propaga a calibração compartilhada e as contagens de todos os fatores. Valores fora do intervalo físico não são recortados.

| Bloco | Base | Leitura ajustada, fator 1 | ZNE linear | ZNE − fator 1 |
| --- | --- | ---: | ---: | ---: |
'''
    for item in registros:
        if item['protocolo'] == 'zne':
            a = item['analise']
            for base in ('Z', 'X'):
                texto += f"| {item['bloco']} | {base} | {f(a['circuitos'][f'zne_1_{base}']['ajustado'])} | {f(a['contrastes'][base]['zne'])} | {f(a['contrastes'][base]['zne_menos_fator1'])} |\n"
    texto += '\nA sensibilidade à faixa de fatores pode ser examinada sem shots no modelo:\n\n| Base | Fator 1 | Fator 3 | Fator 5 | Intercepto linear 1,3,5 | Intercepto linear 1,3 |\n| --- | ---: | ---: | ---: | ---: | ---: |\n'
    ref = manifesto['referencias']['zne']['leitura_e_portas']
    for base in ('Z', 'X'):
        vals = np.array([pesos(f'zne_{k}_{base}') @ np.array(ref[f'zne_{k}_{base}']['antes_leitura']) for k in (1, 3, 5)])
        texto += f'| {base} | ' + ' | '.join(f'{v:.6f}' for v in [*vals, intercepto(vals), 1.5*vals[0]-.5*vals[1]]) + ' |\n'
    texto += f'''
## Conclusão e próximo passo

A validação verifica a lógica do protocolo e o tratamento do roteamento em um modelo controlado. A leitura pode ser invertida, mas o ruído das portas permanece; ZNE é uma extrapolação com viés de modelo e custo de variância, não garantia de recuperação exata. Resultados com mais de 1 ou abaixo de −1 são possíveis para os estimadores não restringidos.

Os três blocos de cada cenário mudam a semente de amostragem, não o equipamento ou o modelo: não representam deriva temporal real. O mapa, portas e ruídos sintéticos não permitem prever numericamente o próximo resultado no Fez. O próximo passo experimental continua sendo discutir os controles e preparar uma compilação específica para um backend disponível; nenhuma submissão é feita por estes scripts.

## Reprodução

```powershell
python -m venv .venv-simulacao
.venv-simulacao/Scripts/python -m pip install -r quantum-mitigation/requirements-simulacao.txt
.venv-simulacao/Scripts/python -m unittest discover -s quantum-mitigation/tests -v
.venv-simulacao/Scripts/python quantum-mitigation/scripts/validar_protocolo_local.py --execucao minha_validacao
```

O comando recusa reutilizar uma pasta existente. Para uma repetição, escolher outro nome. Os parâmetros padrão são três blocos, 1.000 shots e 2.000 réplicas bootstrap. A execução registrada levou {manifesto['tempo_segundos']:.1f} segundos para simulação e análise neste PC; não é uma previsão de tempo de QPU. O teste usa no máximo quatro threads de CPU, não utiliza a GPU nem lê credenciais.

Referências de implementação: [AerSimulator](https://qiskit.github.io/qiskit-aer/stubs/qiskit_aer.AerSimulator.html), [ReadoutError](https://qiskit.github.io/qiskit-aer/stubs/qiskit_aer.noise.ReadoutError.html), [canal despolarizante](https://qiskit.github.io/qiskit-aer/stubs/qiskit_aer.noise.depolarizing_error.html). As versões efetivamente usadas estão no manifesto; a documentação online pode descrever versão posterior.
'''
    return texto


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--execucao', required=True)
    args = parser.parse_args()
    if not args.execucao or any(c not in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-' for c in args.execucao):
        parser.error('Use apenas letras ASCII, números, hífen e underscore')
    base = Path(__file__).resolve().parents[1]
    pasta = base / 'dados/simulados' / args.execucao
    pasta.mkdir(parents=True, exist_ok=False)
    inicio = time.perf_counter()
    manifesto = dict(execucao=args.execucao, origem='simulacao_local_CPU', estado='iniciada',
        inicio_utc=datetime.now(timezone.utc).isoformat(), shots=1000, bootstrap=2000,
        blocos=3, shots_simulados=0, seed_transpiler=42, max_parallel_threads=4,
        versoes={p: importlib.metadata.version(p) for p in ['numpy', 'qiskit', 'qiskit-aer']},
        python=platform.python_version(), sistema=platform.system(),
        parametros=dict(arestas=ARESTAS, base=BASIS, e01=E01, e10=E10, depolarizante_cx=.02),
        referencias={}, circuitos={}, arquivos={}, fontes={})
    for nome in ['protocolo_local.py', 'validar_protocolo_local.py']:
        manifesto['fontes'][nome] = hashlib.sha256((base / 'scripts' / nome).read_bytes()).hexdigest()
    salvar(pasta / 'manifesto.json', manifesto)
    registros = []
    for protocolo in ('comparacao', 'zne'):
        logicos = circuitos(zne=protocolo == 'zne')
        compilados = compilar(logicos)
        validar_circuitos(logicos, compilados)
        with (pasta / f'{protocolo}.qpy').open('wb') as arquivo:
            qpy.dump(list(compilados.values()), arquivo)
        manifesto['circuitos'][protocolo] = {
            nome: dict(profundidade=qc.depth(), operacoes=dict(qc.count_ops()),
                       mapa_medidas=medidas(qc), layout_final=qc.layout.final_index_layout(),
                       duracao_compilada=None, motivo_duracao='Mapa sintético sem durações de portas')
            for nome, qc in compilados.items()}
        manifesto['referencias'][protocolo] = {}
        cenarios = ('ideal', 'leitura', 'leitura_e_portas') if protocolo == 'comparacao' else ('leitura_e_portas',)
        for cenario_idx, cenario in enumerate(cenarios):
            refs = referencia_exata(compilados, cenario)
            conferir_referencia(compilados, refs, cenario)
            manifesto['referencias'][protocolo][cenario] = refs
            for bloco in range(1, 4):
                seed = 20261101 + 1000*(protocolo == 'zne') + 100*cenario_idx + bloco
                nomes = list(compilados)
                ordem = np.random.default_rng(seed).permutation(len(nomes))
                ordenados = [nomes[i] for i in ordem]
                sim = AerSimulator(method='density_matrix', device='CPU', noise_model=ruido(cenario),
                    max_parallel_threads=4, max_parallel_experiments=1)
                resultado = sim.run([compilados[n] for n in ordenados], shots=1000, seed_simulator=seed).result()
                if not resultado.success:
                    raise RuntimeError('Simulador não concluiu')
                counts = {nome: resultado.get_counts(i) for i, nome in enumerate(ordenados)}
                prefixo = f'{protocolo}_{cenario}_bloco_{bloco:02d}'
                bruto = dict(origem='simulacao_local', protocolo=protocolo, cenario=cenario, bloco=bloco,
                    seed_simulator=seed, seed_ordem=seed, seed_bootstrap=seed+10000, shots=1000,
                    ordem_circuitos=ordenados, contagens=counts)
                salvar(pasta / f'{prefixo}_contagens.json', bruto)
                analise = analisar(counts, 1000, 2000, seed+10000, compilados)
                salvar(pasta / f'{prefixo}_analise.json', analise)
                registros.append(dict(protocolo=protocolo, cenario=cenario, bloco=bloco, analise=analise))
                manifesto['shots_simulados'] += 1000*len(compilados)
                print(f'{prefixo}: {len(compilados)} circuitos simulados e analisados.', flush=True)
    manifesto.update(estado='concluida', fim_utc=datetime.now(timezone.utc).isoformat(),
                     tempo_segundos=time.perf_counter()-inicio)
    for caminho in sorted(pasta.iterdir()):
        if caminho.name != 'manifesto.json':
            manifesto['arquivos'][caminho.name] = hashlib.sha256(caminho.read_bytes()).hexdigest()
    salvar(pasta / 'manifesto.json', manifesto)
    texto = relatorio(manifesto, registros)
    (pasta / 'relatorio.md').write_text(texto, encoding='utf-8')
    print(f'Concluído em {manifesto["tempo_segundos"]:.1f}s. Relatório: {pasta / "relatorio.md"}')


if __name__ == '__main__':
    main()
