"""Experimento 2: o computador acerta o que é fácil? Estados simples, sem técnica."""
pergunta = 'O computador acerta o que é fácil?'
execucao = 'ibm'
computador = 'ibm_fez'
shots = 1000
repeticoes = 3   # sessões, em dias diferentes

Q5 = [0, 1, 2, 3, 4]

# Cinco qubits parados em 00000 e em 11111, e cada qubit sozinho, pedido em 0 e em 1.
itens = [dict(circuito='simples', n=5, variante=v, qubits=Q5) for v in ('00000', '11111')]
itens += [dict(circuito='simples', n=1, variante=v, qubits=[q]) for q in Q5 for v in ('0', '1')]
