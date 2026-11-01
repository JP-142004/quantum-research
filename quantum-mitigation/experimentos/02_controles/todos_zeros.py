from qiskit import QuantumCircuit, transpile
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler

NUM_QUBITS = 5
SHOTS = 1000
BACKEND_NAME = "ibm_kingston"

# Teste: medir o estado inicial, sem criar o GHZ.
# Resultado ideal: 00000 em todas as medições.
qc = QuantumCircuit(NUM_QUBITS, NUM_QUBITS)
qc.measure(range(NUM_QUBITS), range(NUM_QUBITS))

print("Circuito de teste — todos zeros:")
print(qc.draw())

# Carrega as credenciais salvas no computador
service = QiskitRuntimeService(channel="ibm_quantum_platform")

# Seleciona exatamente o dispositivo solicitado
backend = service.backend(BACKEND_NAME)
print(f"\nBackend: {backend.name}")

# Usa explicitamente os qubits físicos 0, 1, 2, 3 e 4.
# Não sabemos ainda se foram os mesmos utilizados no GHZ anterior.
qubits_fisicos = [0, 1, 2, 3, 4]

compiled = transpile(
    qc,
    backend=backend,
    initial_layout=qubits_fisicos,
    optimization_level=1,
)

print(f"Qubits físicos: {qubits_fisicos}")

sampler = Sampler(mode=backend)
sampler.options.dynamical_decoupling.enable = False
sampler.options.twirling.enable_gates = False
sampler.options.twirling.enable_measure = False
sampler.options.execution.init_qubits = True

job = sampler.run([compiled], shots=SHOTS)

print(f"Job enviado. ID: {job.job_id()}", flush=True)
print("Aguardando resultado...")

job_result = job.result()
counts = job_result[0].data.c.get_counts()

print(f"\nStatus do job: {job.status()}")
print("\nRESULTADO    CONTAGEM")
print("---------------------")

for estado in sorted(counts):
    print(f"{estado:<12} {counts[estado]:>7}")

total = sum(counts.values())
corretos = counts.get("00000", 0)
outros = total - corretos

print(f"\nTotal de medições: {total}")
print(f"00000: {corretos}/{total} ({100 * corretos / total:.2f}%)")
print(f"Outros: {outros}/{total} ({100 * outros / total:.2f}%)")