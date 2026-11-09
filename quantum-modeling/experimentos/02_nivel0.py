"""
Compara, para cada job de GHZ ja rodado na IBM, o resultado real do hardware
com uma simulacao local calibrada (Nivel 0: calibracao padrao do backend).
Salva tudo num unico arquivo de resultados para uso posterior no ajuste evolutivo.
"""

import os
import json
from qiskit_ibm_runtime import QiskitRuntimeService
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel
from qiskit.quantum_info import hellinger_distance

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ---- Jobs de GHZ confirmados (um por tamanho) ----
JOBS_GHZ = [
    ("db2fmk47f06c73apoos0", 5),
    ("db2g70e8v0ts73c2pdf0", 10),
    ("db2g86vr11fs7396mt00", 15),
    ("db2g9jk2ljfc73d4ecs0", 20),
    ("db2gbrnr11fs7396n3e0", 25),
    ("db344rc7f06c73aqstag", 30),
    ("db346rm8v0ts73c3sb3g", 35),
    ("db37spqqfgmc73d0a850", 40),
    ("db37v1j9kq9s73atb000", 45),
    ("db37vg9lb5cs73fhee7g", 50),
]


def escolher_metodo(n_qubits):
    """
    density_matrix cresce em 4^n (explode rapido, so viavel ate ~10-12 qubits).
    statevector com ruido usa trajetorias quanticas, cresce em 2^n (viavel ate ~25).
    matrix_product_state escala bem para GHZ grandes (baixo emaranhado efetivo).
    """
    if n_qubits <= 20:
        return "statevector"
    return "matrix_product_state"


def main():
    service = QiskitRuntimeService()
    resultados = []
    cache_backend = {}

    for job_id, tamanho in JOBS_GHZ:
        print(f"\n=== Processando {job_id} (GHZ-{tamanho}) ===")
        try:
            job = service.job(job_id)
            backend_name = job.backend().name
            result = job.result()
            data = result[0].data
            counts_real = (
                data.c.get_counts() if hasattr(data, "c") else data.meas.get_counts()
            )

            inputs = job.inputs
            isa_circuit = inputs["pubs"][0][0]
            shots = sum(counts_real.values())

            metodo = escolher_metodo(tamanho)

            chave_cache = (backend_name, metodo)
            if chave_cache not in cache_backend:
                backend_real = service.backend(backend_name)
                noise_model = NoiseModel.from_backend(backend_real)
                sim = AerSimulator(method=metodo, noise_model=noise_model)
                cache_backend[chave_cache] = sim
            sim = cache_backend[chave_cache]

            sim_result = sim.run(isa_circuit, shots=shots).result()
            counts_sim = sim_result.get_counts()

            dist = hellinger_distance(counts_real, counts_sim)
            print(f"  backend={backend_name} metodo={metodo} hellinger={dist:.4f}")

            resultados.append({
                "job_id": job_id,
                "tamanho_ghz": tamanho,
                "backend": backend_name,
                "data_hardware": str(job.creation_date),
                "metodo_simulacao": metodo,
                "shots": shots,
                "counts_real": counts_real,
                "counts_sim_nivel0": counts_sim,
                "hellinger_nivel0": dist,
            })

        except Exception as e:
            print(f"  ERRO neste job: {e}")
            resultados.append({
                "job_id": job_id,
                "tamanho_ghz": tamanho,
                "erro": str(e),
            })

    caminho_saida = os.path.join(BASE_DIR, "..", "resultados", "resultados_ghz_nivel0.json")
    with open(caminho_saida, "w") as f:
        json.dump(resultados, f, indent=2)

    print("\n\nResumo final:")
    for r in resultados:
        if "hellinger_nivel0" in r:
            print(f"  GHZ-{r['tamanho_ghz']:>2} | {r['backend']:<12} | Hellinger = {r['hellinger_nivel0']:.4f}")
        else:
            print(f"  GHZ-{r['tamanho_ghz']:>2} | ERRO: {r.get('erro')}")

    print(f"\nSalvo em {caminho_saida}")


if __name__ == "__main__":
    main()