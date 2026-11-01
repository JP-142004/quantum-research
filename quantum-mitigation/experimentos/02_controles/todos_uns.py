from qiskit import QuantumCircuit, transpile
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler

NUM_QUBITS = 5
SHOTS = 1000
BACKEND_NAME = "ibm_kingston"
QUBITS_FISICOS = [0, 1, 2, 3, 4]

# Prepara todos os cinco qubits em 1.
# Resultado ideal: 11111 em todas as medições.
qc = QuantumCircuit(NUM_QUBITS, NUM_QUBITS)

for qubit in range(NUM_QUBITS):
    qc.x(qubit)

qc.measure(range(NUM_QUBITS), range(NUM_QUBITS))

print("Circuito de teste — todos uns:")
print(qc.draw())

# Carrega as credenciais IBM salvas no computador.
service = QiskitRuntimeService(channel="ibm_quantum_platform")

# Seleciona exatamente o ibm_kingston.
backend = service.backend(BACKEND_NAME)
print(f"\nBackend: {backend.name}")
print(f"Qubits físicos: {QUBITS_FISICOS}")

# Mantém o mesmo mapeamento do teste todos zeros.
compiled = transpile(
    qc,
    backend=backend,
    initial_layout=QUBITS_FISICOS,
    optimization_level=1,
)

sampler = Sampler(mode=backend)

# Mesmas configurações do teste todos zeros.
sampler.options.dynamical_decoupling.enable = False
sampler.options.twirling.enable_gates = False
sampler.options.twirling.enable_measure = False
sampler.options.execution.init_qubits = True

# Envia uma execução com 1.000 medições.
job = sampler.run([compiled], shots=SHOTS)

print(f"\nJob enviado. ID: {job.job_id()}", flush=True)
print("Aguardando resultado...")

job_result = job.result()
counts = job_result[0].data.c.get_counts()

print(f"\nStatus do job: {job.status()}")
print("\nRESULTADO    CONTAGEM")
print("---------------------")

for estado in sorted(counts):
    print(f"{estado:<12} {counts[estado]:>7}")

total = sum(counts.values())
corretos = counts.get("11111", 0)
outros = total - corretos

print(f"\nTotal de medições: {total}")
print(f"11111: {corretos}/{total} ({100 * corretos / total:.2f}%)")
print(f"Outros: {outros}/{total} ({100 * outros / total:.2f}%)")