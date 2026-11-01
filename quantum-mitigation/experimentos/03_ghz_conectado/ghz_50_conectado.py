from collections import deque
from pathlib import Path
import json

from qiskit import QuantumCircuit, transpile
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler

NUM_QUBITS = 50
SHOTS = 1000
BACKEND_NAME = "ibm_fez"
RAIZ_FISICA = 2

# Carrega as credenciais já salvas.
service = QiskitRuntimeService(channel="ibm_quantum_platform")
backend = service.backend(BACKEND_NAME)

# Consulta as conexões físicas.
vizinhos = {q: set() for q in range(backend.num_qubits)}

for a, b in backend.coupling_map.get_edges():
    vizinhos[a].add(b)
    vizinhos[b].add(a)

# Seleciona 50 qubits conectados a partir da raiz.
# Cada novo qubit será ligado a um que já participa do GHZ.
selecionados = [RAIZ_FISICA]
visitados = {RAIZ_FISICA}
fila = deque([RAIZ_FISICA])
conexoes = []

while fila and len(selecionados) < NUM_QUBITS:
    origem = fila.popleft()

    for destino in sorted(vizinhos[origem]):
        if destino in visitados:
            continue

        visitados.add(destino)
        selecionados.append(destino)
        conexoes.append((origem, destino))
        fila.append(destino)

        if len(selecionados) == NUM_QUBITS:
            break

if len(selecionados) != NUM_QUBITS:
    raise RuntimeError(
        "Não foi possível selecionar 50 qubits conectados. "
        "Nenhum job foi enviado."
    )

# Relaciona os qubits físicos aos índices lógicos do circuito.
indice_logico = {
    fisico: logico
    for logico, fisico in enumerate(selecionados)
}

# Prepara o GHZ conectado.
qc = QuantumCircuit(NUM_QUBITS, NUM_QUBITS)
qc.h(0)

for origem, destino in conexoes:
    qc.cx(indice_logico[origem], indice_logico[destino])

# Medição em Z: sem H adicionais antes das medidas.
qc.measure(range(NUM_QUBITS), range(NUM_QUBITS))

# Impede o roteamento por SWAP.
# As interações solicitadas já seguem conexões diretas.
compiled = transpile(
    qc,
    backend=backend,
    initial_layout=selecionados,
    routing_method="none",
    optimization_level=1,
    seed_transpiler=42,
)

mapa_final = compiled.layout.final_index_layout(
    filter_ancillas=True
)

portas_duplas = sum(
    1
    for instrucao in compiled.data
    if instrucao.operation.num_qubits == 2
)

print(f"\nBackend: {backend.name}")
print(f"Quantidade de qubits: {NUM_QUBITS}")
print(f"Mapeamento inicial: {selecionados}")
print(f"Mapeamento final: {mapa_final}")
print(f"Conexões físicas utilizadas: {conexoes}")
print(f"CX no circuito lógico: {len(conexoes)}")
print(f"Portas de dois qubits após compilar: {portas_duplas}")
print(f"Profundidade compilada: {compiled.depth()}")
print(f"Operações compiladas: {dict(compiled.count_ops())}")

sampler = Sampler(mode=backend)

# Mantém as configurações dos testes anteriores.
sampler.options.dynamical_decoupling.enable = False
sampler.options.twirling.enable_gates = False
sampler.options.twirling.enable_measure = False
sampler.options.execution.init_qubits = True

job = sampler.run([compiled], shots=SHOTS)

print(f"\nJob enviado. ID: {job.job_id()}", flush=True)
print("Aguardando resultado...")

resultado = job.result()
counts = resultado[0].data.c.get_counts()

total = sum(counts.values())
todos_zero = "0" * NUM_QUBITS
todos_um = "1" * NUM_QUBITS

zeros = counts.get(todos_zero, 0)
uns = counts.get(todos_um, 0)
outros = total - zeros - uns
pz = (zeros + uns) / total

# Salva os resultados e o contexto da execução.
pasta_dados = Path(__file__).resolve().parents[2] / "dados" / "brutos" / "03_ghz_conectado"
pasta_dados.mkdir(parents=True, exist_ok=True)
arquivo = pasta_dados / (
    f"GHZ50_conectado_{job.job_id()}.json"
)

arquivo.write_text(
    json.dumps(
        {
            "backend": backend.name,
            "job_id": job.job_id(),
            "num_qubits": NUM_QUBITS,
            "shots": total,
            "base_medida": "Z",
            "mapa_inicial": selecionados,
            "mapa_final": mapa_final,
            "conexoes": conexoes,
            "profundidade": compiled.depth(),
            "operacoes": dict(compiled.count_ops()),
            "contagens": counts,
            "PZ": pz,
        },
        indent=2,
        ensure_ascii=False,
    ),
    encoding="utf-8",
)

print(f"\nStatus: {job.status()}")
print("\nRESULTADO" + " " * 45 + "CONTAGEM")
print("-" * 65)

for estado, quantidade in sorted(counts.items()):
    print(f"{estado} {quantidade:>10}")

print(f"\nTotal: {total}")
print(f"Todos zeros: {zeros} ({100 * zeros / total:.2f}%)")
print(f"Todos uns: {uns} ({100 * uns / total:.2f}%)")
print(f"Outros: {outros} ({100 * outros / total:.2f}%)")
print(f"PZ: {pz:.4f} ({100 * pz:.2f}%)")
print(f"\nDados salvos em: {arquivo}")