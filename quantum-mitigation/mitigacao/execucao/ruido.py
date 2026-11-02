"""Modelo de ruído sintético do simulador. Os valores são escolhidos por nós: não são
uma calibração de nenhum computador real."""
from qiskit_aer.noise import NoiseModel, ReadoutError, depolarizing_error

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
