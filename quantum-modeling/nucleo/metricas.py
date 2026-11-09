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
