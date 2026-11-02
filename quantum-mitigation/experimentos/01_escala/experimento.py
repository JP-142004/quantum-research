"""Experimento 1: como o erro cresce de 5 a 50 qubits? GHZ original, medido em Z, sem técnica."""
pergunta = 'Como o erro cresce de 5 a 50 qubits?'
execucao = 'ibm'
computador = 'ibm_fez'
shots = 1000
repeticoes = 3   # sessões, em dias diferentes
raiz = 2         # qubit físico de partida da escolha de qubits (tamanhos acima de 5)

Q5 = [0, 1, 2, 3, 4]

# Com 5 qubits, os qubits 0 a 4, como nos outros experimentos. Os maiores partem do qubit 2.
itens = [dict(circuito='ghz', n=n, variante='original', base='Z', regiao=Q5 if n == 5 else None)
         for n in range(5, 51, 5)]
