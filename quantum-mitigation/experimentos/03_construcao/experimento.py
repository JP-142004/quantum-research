"""Experimento 3: montar o GHZ com menos passos melhora o resultado? Original e conectado."""
pergunta = 'Montar o GHZ com menos passos melhora o resultado?'
execucao = 'ibm'
computador = 'ibm_fez'
shots = 1000
repeticoes = 3   # sessões, em dias diferentes
raiz = 2         # qubit físico de partida da escolha de qubits (tamanhos acima de 5)

Q5 = [0, 1, 2, 3, 4]

# As duas construções nos mesmos qubits, medidas em Z e em X, no mesmo job.
itens = [dict(circuito='ghz', n=n, variante=v, base=b, regiao=Q5 if n == 5 else None)
         for n in (5, 10, 20) for v in ('original', 'conectado') for b in ('Z', 'X')]
