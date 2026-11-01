"""Repete a calibração e o GHZ de cinco qubits, preservando IDs e dados.

Exemplos (a partir da raiz do repositório):
  python quantum-mitigation/experimentos/04_mitigacao_leitura/repetir_mitigacao.py --verificar
  python quantum-mitigation/experimentos/04_mitigacao_leitura/repetir_mitigacao.py --rodada 3 --enviar
  python quantum-mitigation/experimentos/04_mitigacao_leitura/repetir_mitigacao.py --rodada 3 --coletar
Nenhum job é enviado sem --enviar. Uma rodada já registrada não é reenviada.
"""
import argparse
import importlib.metadata
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
from qiskit import QuantumCircuit, qpy, transpile
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2

BASE = Path(__file__).resolve().parents[2]
PASTA = BASE / 'dados/brutos/04_mitigacao_leitura/repeticoes'
QUBITS = [0, 1, 2, 3, 4]
SHOTS = 1000


def circuitos(rodada):
    pares = []
    for estado in range(32):
        qc = QuantumCircuit(5, 5)
        for q in range(5):
            if estado >> q & 1:
                qc.x(q)
        qc.measure(range(5), range(5))
        pares.append((f'cal_{estado:05b}', qc))
    for base in ['Z', 'X']:
        qc = QuantumCircuit(5, 5)
        qc.h(2)
        for controle, alvo in [(2, 1), (2, 3), (1, 0), (3, 4)]:
            qc.cx(controle, alvo)
        qc.barrier()
        if base == 'X':
            qc.h(range(5))
        qc.measure(range(5), range(5))
        pares.append((f'GHZ_{base}', qc))
    ordem = np.random.default_rng(42 + rodada).permutation(len(pares))
    return [pares[i] for i in ordem]


def salvar(caminho, dados):
    temporario = caminho.with_suffix('.tmp')
    temporario.write_text(json.dumps(dados, ensure_ascii=False, indent=2), encoding='utf-8')
    temporario.replace(caminho)


