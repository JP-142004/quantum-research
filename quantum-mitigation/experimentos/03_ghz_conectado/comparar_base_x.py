from qiskit import QuantumCircuit, transpile
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler

BACKEND_NAME = "ibm_fez"
QUBITS_FISICOS = [0, 1, 2, 3, 4]
SHOTS = 1000
N = 5

service = QiskitRuntimeService(channel="ibm_quantum_platform")
backend = service.backend(BACKEND_NAME)

# 1. GHZ anterior: todas as CX partem do qubit 0.
anterior = QuantumCircuit(N, N)
anterior.h(0)

for qubit in range(1, N):
    anterior.cx(0, qubit)

# 2. GHZ que segue as conexões físicas observadas no Fez.
conectado = QuantumCircuit(N, N)
conectado.h(2)
conectado.cx(2, 1)
conectado.cx(2, 3)
conectado.cx(1, 0)
conectado.cx(3, 4)

nomes = ["GHZ anterior — base X", "GHZ conectado — base X"]
circuitos = []

for nome, qc in zip(nomes, [anterior, conectado]):
    # Separa a preparação da mudança de base.
    qc.barrier()

    # H antes da leitura permite medir em X.
    for qubit in range(N):
        qc.h(qubit)

    qc.measure(range(N), range(N))

    compiled = transpile(
        qc,
        backend=backend,
        initial_layout=QUBITS_FISICOS,
        optimization_level=1,
        seed_transpiler=42,
    )

    circuitos.append(compiled)

    print(f"\n{nome}")
    print(f"Backend: {backend.name}")
    print(f"Profundidade: {compiled.depth()}")
    print(f"Operações: {dict(compiled.count_ops())}")
    print(
        "Mapeamento final:",
        compiled.layout.final_index_layout(filter_ancillas=True),
    )

sampler = Sampler(mode=backend)
sampler.options.dynamical_decoupling.enable = False
sampler.options.twirling.enable_gates = False
sampler.options.twirling.enable_measure = False
sampler.options.execution.init_qubits = True

# 1.000 medições por circuito: 2.000 no total.
job = sampler.run(circuitos, shots=SHOTS)

print(f"\nID do job: {job.job_id()}", flush=True)
print("Aguardando resultados...")

resultado = job.result()

for indice, nome in enumerate(nomes):
    counts = resultado[indice].data.c.get_counts()
    total = sum(counts.values())

    pares = sum(
        quantidade
        for bits, quantidade in counts.items()
        if bits.count("1") % 2 == 0
    )
    impares = total - pares

    correlacao_x = (pares - impares) / total

    # Erro padrão aproximado por amostragem.
    erro_padrao = (
        max(0.0, 1 - correlacao_x**2) / total
    ) ** 0.5

    print("\n" + "=" * 55)
    print(nome)
    print("\nCONTAGENS")

    for bits, quantidade in sorted(counts.items()):
        print(f"{bits}: {quantidade}")

    print(f"\nTotal: {total}")
    print(f"Paridade par: {pares}")
    print(f"Paridade ímpar: {impares}")
    print(f"Correlação X: {correlacao_x:.4f}")
    print(f"Erro padrão aproximado: {erro_padrao:.4f}")
    print("Correlação X ideal: +1")