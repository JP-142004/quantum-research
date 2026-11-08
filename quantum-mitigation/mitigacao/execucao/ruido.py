"""Modelo de ruído sintético do simulador. Os valores são escolhidos por nós: não são
uma calibração de nenhum computador real."""
import numpy as np
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, ReadoutError, depolarizing_error

from mitigacao.execucao import info_compilado

CENARIOS = ('ideal', 'leitura', 'leitura_e_portas')
E01 = [0.01, 0.02, 0.03, 0.04, 0.05]   # chance de ler 1 quando o qubit estava em 0, por qubit
E10 = [0.06, 0.05, 0.04, 0.03, 0.02]   # chance de ler 0 quando o qubit estava em 1, por qubit
DEPOLARIZANTE_CX = 0.02                # ruído depois de cada CX


def parametros():
    return dict(e01=E01, e10=E10, depolarizante_cx=DEPOLARIZANTE_CX)


def modelo_ruido(cenario, n, incluir_leitura=True):
    """'ideal' (sem ruído), 'leitura' (só erro de leitura) ou 'leitura_e_portas'."""
    if cenario not in CENARIOS:
        raise ValueError(f'Cenário desconhecido: {cenario}')
    modelo = NoiseModel()
    if cenario != 'ideal' and incluir_leitura:
        for q in range(n):
            e01, e10 = E01[q % len(E01)], E10[q % len(E10)]
            modelo.add_readout_error(ReadoutError([[1 - e01, e01], [e10, 1 - e10]]), [q])
    if cenario == 'leitura_e_portas':
        modelo.add_all_qubit_quantum_error(depolarizing_error(DEPOLARIZANTE_CX, 2), ['cx'])
    return modelo


def reordenar(prob, mapa_medidas, n):
    """Probabilidades indexadas pelo estado dos qubits físicos -> pelo dos bits clássicos."""
    saida = np.zeros(2 ** n)
    for estado, p in enumerate(prob):
        saida[sum(((estado >> q) & 1) << c for q, c in mapa_medidas)] += p
    return saida


def matriz_leitura(mapa_medidas, cenario):
    """A[observado, verdadeiro] do modelo, na ordem dos bits clássicos."""
    dim = 2 ** len(mapa_medidas)
    if cenario == 'ideal':
        return np.eye(dim)
    a = np.ones((dim, dim))
    for q, c in mapa_medidas:
        e01, e10 = E01[q % len(E01)], E10[q % len(E10)]
        erro = np.array([[1 - e01, e10], [e01, 1 - e10]])
        for observado in range(dim):
            for verdadeiro in range(dim):
                a[observado, verdadeiro] *= erro[(observado >> c) & 1, (verdadeiro >> c) & 1]
    return a


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
