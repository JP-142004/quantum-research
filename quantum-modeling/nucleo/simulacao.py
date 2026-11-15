"""Simulacao local com o Aer, com seed e configuracao registradas."""

import time
from qiskit_aer import AerSimulator

# Valores padrao do Aer, escritos explicitamente para ficarem no manifesto.
OPCOES_MPS = {
    "matrix_product_state_max_bond_dimension": None,
    "matrix_product_state_truncation_threshold": 1e-16,
}


LIMITE_STATEVECTOR = 20


def seed_independente(seed, k):
    """k-esima seed independente a partir de uma seed base.
    O Aer usa seed + i no shot i, entao seeds vizinhas (1234 e 1235) repetem
    quase todos os shots e dao simulacoes praticamente iguais."""
    return seed + k * 10_000_019


def escolher_metodo(n_qubits, limite=None):
    """
    density_matrix cresce em 4^n (estourou a RAM no GHZ-15). Nao usar.
    statevector com ruido (trajetorias) e viavel ate ~20 qubits.
    matrix_product_state escala bem para GHZ maiores.
    """
    limite = LIMITE_STATEVECTOR if limite is None else limite
    return "statevector" if n_qubits <= limite else "matrix_product_state"


def criar_simulador(metodo, modelo_ruido):
    opcoes = OPCOES_MPS if metodo == "matrix_product_state" else {}
    return AerSimulator(method=metodo, noise_model=modelo_ruido, **opcoes)


def simular(circuito, modelo_ruido, shots, seed, metodo):
    """Roda o circuito e devolve (contagens, segundos, configuracao usada)."""
    sim = criar_simulador(metodo, modelo_ruido)
    inicio = time.perf_counter()
    counts = sim.run(circuito, shots=shots, seed_simulator=seed).result().get_counts()
    segundos = time.perf_counter() - inicio
    config = {"metodo": metodo, "shots": shots, "seed_simulator": seed}
    if metodo == "matrix_product_state":
        config.update(OPCOES_MPS)
    return counts, segundos, config
