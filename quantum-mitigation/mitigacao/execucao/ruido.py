"""Modelo de ruído sintético do simulador. Os valores são escolhidos por nós: não são
uma calibração de nenhum computador real."""
import numpy as np
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, ReadoutError, depolarizing_error

from mitigacao.execucao import info_compilado

CENARIOS = ('ideal', 'leitura', 'leitura_e_portas')
# Fora de CENARIOS de propósito: o experimento 5 percorre CENARIOS e ganharia sessões novas.
CORRELACIONADO = 'leitura_correlacionada'
CORRELACAO = 0.03                      # chance de os dois qubits de um par (0,1), (2,3), ... lerem errado juntos
E01 = [0.01, 0.02, 0.03, 0.04, 0.05]   # chance de ler 1 quando o qubit estava em 0, por qubit
E10 = [0.06, 0.05, 0.04, 0.03, 0.02]   # chance de ler 0 quando o qubit estava em 1, por qubit
DEPOLARIZANTE_CX = 0.02                # ruído depois de cada CX


def parametros():
    return dict(e01=E01, e10=E10, depolarizante_cx=DEPOLARIZANTE_CX)


def modelo_ruido(cenario, n, incluir_leitura=True):
    """'ideal' (sem ruído), 'leitura' (só erro de leitura) ou 'leitura_e_portas'."""
    if cenario not in CENARIOS + (CORRELACIONADO,):
        raise ValueError(f'Cenário desconhecido: {cenario}')
    modelo = NoiseModel()
    # O simulador não aplica erro de leitura entre dois qubits (cada medida é uma instrução): o cenário
    # correlacionado fica sem erro de leitura aqui, e `aplicar_leitura` o aplica às contagens depois.
    if cenario in ('leitura', 'leitura_e_portas') and incluir_leitura:
        for q in range(n):
            modelo.add_readout_error(ReadoutError(_tabela(q).T.tolist()), [q])   # o simulador quer [verdadeiro][observado]
    if cenario == 'leitura_e_portas':
        modelo.add_all_qubit_quantum_error(depolarizing_error(DEPOLARIZANTE_CX, 2), ['cx'])
    return modelo


def reordenar(prob, mapa_medidas, n):
    """Probabilidades indexadas pelo estado dos qubits físicos -> pelo dos bits clássicos."""
    saida = np.zeros(2 ** n)
    for estado, p in enumerate(prob):
        saida[sum(((estado >> q) & 1) << c for q, c in mapa_medidas)] += p
    return saida


def _tabela(q):
    """Um qubit sozinho: a[observado, verdadeiro]."""
    e01, e10 = E01[q % len(E01)], E10[q % len(E10)]
    return np.array([[1 - e01, e10], [e01, 1 - e10]])


def _blocos(qubits, cenario):
    """[(qubits do bloco, a[observado, verdadeiro])]. O índice do bloco é soma de bit_i << i, na ordem dos qubits.

    'leitura': um bloco por qubit. 'leitura_correlacionada': o mesmo erro por qubit, e com chance
    CORRELACAO os dois qubits de cada par (2k, 2k+1) leem errado ao mesmo tempo.
    """
    qubits, blocos, vistos = sorted(qubits), [], set()
    for q in qubits:
        if q in vistos:
            continue
        if cenario == CORRELACIONADO and q % 2 == 0 and q + 1 in qubits:
            independente = np.kron(_tabela(q + 1), _tabela(q))
            junto = np.eye(4)[::-1]   # os dois bits trocam
            blocos.append(((q, q + 1), (1 - CORRELACAO) * independente + CORRELACAO * junto))
            vistos.update((q, q + 1))
        else:
            blocos.append(((q,), _tabela(q)))
            vistos.add(q)
    return blocos


def matriz_leitura(mapa_medidas, cenario):
    """A[observado, verdadeiro] do modelo, na ordem dos bits clássicos."""
    dim = 2 ** len(mapa_medidas)
    if cenario == 'ideal':
        return np.eye(dim)
    clbit = dict(mapa_medidas)
    estados = np.arange(dim)
    a = np.ones((dim, dim))
    for bits, bloco in _blocos(clbit, cenario):
        indice = sum(((estados >> clbit[q]) & 1) << i for i, q in enumerate(bits))
        a *= bloco[indice[:, None], indice[None, :]]
    return a


def aplicar_leitura(contagens, mapa_medidas, cenario, rng):
    """Passa as contagens de um circuito pelo erro de leitura do cenário (usado só no correlacionado)."""
    dim = len(mapa_medidas)
    a = matriz_leitura(mapa_medidas, cenario)
    saida = {}
    for bits, vezes in contagens.items():
        for observado, k in enumerate(rng.multinomial(vezes, a[:, int(bits, 2)])):
            if k:
                chave = f'{observado:0{dim}b}'
                saida[chave] = saida.get(chave, 0) + int(k)
    return saida


def referencia_exata(compilados, cenario):
    """Distribuição exata do modelo, sem flutuação de shots.

    compilados: {nome: circuito compilado}. Devolve {nome: dict(antes_leitura, observado)},
    cada um um vetor na ordem dos bits clássicos: o estado que chega à leitura e o que
    o equipamento registraria depois do erro de leitura.
    """
    n_max = max(qc.num_qubits for qc in compilados.values())
    sim = AerSimulator(method='density_matrix', device='CPU', max_parallel_threads=4,
                       noise_model=modelo_ruido(cenario, n_max, incluir_leitura=False))
    sem_medida = []
    for qc in compilados.values():
        copia = qc.remove_final_measurements(inplace=False)
        copia.save_probabilities()
        sem_medida.append(copia)
    resultado = sim.run(sem_medida).result()
    saida = {}
    for i, (nome, qc) in enumerate(compilados.items()):
        mapa = info_compilado(qc)['mapa_medidas']
        antes = reordenar(resultado.data(i)['probabilities'], mapa, qc.num_qubits)
        saida[nome] = dict(antes_leitura=antes, observado=matriz_leitura(mapa, cenario) @ antes)
    return saida
