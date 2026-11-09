"""
Ajusta um modelo de ruido parametrizado (5 escalas: erro 1Q, erro 2Q,
erro de leitura, T1, T2) usando evolucao diferencial, para minimizar a
distancia de Hellinger entre simulacao local e hardware real.

Treino: GHZ-5, 10, 15 (rapidos de simular, usados para o ajuste em si)
Validacao: GHZ-20 a 50 (nunca vistos pelo otimizador, provam generalizacao)

Usa como linha de base a execucao mais recente de 02_nivel0.py.
Pendente (PR 2): leitura assimetrica, calibracao do dia do job, seed fixa,
remover rz do ruido, opcao --rapido.
"""

import os
import sys
import json
import numpy as np
from scipy.optimize import differential_evolution
from qiskit_ibm_runtime import QiskitRuntimeService
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error, thermal_relaxation_error, ReadoutError
from qiskit.quantum_info import hellinger_distance

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from nucleo import registro
from nucleo.simulacao import escolher_metodo

CAMINHO_BASELINE = os.path.join(registro.ultima_pasta_execucao("nivel0"), "resultados.json")

TREINO = [5, 10, 15]
VALIDACAO = [20, 25, 30, 35, 40, 45, 50]


def carregar_baseline():
    with open(CAMINHO_BASELINE, "r") as f:
        dados = json.load(f)
    return {r["tamanho_ghz"]: r for r in dados if "hellinger_nivel0" in r}


def extrair_calibracao_media(backend):
    """Calcula medias de erro/tempo a partir da calibracao real do backend."""
    props = backend.properties()

    erros_1q, erros_2q = [], []
    t1s, t2s = [], []
    erros_leitura = []
    duracao_1q, duracao_2q = [], []

    for gate in props.gates:
        if len(gate.qubits) == 1:
            try:
                erros_1q.append(props.gate_error(gate.gate, gate.qubits))
                duracao_1q.append(props.gate_length(gate.gate, gate.qubits))
            except Exception:
                pass
        elif len(gate.qubits) == 2:
            try:
                erros_2q.append(props.gate_error(gate.gate, gate.qubits))
                duracao_2q.append(props.gate_length(gate.gate, gate.qubits))
            except Exception:
                pass

    for q in range(len(props.qubits)):
        try:
            t1s.append(props.t1(q))
            t2s.append(props.t2(q))
            erros_leitura.append(props.readout_error(q))
        except Exception:
            pass

    return {
        "erro_1q": float(np.mean(erros_1q)) if erros_1q else 0.0,
        "erro_2q": float(np.mean(erros_2q)) if erros_2q else 0.0,
        "erro_leitura": float(np.mean(erros_leitura)) if erros_leitura else 0.0,
        "t1": float(np.mean(t1s)) if t1s else 100e-6,
        "t2": float(np.mean(t2s)) if t2s else 100e-6,
        "duracao_1q": float(np.mean(duracao_1q)) if duracao_1q else 35e-9,
        "duracao_2q": float(np.mean(duracao_2q)) if duracao_2q else 300e-9,
    }


def montar_modelo(escalas, calib, basis_gates_1q, basis_gates_2q):
    s1q, s2q, sro, st1, st2 = escalas

    erro_1q = min(max(calib["erro_1q"] * s1q, 0.0), 0.999)
    erro_2q = min(max(calib["erro_2q"] * s2q, 0.0), 0.999)
    erro_leitura = min(max(calib["erro_leitura"] * sro, 0.0), 0.5)
    t1 = max(calib["t1"] * st1, 1e-9)
    t2 = min(max(calib["t2"] * st2, 1e-9), 2 * t1)

    modelo = NoiseModel()

    dep_1q = depolarizing_error(erro_1q, 1)
    term_1q = thermal_relaxation_error(t1, t2, calib["duracao_1q"])
    erro_1q_total = dep_1q.compose(term_1q)
    for gate in basis_gates_1q:
        modelo.add_all_qubit_quantum_error(erro_1q_total, gate)

    dep_2q = depolarizing_error(erro_2q, 2)
    term_2q_single = thermal_relaxation_error(t1, t2, calib["duracao_2q"])
    term_2q = term_2q_single.tensor(term_2q_single)
    erro_2q_total = dep_2q.compose(term_2q)
    for gate in basis_gates_2q:
        modelo.add_all_qubit_quantum_error(erro_2q_total, gate)

    ro_error = ReadoutError([[1 - erro_leitura, erro_leitura], [erro_leitura, 1 - erro_leitura]])
    modelo.add_all_qubit_readout_error(ro_error)

    return modelo


