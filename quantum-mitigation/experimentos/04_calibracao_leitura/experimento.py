"""Experimento 4: a calibração de leitura aproxima os indicadores do ideal?

GHZ conectado de 5 qubits em Z e em X, as 32 calibrações e 4 controles independentes
(amostras novas, sem reaproveitar as contagens da calibração).
"""
from mitigacao.tecnicas import leitura

pergunta = 'A calibração de leitura aproxima os indicadores do ideal?'
execucao = 'ibm'
computador = 'ibm_fez'
shots = 1000
repeticoes = 3   # sessões, em dias diferentes
tecnicas = ['leitura']   # o que a análise aplica

Q5 = [0, 1, 2, 3, 4]

itens = [dict(circuito='ghz', n=5, variante='conectado', base=b, regiao=Q5) for b in ('Z', 'X')]
itens += leitura.itens_calibracao(5, qubits=Q5)
# zeros e uns em Z; os estados +++++ e ++++- (qubit 0 em |->) em X, com resposta 00000 e 00001
itens += [dict(circuito='simples', n=5, variante=v, base=b, qubits=Q5, rotulo='controle')
          for v, b in (('00000', 'Z'), ('11111', 'Z'), ('+++++', 'X'), ('++++-', 'X'))]
