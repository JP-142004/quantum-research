"""Execução dos circuitos: simulador local (simulador.py) e IBM (ibm.py).

Os dois módulos têm a mesma interface, então um experimento roda em qualquer um:

  INSTANTANEO                   True se o resultado já fica pronto ao enviar
  vizinhos(computador, n)       ligações do computador: dict qubit -> conjunto de vizinhos
  enviar(montados, shots, semente, computador)
        -> dict com job_id, ordem (nomes na ordem enviada), compilados e, se
           INSTANTANEO, contagens
  coletar(job)                  -> {nome: {bits: vezes}} ou None se ainda não terminou

`montados` é a lista que mitigacao.montagem.montar devolve.
"""
import numpy as np


def info_compilado(qc):
    """Números do circuito compilado que entram na ficha da sessão."""
    medidas = [(qc.find_bit(i.qubits[0]).index, qc.find_bit(i.clbits[0]).index)
               for i in qc.data if i.operation.name == 'measure']
    portas_2q = sum(1 for i in qc.data if i.operation.num_qubits == 2 and i.operation.name != 'barrier')
    return dict(profundidade=qc.depth(), operacoes=dict(qc.count_ops()), portas_2q=portas_2q,
                mapa_medidas=sorted(medidas))


def embaralhar(nomes, semente):
    """Ordem reprodutível de envio. Não garante a ordem física no serviço."""
    return [nomes[i] for i in np.random.default_rng(semente).permutation(len(nomes))]


def conferir_sem_troca(qc, qubits_fisicos, nome):
    """Circuito conectado compilado sem roteamento: nenhum qubit pode ter trocado de lugar."""
    if qc.layout.final_index_layout(filter_ancillas=True) != list(qubits_fisicos):
        raise RuntimeError(f'O compilador trocou qubits de lugar em {nome}. Nada foi enviado.')
