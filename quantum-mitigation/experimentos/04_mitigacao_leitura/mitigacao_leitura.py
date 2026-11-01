import json
from pathlib import Path

import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler

BACKEND_NAME = "ibm_fez"
QUBITS = [0, 1, 2, 3, 4]
N = 5
DIM = 2**N
SHOTS = 1000

# Deixe vazio para enviar um novo job.
# Para recuperar um job deste script, coloque seu ID aqui.
JOB_ID = ""

service = QiskitRuntimeService(channel="ibm_quantum_platform")
backend = service.backend(BACKEND_NAME)

nomes = []
circuitos_logicos = []

# ---------------------------------------------------------
# 1. Calibrações: preparar cada resposta conhecida.
# O bit da direita corresponde ao qubit lógico 0.
# ---------------------------------------------------------
for estado in range(DIM):
    qc = QuantumCircuit(N, N)

    for q in range(N):
        if (estado >> q) & 1:
            qc.x(q)

    qc.measure(range(N), range(N))

    nomes.append(f"cal_{estado:05b}")
    circuitos_logicos.append(qc)

# ---------------------------------------------------------
# 2. GHZ conectado: mesma preparação para Z e X.
# ---------------------------------------------------------
for base in ["Z", "X"]:
    qc = QuantumCircuit(N, N)

    qc.h(2)
    qc.cx(2, 1)
    qc.cx(2, 3)
    qc.cx(1, 0)
    qc.cx(3, 4)

    qc.barrier()

    if base == "X":
        for q in range(N):
            qc.h(q)

    qc.measure(range(N), range(N))

    nomes.append(f"GHZ_{base}")
    circuitos_logicos.append(qc)

# Ordem embaralhada, mas reproduzível.
# Não garante ordem física nem simultaneidade no serviço.
ordem = np.random.default_rng(42).permutation(len(nomes))
nomes = [nomes[i] for i in ordem]
circuitos_logicos = [circuitos_logicos[i] for i in ordem]

if JOB_ID:
    job = service.job(JOB_ID)
    print(f"Recuperando job: {JOB_ID}")
else:
    compilados = []

    for nome, qc in zip(nomes, circuitos_logicos):
        compiled = transpile(
            qc,
            backend=backend,
            initial_layout=QUBITS,
            routing_method="none",
            optimization_level=1,
            seed_transpiler=42,
        )

        mapa = compiled.layout.final_index_layout(
            filter_ancillas=True
        )

        if mapa != QUBITS:
            raise RuntimeError(
                f"Mapeamento inesperado em {nome}: {mapa}. "
                "Nenhum job foi enviado."
            )

        compilados.append(compiled)

        if nome.startswith("GHZ"):
            print(f"\n{nome}")
            print(f"Profundidade: {compiled.depth()}")
            print(f"Operações: {dict(compiled.count_ops())}")
            print(f"Mapeamento final: {mapa}")

    sampler = Sampler(mode=backend)
    sampler.options.dynamical_decoupling.enable = False
    sampler.options.twirling.enable_gates = False
    sampler.options.twirling.enable_measure = False
    sampler.options.execution.init_qubits = True

    print(f"\nBackend: {backend.name}")
    print(f"Qubits: {QUBITS}")
    print("Enviando 34 circuitos, com 1.000 shots cada...")

    job = sampler.run(compilados, shots=SHOTS)

print(f"\nID do job: {job.job_id()}", flush=True)
print("Aguardando resultados...")

resultado = job.result()

if len(resultado) != len(nomes):
    raise RuntimeError("O job não corresponde aos 34 circuitos deste script.")

contagens = {
    nome: resultado[i].data.c.get_counts()
    for i, nome in enumerate(nomes)
}

# Preserva os dados brutos antes de qualquer ajuste.
pasta_dados = Path(__file__).resolve().parents[2] / "dados" / "brutos" / "04_mitigacao_leitura"
pasta_dados.mkdir(parents=True, exist_ok=True)
arquivo = pasta_dados / (
    f"GHZ_leitura_{job.job_id()}.json"
)

arquivo.write_text(
    json.dumps(
        {
            "backend": BACKEND_NAME,
            "qubits": QUBITS,
            "shots_por_circuito": SHOTS,
            "job_id": job.job_id(),
            "ordem_circuitos": nomes,
            "contagens": contagens,
        },
        indent=2,
        ensure_ascii=False,
    ),
    encoding="utf-8",
)

