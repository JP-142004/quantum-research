from qiskit import QuantumCircuit, transpile
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler

NUM_QUBITS = 15
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

# Carrega as credenciais IBM salvas localmente
service = QiskitRuntimeService(channel="ibm_quantum_platform")

# Seleciona o computador especificado
backend = service.backend(BACKEND_NAME)
print(f"\nBackend: {backend.name}")

# Adapta o circuito às instruções e conexões do backend
compiled = transpile(qc, backend=backend, optimization_level=1)

# Envia o circuito
sampler = Sampler(mode=backend)
job = sampler.run([compiled], shots=SHOTS)

print(f"Job enviado. ID: {job.job_id()}")
print(f"Status inicial: {job.status()}")
print("Aguardando resultado...")

job_result = job.result()
print(f"\nStatus do job: {job.status()}")

# O registrador clássico criado acima chama-se "c"
counts = job_result[0].data.c.get_counts()

# Exibe as contagens em ordem crescente e alinhadas
largura_estado = max(NUM_QUBITS, len("RESULTADO"))
linha = "-" * (largura_estado + 13)

print(f"\n{'RESULTADO':<{largura_estado}} {'CONTAGEM':>10}")
print(linha)

for estado in sorted(counts):
    print(f"{estado:<{largura_estado}} {counts[estado]:>10}")

total = sum(counts.values())
print(linha)
print(f"{'Total de medições:':<{largura_estado}} {total:>10}")

# Em um GHZ ideal, esperamos somente todos zeros ou todos uns
todos_zero = "0" * NUM_QUBITS
todos_um = "1" * NUM_QUBITS
fora_do_esperado = total - counts.get(todos_zero, 0) - counts.get(todos_um, 0)
porcentagem = 100 * fora_do_esperado / total if total else 0.0

print(
    f"\nResultados fora dos estados GHZ ideais: "
    f"{fora_do_esperado}/{total} ({porcentagem:.2f}%)"
)

