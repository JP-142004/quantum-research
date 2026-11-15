"""Circuitos logicos dos lotes (antes da transpilacao). Descricao em circuitos/README.md.
Todos usam um registrador classico chamado "c", com o bit i medindo o qubit i."""

import math
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister


def _vazio(n):
    return QuantumCircuit(QuantumRegister(n, "q"), ClassicalRegister(n, "c"))


def _medir(qc):
    qc.barrier()  # impede o transpilador de simplificar o que vem antes da medida
    qc.measure(range(qc.num_qubits), range(qc.num_qubits))
    return qc


def ghz(n, medir=True):
    qc = _vazio(n)
    qc.h(0)
    for i in range(n - 1):
        qc.cx(i, i + 1)
    return _medir(qc) if medir else qc


def leitura(n, estado):
    """Prepara todos os qubits em |0> (estado=0) ou |1> (estado=1) e mede."""
    qc = _vazio(n)
    if estado == 1:
        qc.x(range(n))
    return _medir(qc)


def paridade(n, fase):
    """GHZ + medida de cada qubit na base cos(fase) X + sin(fase) Y.
    A paridade ideal vale cos(n * fase); so oscila se o estado for coerente."""
    qc = ghz(n, medir=False)
    for i in range(n):
        qc.rz(-fase, i)
        qc.h(i)
    return _medir(qc)


def montar_lote(cfg):
    """Lista de (descricao, circuito logico) na ordem em que vao no job."""
    n_max = max(cfg["tamanhos_ghz"])
    itens = []
    if cfg.get("leitura"):
        for estado in (0, 1):
            itens.append(({"nome": f"leitura{estado}_n{n_max:02d}", "tipo": "leitura",
                           "n": n_max, "estado": estado}, leitura(n_max, estado)))
    for n in cfg["tamanhos_ghz"]:
        itens.append(({"nome": f"ghz_n{n:02d}", "tipo": "ghz", "n": n}, ghz(n)))
    par = cfg.get("paridade")
    if par:
        for n in par["tamanhos"]:
            for k in range(par["n_fases"]):
                fase = k * 2 * math.pi / (n * par["n_fases"])
                itens.append(({"nome": f"paridade_n{n:02d}_f{k}", "tipo": "paridade", "n": n,
                               "fase": fase, "paridade_ideal": math.cos(n * fase)},
                              paridade(n, fase)))
    return itens
