from qiskit import QuantumCircuit, transpile
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler

NUM_QUBITS = 5
SHOTS = 1000
BACKEND_NAME = "ibm_fez"
QUBITS_FISICOS = [0, 1, 2, 3, 4]

# Prepara o GHZ de 5 qubits.
qc = QuantumCircuit(NUM_QUBITS, NUM_QUBITS)
qc.h(0)

for qubit in range(1, NUM_QUBITS):
    qc.cx(0, qubit)

qc.measure(range(NUM_QUBITS), range(NUM_QUBITS))

print("Circuito GHZ de 5 qubits:")
print(qc.draw())

service = QiskitRuntimeService(channel="ibm_quantum_platform")
backend = service.backend(BACKEND_NAME)

compiled = transpile(
    qc,
    backend=backend,
    initial_layout=QUBITS_FISICOS,
    optimization_level=1,
    seed_transpiler=42,
)

print(f"\nBackend: {backend.name}")
print(f"Mapeamento inicial: {QUBITS_FISICOS}")
print(f"Profundidade compilada: {compiled.depth()}")
print(f"Operações compiladas: {dict(compiled.count_ops())}")

# O compilador pode mover estados para executar as CX.
# Registra onde cada qubit lógico termina.
mapa_final = compiled.layout.final_index_layout(
    filter_ancillas=True
)
print(f"Mapeamento final: {mapa_final}")

sampler = Sampler(mode=backend)
sampler.options.dynamical_decoupling.enable = False
sampler.options.twirling.enable_gates = False
sampler.options.twirling.enable_measure = False
sampler.options.execution.init_qubits = True

job = sampler.run([compiled], shots=SHOTS)

print(f"\nJob enviado. ID: {job.job_id()}", flush=True)
print("Aguardando resultado...")

resultado = job.result()
counts = resultado[0].data.c.get_counts()

print(f"\nStatus: {job.status()}")
print("\nRESULTADO    CONTAGEM")
print("---------------------")

for estado, quantidade in sorted(counts.items()):
    print(f"{estado:<12} {quantidade:>7}")

total = sum(counts.values())
zeros = counts.get("00000", 0)
uns = counts.get("11111", 0)
outros = total - zeros - uns

print(f"\nTotal: {total}")
print(f"00000: {zeros} ({100 * zeros / total:.2f}%)")
print(f"11111: {uns} ({100 * uns / total:.2f}%)")
print(f"Outros: {outros} ({100 * outros / total:.2f}%)")
print(
    "População nos dois resultados esperados: "
    f"{100 * (zeros + uns) / total:.2f}%"
)