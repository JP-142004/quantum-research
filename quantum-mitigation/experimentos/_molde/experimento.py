"""Receita do experimento. Copie para NN_nome/experimento.py e edite.

Cada item é um circuito a executar. Chaves: circuito, n, variante, base ('Z' ou 'X'),
fator (ruído; 1 por padrão) e, se precisar, qubits (físicos) e raiz (qubit físico de partida).
Circuitos disponíveis: mitigacao/circuitos/. Técnicas: mitigacao/tecnicas/.
"""
from mitigacao.tecnicas import leitura, zne  # noqa: F401  (use as que o experimento precisar)

pergunta = 'Montar o GHZ com menos passos melhora o resultado?'
execucao = 'ibm'            # 'ibm' ou 'simulador'
computador = 'ibm_fez'      # padrão; pode ser trocado com --computador
shots = 1000
repeticoes = 3              # sessões previstas, em dias diferentes
raiz = 2                    # qubit físico de partida da escolha de qubits

itens = [dict(circuito='ghz', n=n, variante=v, base=b)
         for n in (5, 10, 20) for v in ('original', 'conectado') for b in ('Z', 'X')]

# Para uma técnica de leitura, acrescente: itens += leitura.itens_calibracao(5)
# Para ZNE, troque os itens por: zne.expandir(itens)
# Opções passadas ao envio (por exemplo, o cenário de ruído do simulador): opcoes_envio = dict(cenario='leitura')
