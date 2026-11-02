"""Escolha dos qubits físicos a partir das ligações do computador."""
from collections import deque


def vizinhos_de(arestas):
    """Lista de ligações (a, b) em dict qubit -> conjunto de vizinhos (nos dois sentidos)."""
    v = {}
    for a, b in arestas:
        v.setdefault(a, set()).add(b)
        v.setdefault(b, set()).add(a)
    return v


def vizinhos_linha(n):
    """Computador sintético em linha: 0-1-2-...-(n-1)."""
    vizinhos = {i: set() for i in range(n)}
    for a, b in [(i, i + 1) for i in range(n - 1)]:
        vizinhos[a].add(b)
        vizinhos[b].add(a)
    return vizinhos


def escolher_qubits(vizinhos, n, raiz):
    """Busca em largura a partir do qubit físico `raiz`, até juntar n qubits.

    Devolve (qubits físicos em ordem crescente, arestas em índices lógicos). O índice
    lógico i é o i-ésimo qubit físico em ordem crescente. A origem da primeira aresta
    é a raiz. Assim a variante original e a conectada usam exatamente os mesmos qubits.
    """
    if raiz not in vizinhos:
        raise ValueError(f'O qubit {raiz} não existe neste computador')
    escolhidos, fila, arestas = [raiz], deque([raiz]), []
    while fila and len(escolhidos) < n:
        origem = fila.popleft()
        for destino in sorted(vizinhos[origem]):
            if destino in escolhidos:
                continue
            escolhidos.append(destino)
            arestas.append((origem, destino))
            fila.append(destino)
            if len(escolhidos) == n:
                break
    if len(escolhidos) != n:
        raise RuntimeError(f'Não há {n} qubits conectados a partir do qubit {raiz}')
    fisicos = sorted(escolhidos)
    indice = {q: i for i, q in enumerate(fisicos)}
    return fisicos, [(indice[o], indice[d]) for o, d in arestas]
