"""Circuitos e análise de cinco qubits, exclusivamente locais; sem cliente IBM."""
import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit.transpiler import CouplingMap
from qiskit.quantum_info import Statevector
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, ReadoutError, depolarizing_error

N = 5
DIM = 2**N
ARESTAS = [(2, 1), (2, 3), (1, 0), (3, 4)]
BASIS = ['rz', 'sx', 'x', 'cx']
E01 = [0.01, 0.02, 0.03, 0.04, 0.05]
E10 = [0.06, 0.05, 0.04, 0.03, 0.02]
PARIDADE = np.array([(-1)**i.bit_count() for i in range(DIM)])


def preparacao(tipo):
    qc = QuantumCircuit(N)
    if tipo == 'original':
        qc.h(0)
        for alvo in range(1, N):
            qc.cx(0, alvo)
    elif tipo == 'conectado':
        qc.h(2)
        for controle, alvo in ARESTAS:
            qc.cx(controle, alvo)
    else:
        raise ValueError('Construção desconhecida')
    return qc


def ghz(tipo, base, fator=1):
    if fator not in (1, 3, 5) or base not in ('Z', 'X'):
        raise ValueError('Base ou fator inválido')
    qc = QuantumCircuit(N, N)
    u = preparacao(tipo)
    qc.compose(u, inplace=True)
    for _ in range((fator-1)//2):
        qc.barrier()
        qc.compose(u.inverse(), inplace=True)
        qc.barrier()
        qc.compose(u, inplace=True)
    qc.barrier()
    if base == 'X':
        qc.h(range(N))
    qc.measure(range(N), range(N))
    return qc


def circuitos(zne=False):
    saida = {}
    for estado in range(DIM):
        qc = QuantumCircuit(N, N)
        for bit in range(N):
            if estado >> bit & 1:
                qc.x(bit)
        qc.measure(range(N), range(N))
        saida[f'cal_{estado:05b}'] = qc
    if zne:
        for fator in (1, 3, 5):
            for base in ('Z', 'X'):
                saida[f'zne_{fator}_{base}'] = ghz('conectado', base, fator)
    else:
        for tipo in ('original', 'conectado'):
            for base in ('Z', 'X'):
                saida[f'{tipo}_{base}'] = ghz(tipo, base)
    # Novas instâncias e novos shots: nunca reutilizar contagens da calibração.
    saida['controle_zeros_Z'] = saida['cal_00000'].copy()
    saida['controle_uns_Z'] = saida['cal_11111'].copy()
    for negativo, nome in [(False, 'controle_mais_X'), (True, 'controle_menos_X')]:
        qc = QuantumCircuit(N, N)
        qc.h(range(N))
        if negativo:
            qc.z(0)  # |−> no qubit 0, bit mais à direita: ++++− na ordem q4...q0.
        qc.barrier()
        qc.h(range(N))
        qc.measure(range(N), range(N))
        saida[nome] = qc
    return saida


def compilar(circuitos_logicos):
    mapa = CouplingMap(ARESTAS + [(b, a) for a, b in ARESTAS])
    return dict(zip(circuitos_logicos, transpile(
        list(circuitos_logicos.values()), basis_gates=BASIS, coupling_map=mapa,
        initial_layout=list(range(N)), routing_method='sabre',
        optimization_level=1, seed_transpiler=42)))


def medidas(qc):
    return [(qc.find_bit(item.qubits[0]).index, qc.find_bit(item.clbits[0]).index)
            for item in qc.data if item.operation.name == 'measure']


def reordenar(probabilidades, qc):
    mapa = medidas(qc)
    if len(mapa) != N or len({q for q, _ in mapa}) != N or len({c for _, c in mapa}) != N:
        raise ValueError('Medição não bijetiva')
    saida = np.zeros(DIM)
    for estado, p in enumerate(probabilidades):
        bits = sum(((estado >> q) & 1) << c for q, c in mapa)
        saida[bits] += p
    return saida


def ideal(qc):
    return reordenar(Statevector.from_instruction(qc.remove_final_measurements(inplace=False)).probabilities(), qc)


def esperado(nome):
    p = np.zeros(DIM)
    if nome.startswith('cal_'):
        p[int(nome[4:], 2)] = 1
    elif nome == 'controle_zeros_Z' or nome == 'controle_mais_X':
        p[0] = 1
    elif nome == 'controle_uns_Z':
        p[-1] = 1
    elif nome == 'controle_menos_X':
        p[1] = 1
    elif nome.endswith('_Z'):
        p[[0, -1]] = .5
    else:
        p[PARIDADE == 1] = 1/16
    return p


def validar_circuitos(logicos, compilados):
    for nome in logicos:
        for qc in (logicos[nome], compilados[nome]):
            if not np.allclose(ideal(qc), esperado(nome), atol=1e-12):
                raise ValueError(f'Distribuição ideal incorreta: {nome}')
        for item in compilados[nome].data:
            if item.operation.name == 'cx':
                par = tuple(compilados[nome].find_bit(q).index for q in item.qubits)
                if par not in ARESTAS and par[::-1] not in ARESTAS:
                    raise ValueError('Porta fora do mapa sintético')
    for nome, qc in compilados.items():
        if nome.startswith('conectado') and qc.count_ops().get('cx', 0) != 4:
            raise ValueError('Quantidade incorreta de CX conectadas')
        if nome.startswith('zne_') and qc.count_ops().get('cx', 0) != 4*int(nome.split('_')[1]):
            raise ValueError('Compilação cancelou o dobramento')


def ruido(cenario, incluir_leitura=True):
    if cenario not in ('ideal', 'leitura', 'leitura_e_portas'):
        raise ValueError('Cenário desconhecido')
    modelo = NoiseModel()
    if cenario != 'ideal' and incluir_leitura:
        for q in range(N):
            modelo.add_readout_error(ReadoutError([[1-E01[q], E01[q]], [E10[q], 1-E10[q]]]), [q])
    if cenario == 'leitura_e_portas':
        modelo.add_all_qubit_quantum_error(depolarizing_error(.02, 2), ['cx'])
    return modelo


def matriz_leitura(qc, cenario):
    """A[observado, verdadeiro] em ordem dos bits clássicos, não dos físicos."""
    if cenario == 'ideal':
        return np.eye(DIM)
    matriz = np.ones((DIM, DIM))
    for q, c in medidas(qc):
        erros = np.array([[1-E01[q], E10[q]], [E01[q], 1-E10[q]]])
        for observado in range(DIM):
            for verdadeiro in range(DIM):
                matriz[observado, verdadeiro] *= erros[(observado >> c) & 1, (verdadeiro >> c) & 1]
    return matriz


def referencia_exata(compilados, cenario):
    sim = AerSimulator(method='density_matrix', device='CPU',
                       noise_model=ruido(cenario, incluir_leitura=False), max_parallel_threads=4)
    circuitos_dm = []
    for qc in compilados.values():
        sem_medida = qc.remove_final_measurements(inplace=False)
        sem_medida.save_probabilities()
        circuitos_dm.append(sem_medida)
    resultado = sim.run(circuitos_dm).result()
    saida = {}
    for i, (nome, qc) in enumerate(compilados.items()):
        antes = reordenar(resultado.data(i)['probabilities'], qc)
        depois = matriz_leitura(qc, cenario) @ antes
        saida[nome] = dict(antes_leitura=antes.tolist(), observado=depois.tolist())
    return saida


def vetor(counts, shots):
    p = np.zeros(DIM)
    for bits, qtd in counts.items():
        if len(bits) != N or set(bits)-{'0', '1'} or type(qtd) is not int or qtd < 0:
            raise ValueError('Contagem inválida')
        p[int(bits, 2)] = qtd
    if p.sum() != shots:
        raise ValueError('Número incorreto de shots')
    return p / shots


def pesos(nome):
    if nome.endswith('_X'):
        return PARIDADE
    w = np.zeros(DIM)
    if nome == 'controle_zeros_Z':
        w[0] = 1
    elif nome == 'controle_uns_Z':
        w[-1] = 1
    else:
        w[[0, -1]] = 1
    return w


def corrigir(a, p):
    if not np.isfinite(a).all() or not np.isfinite(p).all():
        raise ValueError('Dados não finitos')
    if not np.allclose(a.sum(axis=0), 1) or not np.allclose(p.sum(axis=0), 1):
        raise ValueError('Dados não normalizados')
    cond = np.linalg.cond(a)
    if not np.isfinite(cond) or cond > 100:
        raise ValueError('Calibração instável')
    q = np.linalg.solve(a, p)
    if not np.allclose(a @ q, p) or not np.allclose(q.sum(axis=0), 1):
        raise ValueError('Falha de inversão')
    return q


def resumo(valor, replicas):
    return dict(valor=float(valor), erro_padrao=float(np.std(replicas, ddof=1)),
                ic95_percentil=np.quantile(replicas, [.025, .975]).tolist())


def intercepto(valores):
    # OLS pré-definido em fatores 1,3,5. Válido para vetores ou lotes (..., 3).
    return np.asarray(valores) @ np.array([13/12, 1/3, -5/12])


def analisar(counts, shots, bootstrap, seed, compilados):
    nomes = [nome for nome in compilados if not nome.startswith('cal_')]
    if set(counts) != set(compilados):
        raise ValueError('Circuitos ausentes ou extras')
    a = np.column_stack([vetor(counts[f'cal_{i:05b}'], shots) for i in range(DIM)])
    p = np.column_stack([vetor(counts[nome], shots) for nome in nomes])
    # Calibração indexada em bits físicos. Cada observação é medida em bits
    # lógicos; SWAPs de roteamento podem alterar essa correspondência.
    def ajustar(matriz, observados):
        saida = []
        for j, nome in enumerate(nomes):
            perm = np.array([sum(((estado >> q) & 1) << c for q, c in medidas(compilados[nome]))
                             for estado in range(DIM)])
            inversa = np.argsort(perm)
            local = matriz[np.ix_(inversa, inversa)]
            saida.append(corrigir(local, observados[:, j]))
        return np.column_stack(saida)
    q = ajustar(a, p)
    w = np.column_stack([pesos(nome) for nome in nomes])
    b, m = (w*p).sum(axis=0), (w*q).sum(axis=0)
    rng = np.random.default_rng(seed)
    rb, rm = np.empty((bootstrap, len(nomes))), np.empty((bootstrap, len(nomes)))
    for i in range(bootstrap):
        ab = np.column_stack([rng.multinomial(shots, a[:, j]) for j in range(DIM)]) / shots
        pb = np.column_stack([rng.multinomial(shots, p[:, j]) for j in range(len(nomes))]) / shots
        rb[i], rm[i] = (w*pb).sum(axis=0), (w*ajustar(ab, pb)).sum(axis=0)
    saida = dict(condicionamento=float(np.linalg.cond(a)), circuitos={}, contrastes={})
    for j, nome in enumerate(nomes):
        saida['circuitos'][nome] = dict(bruto=resumo(b[j], rb[:, j]),
            ajustado=resumo(m[j], rm[:, j]), ganho=resumo(m[j]-b[j], rm[:, j]-rb[:, j]),
            menor_quasi=float(q[:, j].min()))
    for base in ('Z', 'X'):
        if f'original_{base}' in nomes:
            i, j = nomes.index(f'original_{base}'), nomes.index(f'conectado_{base}')
            saida['contrastes'][base] = dict(bruto=resumo(b[j]-b[i], rb[:, j]-rb[:, i]),
                ajustado=resumo(m[j]-m[i], rm[:, j]-rm[:, i]))
        else:
            idx = [nomes.index(f'zne_{f}_{base}') for f in (1, 3, 5)]
            zne, replicas = intercepto(m[idx]), intercepto(rm[:, idx])
            # Comparação com fator 1 usa a mesma réplica: não somar variâncias independentes.
            saida['contrastes'][base] = dict(zne=resumo(zne, replicas),
                zne_menos_fator1=resumo(zne-m[idx[0]], replicas-rm[:, idx[0]]))
    return saida
