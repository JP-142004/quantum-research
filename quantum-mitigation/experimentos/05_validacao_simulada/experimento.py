"""Experimento 5: o que a calibração recupera quando o erro é conhecido? Simulador.

Três cenários (ideal, só leitura, leitura e portas), três blocos cada. Cada bloco é uma
sessão com a sua calibração e a sua semente. Rode tudo com: python rodar.py 05 --enviar --todas
"""
from mitigacao.execucao.ruido import CENARIOS
from mitigacao.tecnicas import leitura

pergunta = 'O que a calibração recupera quando o erro é conhecido?'
execucao = 'simulador'
computador = 'simulador'
shots = 1000

Q5 = [0, 1, 2, 3, 4]

itens = [dict(circuito='ghz', n=5, variante=v, base=b, regiao=Q5) for v in ('original', 'conectado') for b in ('Z', 'X')]
itens += leitura.itens_calibracao(5, qubits=Q5)
itens += [dict(circuito='simples', n=5, variante=v, base=b, qubits=Q5, rotulo='controle')
          for v, b in (('00000', 'Z'), ('11111', 'Z'), ('+++++', 'X'), ('++++-', 'X'))]

sessoes = [dict(nome=f'{cenario}_bloco_{bloco:02d}', semente=5000 + 100 * i + bloco,
                opcoes_envio=dict(cenario=cenario))
           for i, cenario in enumerate(CENARIOS) for bloco in (1, 2, 3)]
repeticoes = len(sessoes)
