from qiskit import QuantumCircuit, transpile
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler

NUM_QUBITS = 40  
SHOTS = 1000
BACKEND_NAME = "ibm_kingston"

# Prepara o estado GHZ:
# (|000...000⟩ + |111...111⟩) / √2
qc = QuantumCircuit(NUM_QUBITS, NUM_QUBITS)
qc.h(0)

for qubit in range(1, NUM_QUBITS):
    qc.cx(0, qubit)

qc.measure(range(NUM_QUBITS), range(NUM_QUBITS))

print(f"Circuito GHZ de {NUM_QUBITS} qubits:")
print(qc.draw())

service = QiskitRuntimeService(channel="ibm_quantum_platform")
backend = service.backend(BACKEND_NAME)
print(f"\nBackend: {backend.name}")

compiled = transpile(qc, backend=backend, optimization_level=1)

sampler = Sampler(mode=backend)
job = sampler.run([compiled], shots=SHOTS)

print(f"Job enviado. ID: {job.job_id()}")
print(f"Status inicial: {job.status()}")
print("Aguardando resultado...")

job_result = job.result()
print(f"\nStatus do job: {job.status()}")

counts = job_result[0].data.c.get_counts()

print(f"\n{'RESULTADO':<{NUM_QUBITS + 2}} {'CONTAGEM':>10}")
print("-" * (NUM_QUBITS + 14))

# Mostra os resultados em ordem crescente
for estado in sorted(counts):
    print(f"{estado:<{NUM_QUBITS + 2}} {counts[estado]:>10}")

total = sum(counts.values())
print("-" * (NUM_QUBITS + 14))
print(f"{'Total de medições:':<{NUM_QUBITS + 2}} {total:>10}")

# Em um GHZ ideal, os únicos resultados são todos zeros ou todos uns
todos_zero = "0" * NUM_QUBITS
todos_um = "1" * NUM_QUBITS
fora_do_esperado = total - counts.get(todos_zero, 0) - counts.get(todos_um, 0)

print(
    f"\nResultados fora dos estados GHZ ideais: "
    f"{fora_do_esperado}/{total} "
    f"({100 * fora_do_esperado / total:.2f}%)"
)