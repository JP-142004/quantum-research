"""Simulador local (Qiskit Aer, matriz densidade, CPU). Não acessa a IBM."""
from qiskit import transpile
from qiskit.transpiler import CouplingMap
from qiskit_aer import AerSimulator

from mitigacao.execucao import conferir_sem_troca, embaralhar, info_compilado
from mitigacao.execucao.ruido import modelo_ruido
from mitigacao.topologia import vizinhos_linha

INSTANTANEO = True
BASE_PORTAS = ['rz', 'sx', 'x', 'cx']
SEMENTE_COMPILADOR = 42


def vizinhos(computador, n):
    """O computador sintético é uma linha de n qubits: 0-1-2-...-(n-1)."""
    return vizinhos_linha(n)


def _mapa_linha(n):
    """Mapa de ligações em linha, nos dois sentidos."""
    mapa = CouplingMap()
    for i in range(n):
        mapa.add_physical_qubit(i)
    for i in range(n - 1):
        mapa.add_edge(i, i + 1)
        mapa.add_edge(i + 1, i)
    return mapa


def compilar(montado):
    n = montado['item']['n']
    mapa = _mapa_linha(n)
    qc = transpile(montado['circuito'], basis_gates=BASE_PORTAS, coupling_map=mapa,
                   initial_layout=list(montado['qubits_fisicos']), routing_method=montado['roteamento'],
                   optimization_level=1, seed_transpiler=SEMENTE_COMPILADOR)
    if montado['roteamento'] == 'none':
        conferir_sem_troca(qc, montado['qubits_fisicos'], montado['nome'])
    return qc


def enviar(montados, shots, semente, computador='simulador', cenario='leitura_e_portas'):
    """Compila e simula tudo agora. `computador` só entra na ficha."""
    ordem = embaralhar([m['nome'] for m in montados], semente)
    por_nome = {m['nome']: m for m in montados}
    compilados = {nome: compilar(por_nome[nome]) for nome in ordem}
    n_max = max(m['item']['n'] for m in montados)
    sim = AerSimulator(method='density_matrix', device='CPU', noise_model=modelo_ruido(cenario, n_max),
                       max_parallel_threads=4, max_parallel_experiments=1)
    resultado = sim.run([compilados[nome] for nome in ordem], shots=shots, seed_simulator=semente).result()
    if not resultado.success:
        raise RuntimeError('O simulador não concluiu')
    contagens = {nome: resultado.get_counts(i) for i, nome in enumerate(ordem)}
    return dict(job_id=f'simulador-{semente}', ordem=ordem, compilados=compilados, contagens=contagens,
                opcoes=dict(cenario=cenario, metodo='density_matrix'),
                info={nome: info_compilado(qc) for nome, qc in compilados.items()})


def coletar(job):
    return job['contagens']
