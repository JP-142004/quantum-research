from qiskit import QuantumCircuit, transpile
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler

BACKEND_NAME = "ibm_fez"
SHOTS = 1000

service = QiskitRuntimeService(channel="ibm_quantum_platform")
backend = service.backend(BACKEND_NAME)

# Nome do teste e qubits físicos utilizados.
testes = [
    ("Qubit 0 sozinho", [0]),
    ("Qubit 1 sozinho", [1]),
    ("Cinco qubits juntos", [0, 1, 2, 3, 4]),
]

circuitos = []

for nome, qubits in testes:
    n = len(qubits)

    # Sem portas: mede diretamente o estado inicial.
    qc = QuantumCircuit(n, n)
    qc.measure(range(n), range(n))

    compiled = transpile(
        qc,
        backend=backend,
        initial_layout=qubits,
        optimization_level=1,
    )

    circuitos.append(compiled)

sampler = Sampler(mode=backend)
sampler.options.dynamical_decoupling.enable = False
sampler.options.twirling.enable_gates = False
sampler.options.twirling.enable_measure = False
sampler.options.execution.init_qubits = True

print(f"Backend: {backend.name}")
print("Enviando três circuitos, com 1.000 medições cada...")

job = sampler.run(circuitos, shots=SHOTS)

print(f"ID do job: {job.job_id()}", flush=True)
print("Aguardando resultado...")

resultado = job.result()

for indice, (nome, qubits) in enumerate(testes):
    counts = resultado[indice].data.c.get_counts()
    total = sum(counts.values())
    esperado = "0" * len(qubits)
    acertos = counts.get(esperado, 0)

    print("\n" + "=" * 50)
    print(nome)
    print(f"Qubits físicos: {qubits}")
    print(f"Resultado esperado: {esperado}")

    print("\nCONTAGENS")
    for bits, quantidade in sorted(counts.items()):
        print(f"{bits}: {quantidade}")

    print(f"\nTodos zeros: {acertos}/{total}")
    print("\nDesvios por qubit físico:")

    for posicao, qubit_fisico in enumerate(qubits):
        # Qiskit mostra o bit clássico 0 à direita.
        quantidade_uns = sum(
            quantidade
            for bits, quantidade in counts.items()
            if bits[-1 - posicao] == "1"
        )

        percentual = 100 * quantidade_uns / total

        print(
            f"Qubit {qubit_fisico}: "
            f"{quantidade_uns}/{total} ({percentual:.2f}%)"
        )