def analisar(contagens, seed):
    def vetor(nome):
        v = np.zeros(32)
        for bits, qtd in contagens[nome].items():
            v[int(bits, 2)] = qtd
        if v.sum() != SHOTS:
            raise ValueError(f'Total inesperado em {nome}')
        return v

    cal = np.column_stack([vetor(f'cal_{i:05b}') for i in range(32)])
    obs = np.column_stack([vetor('GHZ_Z'), vetor('GHZ_X')])
    a = cal / SHOTS
    cond = float(np.linalg.cond(a))
    if not np.isfinite(cond) or cond > 100:
        raise ValueError('Calibração instável; dados brutos preservados')
    bruto = obs / SHOTS
    quasi = np.linalg.solve(a, bruto)
    pesos = np.array([(-1) ** i.bit_count() for i in range(32)])

    def metricas(p):
        return np.array([p[0, 0] + p[-1, 0], pesos @ p[:, 1]])

    rng = np.random.default_rng(seed)
    amostras_brutas, amostras_ajustadas = [], []
    for _ in range(300):
        ac = np.column_stack([rng.multinomial(SHOTS, a[:, i]) for i in range(32)]) / SHOTS
        ob = np.column_stack([rng.multinomial(SHOTS, bruto[:, i]) for i in range(2)]) / SHOTS
        amostras_brutas.append(metricas(ob))
        amostras_ajustadas.append(metricas(np.linalg.solve(ac, ob)))
    return dict(ordem_metricas=['populacao_z', 'correlacao_x'],
                bruto=metricas(bruto).tolist(), ajustado=metricas(quasi).tolist(),
                erro_padrao_bruto=np.std(amostras_brutas, axis=0, ddof=1).tolist(),
                erro_padrao_ajustado=np.std(amostras_ajustadas, axis=0, ddof=1).tolist(),
                bootstrap_repeticoes=300, condicionamento=cond,
                menor_quasi_z=float(quasi[:, 0].min()), menor_quasi_x=float(quasi[:, 1].min()))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rodada', type=int, default=3)
    parser.add_argument('--backend', default='ibm_fez')
    acao = parser.add_mutually_exclusive_group(required=True)
    acao.add_argument('--verificar', action='store_true', help='Verifica estado ideal localmente, sem IBM')
    acao.add_argument('--enviar', action='store_true')
    acao.add_argument('--coletar', action='store_true')
    args = parser.parse_args()
    if args.rodada < 3:
        parser.error('As rodadas 1 e 2 são as históricas; escolha 3 ou maior')
    pares = circuitos(args.rodada)
    if args.verificar:
        from qiskit.quantum_info import Statevector
        for nome, circuito in pares:
            probs = Statevector.from_instruction(circuito.remove_final_measurements(inplace=False)).probabilities()
            if nome.startswith('cal_'):
                assert np.isclose(probs[int(nome[4:], 2)], 1)
            elif nome == 'GHZ_Z':
                assert np.isclose(probs[0], 0.5) and np.isclose(probs[-1], 0.5)
            else:
                assert np.isclose(sum(p for i, p in enumerate(probs) if i.bit_count() % 2), 0)
        print('34 circuitos conferidos: calibração, população Z ideal e paridade X ideal.')
        return

    PASTA.mkdir(parents=True, exist_ok=True)
    registro = PASTA / f'rodada_{args.rodada:02d}.json'
    if args.enviar and registro.exists():
        raise RuntimeError('Rodada já registrada. Use --coletar para evitar duplicação.')
    if args.coletar and not registro.exists():
        raise RuntimeError('Rodada não registrada; nenhum job será enviado.')
    service = QiskitRuntimeService(channel='ibm_quantum_platform')
    if args.enviar:
        backend = service.backend(args.backend)
        status = backend.status()
        if not status.operational or status.status_msg.lower() != 'active':
            raise RuntimeError('Backend indisponível; nenhum job enviado.')
        nomes, compilados, metadados = [], [], {}
        for nome, circuito in pares:
            qc = transpile(circuito, backend=backend, initial_layout=QUBITS,
                           routing_method='none', optimization_level=1, seed_transpiler=42)
            if qc.layout.final_index_layout(filter_ancillas=True) != QUBITS:
                raise RuntimeError('Mapeamento alterado; nenhum job enviado.')
            nomes.append(nome)
            compilados.append(qc)
            metadados[nome] = dict(profundidade=qc.depth(), operacoes=dict(qc.count_ops()))
        # QPY registra os circuitos realmente enviados, antes da submissão.
        with (PASTA / f'rodada_{args.rodada:02d}.qpy').open('wb') as arquivo:
            qpy.dump(compilados, arquivo)
        sampler = SamplerV2(mode=backend)
        sampler.options.dynamical_decoupling.enable = False
        sampler.options.twirling.enable_gates = False
        sampler.options.twirling.enable_measure = False
        sampler.options.execution.init_qubits = True
        sampler.options.max_execution_time = 120
        job = sampler.run(compilados, shots=SHOTS)
        dados = dict(rodada=args.rodada, backend=backend.name, qubits=QUBITS,
                     shots_por_circuito=SHOTS, job_id=job.job_id(), ordem_circuitos=nomes,
                     enviado_utc=datetime.now(timezone.utc).isoformat(),
                     versoes={p: importlib.metadata.version(p) for p in ['qiskit', 'qiskit-ibm-runtime', 'numpy']},
                     circuitos=metadados, seed_ordem=42+args.rodada, seed_transpiler=42,
                     opcoes=dict(dd=False, twirling_gates=False, twirling_measure=False,
                                 init_qubits=True, max_execution_time=120))
        salvar(registro, dados)
        print(f'Job enviado e registrado: {job.job_id()}', flush=True)
        print('Use --coletar para consultar e salvar as contagens; não será reenviado.')
    else:
        dados = json.loads(registro.read_text(encoding='utf-8'))
        job = service.job(dados['job_id'])
        status = str(job.status())
        print(f"Job {dados['job_id']}: {status}", flush=True)
        if status.upper() != 'DONE':
            return
        resultados = job.result()
        if len(resultados) != len(dados['ordem_circuitos']):
            raise RuntimeError('Quantidade inesperada de resultados')
        dados['contagens'] = {nome: resultados[i].data.c.get_counts()
                             for i, nome in enumerate(dados['ordem_circuitos'])}
        dados['coletado_utc'] = datetime.now(timezone.utc).isoformat()
        salvar(registro, dados)
        dados['analise'] = analisar(dados['contagens'], 2000 + args.rodada)
        salvar(registro, dados)
        print(json.dumps(dados['analise'], indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
