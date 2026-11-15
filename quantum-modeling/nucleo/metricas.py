"""Metricas para comparar histogramas de hardware e simulacao em circuitos GHZ."""

from qiskit.quantum_info import hellinger_distance


def resumo_ghz(counts, n):
    """Indicadores que ajudam a explicar a divergencia (feedback, item 5)."""
    shots = sum(counts.values())
    p_zeros = counts.get("0" * n, 0) / shots
    p_uns = counts.get("1" * n, 0) / shots
    hamming = [0.0] * (n + 1)
    for cadeia, c in counts.items():
        hamming[cadeia.count("1")] += c / shots
    return {
        "shots": shots,
        "p_todos_zeros": p_zeros,
        "p_todos_uns": p_uns,
        "massa_ghz": p_zeros + p_uns,
        "cadeias_distintas": len(counts),
        "distribuicao_peso_hamming": hamming,
    }


def comparar(counts_real, counts_sim, n):
    """Hellinger + indicadores de cada lado + quantas cadeias aparecem nos dois."""
    return {
        "hellinger": float(hellinger_distance(counts_real, counts_sim)),
        "cadeias_em_comum": len(set(counts_real) & set(counts_sim)),
        "real": resumo_ghz(counts_real, n),
        "simulado": resumo_ghz(counts_sim, n),
    }


def erro_leitura_por_qubit(counts, n, estado):
    """Fracao de shots em que o bit i saiu diferente do estado preparado.
    O bit i e o caractere -1-i da cadeia (ordem do Qiskit)."""
    shots = sum(counts.values())
    erros = [0] * n
    for cadeia, c in counts.items():
        for i in range(n):
            if int(cadeia[-1 - i]) != estado:
                erros[i] += c
    return [e / shots for e in erros]


def comparar_leitura(counts_real, counts_sim, n, estado):
    """Circuitos que preparam tudo em 0 (ou 1) e medem: P(1|0) ou P(0|1) por qubit."""
    real = erro_leitura_por_qubit(counts_real, n, estado)
    sim = erro_leitura_por_qubit(counts_sim, n, estado)
    return {
        "hellinger": float(hellinger_distance(counts_real, counts_sim)),
        "erro_medio_real": sum(real) / n,
        "erro_medio_simulado": sum(sim) / n,
        "por_qubit_real": real,
        "por_qubit_simulado": sim,
    }


def paridade(counts):
    """Media de (-1)^(numero de uns). Para GHZ ideal vale cos(n * fase)."""
    shots = sum(counts.values())
    return sum(c * (-1) ** cadeia.count("1") for cadeia, c in counts.items()) / shots


def comparar_paridade(counts_real, counts_sim):
    return {
        "hellinger": float(hellinger_distance(counts_real, counts_sim)),
        "paridade_real": paridade(counts_real),
        "paridade_simulada": paridade(counts_sim),
    }
