"""Experimento 8, parte B: GHZ conectado de 10 e de 20 qubits na IBM, calibrado qubit a qubit.

SÓ PLANO: nada foi enviado. Veja o README. Verifique localmente com: python rodar.py 08b --verificar
O envio (--enviar) pede a confirmação do Luiz e só vale depois de ele conferir o saldo de tempo.
"""
pergunta = 'Na IBM, em 10 e 20 qubits, a calibração por qubit leva os indicadores do GHZ perto do ideal?'
execucao = 'ibm'
computador = 'ibm_fez'
shots = 1000
repeticoes = 3   # sessões, em dias diferentes
tecnicas = ['leitura']


def _calibracoes(n):
    """00…0, 11…1, 0101… e 1010… (o último símbolo é o qubit 0)."""
    return ['0' * n, '1' * n, ('01' * n)[:n], ('10' * n)[:n]]


itens = []
for n in (10, 20):
    itens += [dict(circuito='ghz', n=n, variante='conectado', base=b) for b in ('Z', 'X')]
    itens += [dict(circuito='simples', n=n, variante=v, base='Z') for v in _calibracoes(n)]
    itens += [dict(circuito='simples', n=n, variante=v, base=b, rotulo='controle')
              for v, b in (('0' * n, 'Z'), ('1' * n, 'Z'), ('+' * n, 'X'), ('+' * (n - 1) + '-', 'X'))]
