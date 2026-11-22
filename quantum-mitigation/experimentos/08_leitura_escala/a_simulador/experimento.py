"""Experimento 8, parte A: a calibração por qubit em 10 qubits, no simulador, com erro de leitura conhecido.

Dois cenários, três blocos cada (cada bloco é uma sessão, com a sua calibração e a sua semente):
`leitura` (cada qubit erra sozinho) e `leitura_correlacionada` (além disso, os qubits de cada par
(0,1), (2,3), ... também erram juntos). Sem erro de portas: o valor verdadeiro dos indicadores é 1.
Rode tudo com: python rodar.py 08a --enviar --todas
"""
from mitigacao.execucao.ruido import CORRELACIONADO
from mitigacao.tecnicas import leitura

pergunta = 'Em 10 qubits, a calibração por qubit reproduz a da matriz completa, com erro de leitura conhecido?'
execucao = 'simulador'
computador = 'simulador'
shots = 1000
tecnicas = ['leitura']   # o que a análise aplica

N = 10
Q = list(range(N))

itens = [dict(circuito='ghz', n=N, variante='conectado', base=b, regiao=Q) for b in ('Z', 'X')]
itens += leitura.itens_calibracao(N, qubits=Q)
# zeros e uns em Z; todos em + e todos em + com o qubit 0 em - em X (respostas 0000000000 e 0000000001)
itens += [dict(circuito='simples', n=N, variante=v, base=b, qubits=Q, rotulo='controle')
          for v, b in (('0' * N, 'Z'), ('1' * N, 'Z'), ('+' * N, 'X'), ('+' * (N - 1) + '-', 'X'))]

CENARIOS_A = ('leitura', CORRELACIONADO)
sessoes = [dict(nome=f'{cenario}_bloco_{bloco:02d}', semente=8000 + 100 * i + bloco,
                opcoes_envio=dict(cenario=cenario))
           for i, cenario in enumerate(CENARIOS_A) for bloco in (1, 2, 3)]
repeticoes = len(sessoes)