print(f"\nDados brutos salvos em: {arquivo}")


def vetor_counts(counts):
    vetor = np.zeros(DIM)

    for bits, quantidade in counts.items():
        vetor[int(bits, 2)] += quantidade

    return vetor


# ---------------------------------------------------------
# 3. Matriz A:
# coluna = estado preparado; linha = resultado registrado.
# ---------------------------------------------------------
calibracoes = np.column_stack([
    vetor_counts(contagens[f"cal_{estado:05b}"])
    for estado in range(DIM)
])

totais_cal = calibracoes.sum(axis=0).astype(int)
A = calibracoes / totais_cal

condicao = np.linalg.cond(A)
print(f"Condicionamento da matriz: {condicao:.2f}")

if not np.isfinite(condicao) or condicao > 100:
    raise RuntimeError(
        "Matriz de calibração instável. Os dados foram salvos, "
        "mas o ajuste não será interpretado."
    )

observados = np.column_stack([
    vetor_counts(contagens["GHZ_Z"]),
    vetor_counts(contagens["GHZ_X"]),
])

totais_ghz = observados.sum(axis=0).astype(int)
prob_brutas = observados / totais_ghz

# Resolve A @ p_ajustada = p_observada.
quasi = np.linalg.solve(A, prob_brutas)

# Indicador Z: população em 00000 e 11111.
peso_z = np.zeros(DIM)
peso_z[0] = 1
peso_z[-1] = 1

# Indicador X: paridade par menos paridade ímpar.
peso_x = np.array([
    1 if estado.bit_count() % 2 == 0 else -1
    for estado in range(DIM)
])


def indicadores(distribuicoes):
    return np.array([
        peso_z @ distribuicoes[:, 0],
        peso_x @ distribuicoes[:, 1],
    ])


bruto = indicadores(prob_brutas)
ajustado = indicadores(quasi)

# ---------------------------------------------------------
# 4. Bootstrap: incerteza de amostragem da calibração
# e dos dois circuitos GHZ.
# Não inclui deriva do hardware nem falhas do modelo.
# ---------------------------------------------------------
rng = np.random.default_rng(2026)
amostras_brutas = []
amostras_ajustadas = []

for _ in range(300):
    A_boot = np.column_stack([
        rng.multinomial(totais_cal[j], A[:, j]) / totais_cal[j]
        for j in range(DIM)
    ])

    if np.linalg.cond(A_boot) > 100:
        continue

    p_boot = np.column_stack([
        rng.multinomial(totais_ghz[j], prob_brutas[:, j])
        / totais_ghz[j]
        for j in range(2)
    ])

    q_boot = np.linalg.solve(A_boot, p_boot)

    amostras_brutas.append(indicadores(p_boot))
    amostras_ajustadas.append(indicadores(q_boot))

if len(amostras_ajustadas) < 200:
    raise RuntimeError(
        "Muitas calibrações bootstrap ficaram instáveis. "
        "Envie os dados para avaliarmos."
    )

erro_bruto = np.std(amostras_brutas, axis=0, ddof=1)
erro_ajustado = np.std(amostras_ajustadas, axis=0, ddof=1)

print("\n" + "=" * 60)
print("COMPARAÇÃO — GHZ CONECTADO")
print("± representa erro padrão estimado por bootstrap.")
print("Ideal para os dois indicadores: 1.")

rotulos = [
    "População em Z: P(00000) + P(11111)",
    "Correlação coletiva em X",
]

for i, rotulo in enumerate(rotulos):
    print(f"\n{rotulo}")
    print(f"Bruto:    {bruto[i]:.4f} ± {erro_bruto[i]:.4f}")
    print(f"Ajustado: {ajustado[i]:.4f} ± {erro_ajustado[i]:.4f}")
    print(f"Distância ao ideal, bruto:    {abs(1 - bruto[i]):.4f}")
    print(f"Distância ao ideal, ajustado: {abs(1 - ajustado[i]):.4f}")

print("\nDiagnóstico das quasiprobabilidades:")
for j, base in enumerate(["Z", "X"]):
    print(
        f"{base}: soma={quasi[:, j].sum():.6f}; "
        f"menor valor={quasi[:, j].min():.6f}"
    )

print("\nA calibração também pode incluir erros de preparação.")
print("O ajuste não elimina erros das portas ou perda de fase.")