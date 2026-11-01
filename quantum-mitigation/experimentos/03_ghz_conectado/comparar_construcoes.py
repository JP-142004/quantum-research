from collections import deque

from qiskit import QuantumCircuit, transpile
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler

BACKEND_NAME = "ibm_fez"
QUBITS = [0, 1, 2, 3, 4]
SHOTS = 1000
N = len(QUBITS)

service = QiskitRuntimeService(channel="ibm_quantum_platform")
backend = service.backend(BACKEND_NAME)

# Consulta as conexões entre os cinco qubits escolhidos.
vizinhos = {q: set() for q in QUBITS}

for a, b in backend.coupling_map.get_edges():
    if a in vizinhos and b in vizinhos:
        vizinhos[a].add(b)
        vizinhos[b].add(a)

print(f"Backend: {backend.name}")
print(f"Qubits físicos: {QUBITS}")
print("\nConexões disponíveis entre eles:")

for q in QUBITS:
    print(f"{q}: {sorted(vizinhos[q])}")

# Versão anterior: todas as CX partem do qubit lógico 0.
anterior = QuantumCircuit(N, N)
anterior.h(0)

for q in range(1, N):
    anterior.cx(0, q)

anterior.measure(range(N), range(N))

compilado_anterior = transpile(
    anterior,
    backend=backend,
    initial_layout=QUBITS,
    optimization_level=1,
    seed_transpiler=42,
)


def criar_ghz_conectado(raiz):
    """Espalha o GHZ apenas por conexões físicas diretas."""
    visitados = {raiz}
    fila = deque([raiz])
    arestas = []

    while fila:
        origem = fila.popleft()

        for destino in sorted(vizinhos[origem]):
            if destino not in visitados:
                visitados.add(destino)
                fila.append(destino)
                arestas.append((origem, destino))

    if len(visitados) != N:
        raise RuntimeError(
            "Os cinco qubits não formam um conjunto conectado. "
            "Nenhum job foi enviado."
        )

    circuito = QuantumCircuit(N, N)
    circuito.h(QUBITS.index(raiz))

    for origem, destino in arestas:
        circuito.cx(
            QUBITS.index(origem),
            QUBITS.index(destino),
        )

    circuito.measure(range(N), range(N))
    return circuito, arestas


def contar_portas_duplas(circuito):
    return sum(
        1
        for instrucao in circuito.data
        if instrucao.operation.num_qubits == 2
    )


# Testa diferentes raízes apenas no compilador local.
# Escolhe menos portas de dois qubits e depois menor profundidade.
candidatos = []

for raiz in QUBITS:
    circuito, arestas = criar_ghz_conectado(raiz)

    compilado = transpile(
        circuito,
        backend=backend,
        initial_layout=QUBITS,
        routing_method="none",
        optimization_level=1,
        seed_transpiler=42,
    )

    candidatos.append(
        (
            contar_portas_duplas(compilado),
            compilado.depth(),
            raiz,
            circuito,
            compilado,
            arestas,
        )
    )

melhor = min(candidatos, key=lambda item: (item[0], item[1]))
_, _, raiz, novo, compilado_novo, arestas = melhor

print(f"\nRaiz escolhida para a nova construção: {raiz}")
print(f"Conexões utilizadas: {arestas}")
print("\nNovo circuito lógico:")
print(novo.draw())

nomes = ["GHZ anterior", "GHZ seguindo as conexões"]
circuitos = [compilado_anterior, compilado_novo]

for nome, circuito in zip(nomes, circuitos):
    print(f"\n{nome}")
    print(f"Profundidade: {circuito.depth()}")
    print(f"Portas de dois qubits: {contar_portas_duplas(circuito)}")
    print(f"Operações: {dict(circuito.count_ops())}")
    print(
        "Mapeamento final:",
        circuito.layout.final_index_layout(filter_ancillas=True),
    )

sampler = Sampler(mode=backend)
sampler.options.dynamical_decoupling.enable = False
sampler.options.twirling.enable_gates = False
sampler.options.twirling.enable_measure = False
sampler.options.execution.init_qubits = True

# Apenas duas execuções na IBM: 1.000 shots por versão.
job = sampler.run(circuitos, shots=SHOTS)

print(f"\nID do job: {job.job_id()}", flush=True)
print("Aguardando resultados...")

resultado = job.result()

for indice, nome in enumerate(nomes):
    counts = resultado[indice].data.c.get_counts()
    total = sum(counts.values())
    zeros = counts.get("00000", 0)
    uns = counts.get("11111", 0)
    outros = total - zeros - uns

    print("\n" + "=" * 50)
    print(nome)

    for estado, quantidade in sorted(counts.items()):
        print(f"{estado}: {quantidade}")

    print(f"\nTotal: {total}")
    print(f"00000: {zeros} ({100 * zeros / total:.2f}%)")
    print(f"11111: {uns} ({100 * uns / total:.2f}%)")
    print(f"Outros: {outros} ({100 * outros / total:.2f}%)")
    print(
        "População nos dois resultados esperados: "
        f"{100 * (zeros + uns) / total:.2f}%"
    )