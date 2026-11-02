"""Envio e coleta na IBM. O qiskit-ibm-runtime só é importado aqui dentro, para o resto do
código e os testes funcionarem sem ele. As credenciais ficam salvas no computador de quem
envia; este código nunca as lê nem as grava."""
from qiskit import transpile
from qiskit.transpiler.exceptions import TranspilerError

from mitigacao.execucao import conferir_sem_troca, embaralhar, info_compilado
from mitigacao.topologia import vizinhos_de

INSTANTANEO = False
SEMENTE_COMPILADOR = 42
# Opções fixas em todo envio: nenhuma técnica de mitigação do serviço fica ligada sem querer.
OPCOES = dict(dd=False, twirling_gates=False, twirling_measure=False, init_qubits=True)


def _servico():
    from qiskit_ibm_runtime import QiskitRuntimeService
    return QiskitRuntimeService(channel='ibm_quantum_platform')


def backend(computador):
    return _servico().backend(computador)


def vizinhos(computador, n=None):
    return vizinhos_de(backend(computador).coupling_map.get_edges())


def compilar(montados, backend_):
    """Compila cada circuito para o computador, nos qubits escolhidos. Não envia nada."""
    compilados = {}
    for m in montados:
        try:
            qc = transpile(m['circuito'], backend=backend_, initial_layout=list(m['qubits_fisicos']),
                           routing_method=m['roteamento'], optimization_level=1, seed_transpiler=SEMENTE_COMPILADOR)
        except TranspilerError as erro:
            raise RuntimeError(f'{m["nome"]} não cabe nas ligações do computador sem trocar qubits: {erro}') from erro
        if m['roteamento'] == 'none':
            conferir_sem_troca(qc, m['qubits_fisicos'], m['nome'])
        compilados[m['nome']] = qc
    return compilados


def enviar(montados, shots, semente, computador, limite_segundos=None):
    """Compila e envia todos os circuitos em um único job. Devolve o job_id e o que foi enviado."""
    from qiskit_ibm_runtime import SamplerV2
    backend_ = backend(computador)
    if not backend_.status().operational:
        raise RuntimeError(f'{computador} está indisponível. Nada foi enviado.')
    por_nome = {m['nome']: m for m in montados}
    ordem = embaralhar(list(por_nome), semente)
    compilados = compilar([por_nome[nome] for nome in ordem], backend_)
    sampler = SamplerV2(mode=backend_)
    sampler.options.dynamical_decoupling.enable = OPCOES['dd']
    sampler.options.twirling.enable_gates = OPCOES['twirling_gates']
    sampler.options.twirling.enable_measure = OPCOES['twirling_measure']
    sampler.options.execution.init_qubits = OPCOES['init_qubits']
    if limite_segundos:
        sampler.options.max_execution_time = limite_segundos
    job = sampler.run([compilados[nome] for nome in ordem], shots=shots)
    return dict(job_id=job.job_id(), ordem=ordem, compilados=compilados,
                opcoes=dict(OPCOES, limite_segundos=limite_segundos),
                info={nome: info_compilado(qc) for nome, qc in compilados.items()})


def coletar(job):
    """job: dict com job_id e ordem (da ficha). Devolve None se o job ainda não terminou."""
    ibm_job = _servico().job(job['job_id'])
    if str(ibm_job.status()).upper() != 'DONE':
        return None
    resultado = ibm_job.result()
    if len(resultado) != len(job['ordem']):
        raise RuntimeError('Número inesperado de resultados')
    return {nome: resultado[i].data.c.get_counts() for i, nome in enumerate(job['ordem'])}
