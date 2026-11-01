from qiskit import QuantumCircuit, transpile
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler

BACKEND_NAME = "ibm_fez"
SHOTS = 1000

service = QiskitRuntimeService(channel="ibm_quantum_platform")
backend = service.backend(BACKEND_NAME)

print(f"Backend: {backend.name}")

circuitos = []
testes = []

# Cria quatro circuitos independentes.
for qubit_fisico in [0, 1]:
    for estado_preparado in [0, 1]:
        qc = QuantumCircuit(1, 1)

        # Para preparar 0, não adicionamos porta.
        # Para preparar 1, aplicamos X.
        if estado_preparado == 1:
            qc.x(0)

        qc.measure(0, 0)

        compiled = transpile(
            qc,
            backend=backend,
            initial_layout=[qubit_fisico],
            optimization_level=1,
        )

        circuitos.append(compiled)
        testes.append((qubit_fisico, estado_preparado))

        print(
            f"\nTeste: qubit físico {qubit_fisico}, "
            f"preparado em {estado_preparado}"
        )
        print(qc.draw())

sampler = Sampler(mode=backend)

# Mesmas configurações dos dois controles anteriores.
sampler.options.dynamical_decoupling.enable = False
sampler.options.twirling.enable_gates = False
sampler.options.twirling.enable_measure = False
sampler.options.execution.init_qubits = True

# Envia os quatro circuitos em um único job.
# São 1.000 medições POR circuito: 4.000 ao todo.
job = sampler.run(circuitos, shots=SHOTS)

print(f"\nJob enviado. ID: {job.job_id()}", flush=True)
print("Aguardando os quatro resultados...")

resultado = job.result()

print(f"\nStatus: {job.status()}")

resumo = []

for indice, (qubit_fisico, estado_preparado) in enumerate(testes):
    counts = resultado[indice].data.c.get_counts()

    total = sum(counts.values())
    esperado = str(estado_preparado)
    acertos = counts.get(esperado, 0)
    desvios = total - acertos
    percentual = 100 * desvios / total

    print("\n" + "=" * 45)
    print(f"Qubit físico: {qubit_fisico}")
    print(f"Estado preparado: {estado_preparado}")
    print(f"Resultado ideal: sempre {esperado}")
    print("-" * 45)
    print(f"Resultado 0: {counts.get('0', 0)}")
    print(f"Resultado 1: {counts.get('1', 0)}")
    print(f"Total: {total}")
    print(f"Desvios: {desvios}/{total} ({percentual:.2f}%)")

    resumo.append(
        (qubit_fisico, estado_preparado, acertos, desvios, percentual)
    )

print("\nRESUMO")
print("Qubit | Preparado | Acertos | Desvios | % desvios")
print("-" * 52)

for qubit, estado, acertos, desvios, percentual in resumo:
    print(
        f"{qubit:>5} | {estado:>9} | {acertos:>7} | "
        f"{desvios:>7} | {percentual:>8.2f}%"
    )