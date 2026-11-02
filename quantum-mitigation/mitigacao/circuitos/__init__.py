"""Registro de circuitos.

Cada módulo desta pasta define um circuito com a mesma interface:

  NOME          nome curto, igual ao do arquivo
  VARIANTES     texto que descreve as variantes aceitas
  preparacao(n, variante, arestas) -> QuantumCircuit sem medida
  prob_ideal(bits, n, base, variante) -> probabilidade ideal de uma sequência de bits
  INDICADORES   dict nome -> dict(base, peso, tipo, ideal); pode ser vazio
  EXEMPLOS      lista de (n, variante); os testes percorrem todas, sem escrever teste novo

Um item de experimento é um dict com as chaves circuito, n, variante, base, fator e,
opcionalmente, qubits (qubits físicos explícitos) e raiz (qubit físico de partida).
"""
import importlib
import pkgutil

from qiskit import QuantumCircuit


def listar():
    return sorted(m.name for m in pkgutil.iter_modules(__path__))


def obter(nome):
    return importlib.import_module(f'{__name__}.{nome}')


def completar(item):
    """Preenche os valores padrão de um item."""
    completo = dict(variante='padrao', base='Z', fator=1, qubits=None, raiz=None)
    completo.update(item)
    if completo['base'] not in ('Z', 'X'):
        raise ValueError('A base deve ser Z ou X')
    if completo['fator'] < 1 or completo['fator'] % 2 == 0:
        raise ValueError('O fator de ruído deve ser ímpar: 1, 3, 5...')
    return completo


def nome_item(item):
    """Nome único e legível de um item, usado como chave nos dados."""
    i = completar(item)
    nome = f"{i['circuito']}_{i['n']}q_{i['variante']}_{i['base']}"
    if i['fator'] != 1:
        nome += f"_f{i['fator']}"
    if i['qubits'] is not None:
        nome += '_q' + '-'.join(str(q) for q in i['qubits'])
    return nome


def construir(item, arestas=None):
    """Circuito completo: preparação (repetida como U, U inverso, U para fator > 1),
    mudança de base e medida. O bit clássico i guarda o qubit lógico i."""
    i = completar(item)
    n = i['n']
    u = obter(i['circuito']).preparacao(n, i['variante'], arestas)
    qc = QuantumCircuit(n, n)
    qc.compose(u, inplace=True)
    for _ in range((i['fator'] - 1) // 2):
        qc.barrier()
        qc.compose(u.inverse(), inplace=True)
        qc.barrier()
        qc.compose(u, inplace=True)
    qc.barrier()
    if i['base'] == 'X':
        qc.h(range(n))
    qc.measure(range(n), range(n))
    return qc


def prob_ideal_item(item):
    """Função bits -> probabilidade ideal para o item."""
    i = completar(item)
    modulo = obter(i['circuito'])
    return lambda bits: modulo.prob_ideal(bits, i['n'], i['base'], i['variante'])
