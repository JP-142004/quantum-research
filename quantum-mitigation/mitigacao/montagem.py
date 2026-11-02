"""Da receita ao que vai ser executado: escolhe os qubits e constrói cada circuito."""
import numpy as np
from qiskit.quantum_info import Statevector

from mitigacao.circuitos import completar, construir, nome_item, prob_ideal_item
from mitigacao.topologia import escolher_qubits

LIMITE_VERIFICACAO_IDEAL = 20  # acima disso o vetor de estado fica grande demais


def montar(itens, vizinhos, raiz=2):
    """Devolve uma lista de dicts: nome, item, circuito, qubits_fisicos, arestas, roteamento.

    vizinhos: dict qubit -> conjunto de vizinhos, ou função n -> dict (computador sintético).
    A variante original e a conectada de mesmo n usam os mesmos qubits físicos. A conectada
    é compilada sem roteamento: nenhuma troca de qubits é aceita.
    """
    montados, vistos = [], set()
    for bruto in itens:
        item = completar(bruto)
        nome = nome_item(item)
        if nome in vistos:
            raise ValueError(f'Item repetido: {nome}')
        vistos.add(nome)
        n, arestas = item['n'], None
        if item['qubits'] is not None:
            fisicos = list(item['qubits'])
            if len(fisicos) != n:
                raise ValueError(f'{nome}: precisa de {n} qubits explícitos')
        else:
            mapa = vizinhos(n) if callable(vizinhos) else vizinhos
            raiz_item = item['raiz'] if item['raiz'] is not None else raiz
            if callable(vizinhos):
                raiz_item = min(raiz_item, n - 1)  # na linha sintética de n qubits, a raiz cabe na linha
            fisicos, arestas = escolher_qubits(mapa, n, raiz_item)
        conectado = item['variante'] == 'conectado'
        if conectado and arestas is None:
            raise ValueError(f'{nome}: a variante conectado não aceita qubits explícitos')
        montados.append(dict(nome=nome, item=item, circuito=construir(item, arestas if conectado else None),
                             qubits_fisicos=fisicos, arestas=arestas,
                             roteamento='none' if conectado else None))
    return montados


def verificar_ideal(montado, tolerancia=1e-9):
    """Confere o circuito contra a distribuição ideal declarada. None se n for grande demais."""
    n = montado['item']['n']
    if n > LIMITE_VERIFICACAO_IDEAL:
        return None
    sv = Statevector.from_instruction(montado['circuito'].remove_final_measurements(inplace=False))
    probs = sv.probabilities()
    indices = np.nonzero(probs > 1e-12)[0]  # só as sequências que o circuito realmente produz
    ideal = prob_ideal_item(montado['item'])
    declaradas = [ideal(f'{i:0{n}b}') for i in indices]
    # Se a soma ideal sobre essas sequências é 1, nenhuma sequência ideal ficou de fora.
    return bool(abs(sum(declaradas) - 1) < tolerancia
                and np.allclose(probs[indices], declaradas, atol=tolerancia, rtol=0))
