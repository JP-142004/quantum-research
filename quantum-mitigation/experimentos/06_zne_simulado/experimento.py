"""Experimento 6: a extrapolação a ruído zero reduz o erro das portas? Simulador.

GHZ conectado nos fatores de ruído 1, 3 e 5, mais calibração e controles, no cenário de
leitura e portas. Três blocos. Rode tudo com: python rodar.py 06 --enviar --todas
"""
from mitigacao.tecnicas import leitura, zne

pergunta = 'A extrapolação a ruído zero reduz o erro das portas?'
execucao = 'simulador'
computador = 'simulador'
shots = 1000
tecnicas = ['leitura', 'zne']   # o que a análise aplica

Q5 = [0, 1, 2, 3, 4]

ghz = [dict(circuito='ghz', n=5, variante='conectado', base=b, regiao=Q5) for b in ('Z', 'X')]
itens = zne.expandir(ghz)
itens += leitura.itens_calibracao(5, qubits=Q5)
itens += [dict(circuito='simples', n=5, variante=v, base=b, qubits=Q5, rotulo='controle')
          for v, b in (('00000', 'Z'), ('11111', 'Z'), ('+++++', 'X'), ('++++-', 'X'))]

sessoes = [dict(nome=f'bloco_{bloco:02d}', semente=6000 + bloco, opcoes_envio=dict(cenario='leitura_e_portas'))
           for bloco in (1, 2, 3)]
repeticoes = len(sessoes)
