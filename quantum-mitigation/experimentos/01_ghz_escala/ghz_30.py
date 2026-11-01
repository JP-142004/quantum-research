from qiskit import QuantumCircuit, transpile
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler

NUM_QUBITS = 30
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

# Transpila o circuito para as instruções e conexões do computador
compiled = transpile(qc, backend=backend, optimization_level=1)

sampler = Sampler(mode=backend)
job = sampler.run([compiled], shots=SHOTS)

print(f"Job enviado. ID: {job.job_id()}")
print(f"Status inicial: {job.status()}")
print("Aguardando resultado...")

resultado = job.result()[0]
contagens = resultado.data.c.get_counts()

print(f"\nContagens em {SHOTS} medições:")
for estado in sorted(contagens):
    print(f"  {estado}: {contagens[estado]}")

# Um GHZ ideal produz apenas todos zeros ou todos uns
todos_zero = "0" * NUM_QUBITS
todos_um = "1" * NUM_QUBITS

fora_do_esperado = (
    SHOTS
    - contagens.get(todos_zero, 0)
    - contagens.get(todos_um, 0)
)

print(
    f"\nResultados fora dos dois estados GHZ ideais: "
    f"{fora_do_esperado}/{SHOTS} "
    f"({100 * fora_do_esperado / SHOTS:.2f}%)"
)