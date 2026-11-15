"""Modelos de ruido.

Nivel 0: modelo padrao da IBM (NoiseModel.from_backend), mas montado a partir
do snapshot de calibracao do dia do job, e nao da calibracao de hoje.
"""

from types import SimpleNamespace

from qiskit_aer.noise import NoiseModel
from qiskit_ibm_runtime.utils.backend_converter import convert_to_target


def nivel0(propriedades, configuracao):
    """Reconstroi o Target do backend com a calibracao salva e usa o mesmo
    caminho do NoiseModel.from_backend original (erros de porta, leitura e
    relaxacao termica). Qubits com defeito sao descartados pelo conversor."""
    target = convert_to_target(configuracao, propriedades)
    backend = SimpleNamespace(version=2, target=target,
                              operation_names=list(target.operation_names), dt=target.dt)
    return NoiseModel.from_backend(backend)


# Modelos disponiveis para os scripts de analise: nome -> funcao(propriedades, configuracao).
# O Nivel 1 (ajustado) entra aqui quando o ajuste for revisado.
MODELOS = {"nivel0": nivel0}


# ---------------------------------------------------------------- Nivel 1

import numpy as np
from qiskit_aer.noise import depolarizing_error, thermal_relaxation_error, ReadoutError

# Variaveis ajustadas: multiplicadores da calibracao media dos qubits usados.
GENES = ["erro_1q", "erro_2q", "leitura_1_dado_0", "leitura_0_dado_1", "t1", "t2"]
LIMITES = [(0.1, 5.0), (0.1, 5.0), (0.1, 5.0), (0.1, 5.0), (0.2, 3.0), (0.2, 3.0)]
PORTAS_1Q = ["sx", "x"]  # rz e virtual no hardware (erro zero)
PORTAS_2Q = ["cz"]


def calibracao_media(propriedades, qubits):
    """Medias da calibracao so nos qubits fisicos usados pelo lote."""
    qs = set(qubits)

    def media(valores, padrao):
        valores = [v for v in valores if v is not None]
        return float(np.mean(valores)) if valores else padrao

    e1, d1, e2, d2 = [], [], [], []
    for g in propriedades.gates:
        if not set(g.qubits) <= qs:
            continue
        par = {p.name: p.value for p in g.parameters}
        if g.gate in PORTAS_1Q:
            e1.append(par.get("gate_error")); d1.append(par.get("gate_length"))
        elif g.gate in PORTAS_2Q:
            e2.append(par.get("gate_error")); d2.append(par.get("gate_length"))
    t1, t2, p10, p01 = [], [], [], []
    for q in qs:
        props = propriedades.qubit_property(q)
        pega = lambda nome: props[nome][0] if nome in props else None
        t1.append(pega("T1")); t2.append(pega("T2"))
        p10.append(pega("prob_meas1_prep0")); p01.append(pega("prob_meas0_prep1"))
    # gate_length vem em ns na calibracao da IBM
    return {
        "erro_1q": media(e1, 0.0), "erro_2q": media(e2, 0.0),
        "leitura_1_dado_0": media(p10, 0.0), "leitura_0_dado_1": media(p01, 0.0),
        "t1": media(t1, 100e-6), "t2": media(t2, 100e-6),
        "duracao_1q": media(d1, 36.0) * 1e-9, "duracao_2q": media(d2, 68.0) * 1e-9,
    }


def nivel1(escalas, calib):
    """Modelo uniforme (mesmo erro em todos os qubits) com leitura assimetrica.
    escalas: multiplicadores na ordem de GENES."""
    s1, s2, s10, s01, st1, st2 = escalas
    e1 = min(calib["erro_1q"] * s1, 0.999)
    e2 = min(calib["erro_2q"] * s2, 0.999)
    p10 = min(calib["leitura_1_dado_0"] * s10, 0.5)
    p01 = min(calib["leitura_0_dado_1"] * s01, 0.5)
    t1 = max(calib["t1"] * st1, 1e-9)
    t2 = min(max(calib["t2"] * st2, 1e-9), 2 * t1)

    modelo = NoiseModel(basis_gates=["sx", "x", "rz", "cz"])
    err1 = depolarizing_error(e1, 1).compose(thermal_relaxation_error(t1, t2, calib["duracao_1q"]))
    modelo.add_all_qubit_quantum_error(err1, PORTAS_1Q)
    tr = thermal_relaxation_error(t1, t2, calib["duracao_2q"])
    err2 = depolarizing_error(e2, 2).compose(tr.tensor(tr))
    modelo.add_all_qubit_quantum_error(err2, PORTAS_2Q)
    # linhas = estado preparado, colunas = resultado medido
    modelo.add_all_qubit_readout_error(ReadoutError([[1 - p10, p10], [p01, 1 - p01]]))
    return modelo