def main():
    service = QiskitRuntimeService()
    baseline = carregar_baseline()

    backend_name = baseline[TREINO[0]]["backend"]
    backend = service.backend(backend_name)
    calib = extrair_calibracao_media(backend)
    print("Calibracao media extraida:", calib)

    basis_gates_1q = ["sx", "x", "rz"]
    basis_gates_2q = ["cz", "ecr", "cx"]

    circuitos = {}
    for tamanho in TREINO + VALIDACAO:
        job_id = baseline[tamanho]["job_id"]
        job = service.job(job_id)
        inputs = job.inputs
        isa_circuit = inputs["pubs"][0][0]
        shots = baseline[tamanho]["shots"]
        circuitos[tamanho] = {
            "isa_circuit": isa_circuit,
            "shots": shots,
            "counts_real": baseline[tamanho]["counts_real"],
        }

    def rodar_simulacao(tamanho, modelo):
        metodo = escolher_metodo(tamanho)
        sim = AerSimulator(method=metodo, noise_model=modelo)
        info = circuitos[tamanho]
        result = sim.run(info["isa_circuit"], shots=info["shots"]).result()
        return result.get_counts()

    def aptidao(escalas):
        modelo = montar_modelo(escalas, calib, basis_gates_1q, basis_gates_2q)
        distancias = []
        for tamanho in TREINO:
            counts_sim = rodar_simulacao(tamanho, modelo)
            d = hellinger_distance(circuitos[tamanho]["counts_real"], counts_sim)
            distancias.append(d)
        media = float(np.mean(distancias))
        print(f"  testando escalas={np.round(escalas, 3)} -> hellinger medio treino={media:.4f}")
        return media

    limites = [
        (0.1, 5.0),
        (0.1, 5.0),
        (0.1, 5.0),
        (0.2, 3.0),
        (0.2, 3.0),
    ]

    print("\n=== Iniciando evolucao diferencial (treino: GHZ-5, 10, 15) ===")
    resultado_de = differential_evolution(
        aptidao, limites, maxiter=20, popsize=10, seed=42, polish=True, workers=1
    )

    melhores_escalas = resultado_de.x
    print(f"\nMelhores escalas encontradas: {np.round(melhores_escalas, 4)}")
    print(f"Hellinger medio no treino (ajustado): {resultado_de.fun:.4f}")

    print("\n=== Validando em tamanhos nunca vistos pelo ajuste ===")
    modelo_final = montar_modelo(melhores_escalas, calib, basis_gates_1q, basis_gates_2q)

    comparacao = []
    for tamanho in TREINO + VALIDACAO:
        counts_sim_ajustado = rodar_simulacao(tamanho, modelo_final)
        hellinger_ajustado = hellinger_distance(circuitos[tamanho]["counts_real"], counts_sim_ajustado)
        hellinger_nivel0 = baseline[tamanho]["hellinger_nivel0"]
        conjunto = "treino" if tamanho in TREINO else "validacao"
        print(f"  GHZ-{tamanho:>2} ({conjunto:<10}) | Nivel0 = {hellinger_nivel0:.4f} | Ajustado = {hellinger_ajustado:.4f}")
        comparacao.append({
            "tamanho_ghz": tamanho,
            "conjunto": conjunto,
            "hellinger_nivel0": hellinger_nivel0,
            "hellinger_ajustado": hellinger_ajustado,
            "melhoria": hellinger_nivel0 - hellinger_ajustado,
        })

    saida = {
        "escalas_otimizadas": {
            "erro_1q": melhores_escalas[0],
            "erro_2q": melhores_escalas[1],
            "erro_leitura": melhores_escalas[2],
            "t1": melhores_escalas[3],
            "t2": melhores_escalas[4],
        },
        "calibracao_base": calib,
        "comparacao": comparacao,
    }
    CAMINHO_SAIDA = os.path.join(registro.nova_pasta_execucao("ajuste_nivel1"), "resultados.json")
    with open(CAMINHO_SAIDA, "w") as f:
        json.dump(saida, f, indent=2)

    print(f"\nSalvo em {CAMINHO_SAIDA}")


if __name__ == "__main__":
    main()