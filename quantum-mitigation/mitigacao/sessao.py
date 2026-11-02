"""Uma sessão: monta os circuitos da receita, confere, envia (ou simula) e grava os dados."""
import platform
from datetime import date

from mitigacao import registro
from mitigacao.execucao import ibm, simulador
from mitigacao.montagem import montar, verificar_ideal
from mitigacao.topologia import vizinhos_linha

MODULOS = {'ibm': ibm, 'simulador': simulador}


def montar_receita(receita, computador, online=True):
    """online=False (só para IBM): usa uma linha sintética em vez de consultar o computador real."""
    modulo = MODULOS[receita.execucao]
    if receita.execucao == 'simulador':
        vizinhos = lambda n: modulo.vizinhos(computador, n)  # noqa: E731
    elif online:
        vizinhos = modulo.vizinhos(computador)
    else:
        vizinhos = vizinhos_linha
    return montar(receita.itens, vizinhos, getattr(receita, 'raiz', 2))


def nome_padrao(computador):
    return f'{date.today():%Y-%m-%d}_{computador}'


def preparar(pasta_exp, receita, computador, nome):
    """Confere tudo antes de enviar. Devolve (pasta da sessão, circuitos montados)."""
    pasta = pasta_exp / 'dados' / nome
    if pasta.exists():
        raise RuntimeError(f'A sessão {nome} já existe. Nada foi enviado.')
    montados = montar_receita(receita, computador)
    if any(verificar_ideal(m) is False for m in montados):
        raise RuntimeError('Algum circuito não bate com o resultado ideal. Nada foi enviado.')
    return pasta, montados


def enviar_e_gravar(pasta, pasta_exp, receita, montados, computador, semente, opcoes_envio):
    modulo = MODULOS[receita.execucao]
    shots = getattr(receita, 'shots', 1000)
    job = modulo.enviar(montados, shots, semente, computador, **opcoes_envio)
    print(f'Job: {job["job_id"]}', flush=True)  # antes de gravar: se algo falhar, o id não se perde
    ficha = dict(experimento=pasta_exp.name, pergunta=receita.pergunta, computador=computador,
                 tipo=receita.execucao, data=f'{date.today():%Y-%m-%d}', enviado_utc=registro.agora(),
                 job_id=job['job_id'], shots=shots, semente=semente, opcoes=job['opcoes'],
                 versoes=registro.versoes(), python=platform.python_version(), ordem=job['ordem'],
                 itens=[dict(nome=m['nome'], item=m['item'], qubits_fisicos=m['qubits_fisicos'],
                             arestas=m['arestas'], roteamento=m['roteamento'], compilado=job['info'][m['nome']])
                        for m in montados])
    registro.registrar_envio(pasta, ficha, [job['compilados'][n] for n in job['ordem']])
    if modulo.INSTANTANEO:
        registro.registrar_coleta(pasta, modulo.coletar(job), shots)
    return job
