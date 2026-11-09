"""Simulacao local com o Aer, com seed e configuracao registradas."""

import time
from qiskit_aer import AerSimulator

# Valores padrao do Aer, escritos explicitamente para ficarem no manifesto.
OPCOES_MPS = {
    "matrix_product_state_max_bond_dimension": None,
    "matrix_product_state_truncation_threshold": 1e-16,
}


def escolher_metodo(n_qubits):
    """
    density_matrix cresce em 4^n (estourou a RAM no GHZ-15). Nao usar.
    statevector com ruido (trajetorias) e viavel ate ~20 qubits.
    matrix_product_state escala bem para GHZ maiores.
    """
    return "statevector" if n_qubits <= 20 else "matrix_product_state"


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
