#!/usr/bin/env python3
"""Comando único do projeto. O argumento é o número do experimento.

  python rodar.py 03 --verificar                     mostra o que seria enviado; não envia nada
  python rodar.py 03 --enviar --computador ibm_fez   envia (pede confirmação) e grava a sessão
  python rodar.py 03 --coletar --sessao 2026-11-10_ibm_fez
  python rodar.py 03 --listar                        lista as sessões do experimento

Uma sessão já registrada nunca é sobrescrita nem reenviada.
"""
import argparse
import importlib.util
import platform
import sys
from datetime import date
from pathlib import Path

from mitigacao import registro
from mitigacao.execucao import ibm, simulador
from mitigacao.montagem import montar, verificar_ideal
from mitigacao.topologia import vizinhos_linha

RAIZ = Path(__file__).resolve().parent
MODULOS = {'ibm': ibm, 'simulador': simulador}


def achar_experimento(numero):
    achados = sorted((RAIZ / 'experimentos').glob(f'{int(numero):02d}_*'))
    if len(achados) != 1:
        sys.exit(f'Experimento {numero}: encontrei {len(achados)} pastas em experimentos/')
    return achados[0]


def carregar_receita(pasta):
    caminho = pasta / 'experimento.py'
    if not caminho.exists():
        sys.exit(f'{caminho} não existe')
    spec = importlib.util.spec_from_file_location('receita', caminho)
    receita = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(receita)
    return receita


def resumir(montados, shots, sessoes):
    print(f'{"item":42} {"n":>3}  qubits físicos             ideal')
    for m in montados:
        ok = verificar_ideal(m)
        estado = 'pulado (n grande)' if ok is None else 'ok' if ok else 'FALHOU'
        print(f'{m["nome"]:42} {m["item"]["n"]:>3}  {str(m["qubits_fisicos"]):25} {estado}')
    medidas = len(montados) * shots
    print(f'\n{len(montados)} circuitos x {shots} shots = {medidas:,} medidas por sessão'.replace(',', '.'))
    print(f'{sessoes} sessões previstas = {medidas * sessoes:,} medidas no total'.replace(',', '.'))


def montar_da_receita(receita, computador, online):
    modulo = MODULOS[receita.execucao]
    if receita.execucao == 'ibm' and online:
        vizinhos = modulo.vizinhos(computador)
    elif receita.execucao == 'ibm':
        vizinhos = vizinhos_linha  # verificação local: computador sintético em linha
    else:
        vizinhos = lambda n: modulo.vizinhos(computador, n)  # noqa: E731
    return montar(receita.itens, vizinhos, getattr(receita, 'raiz', 2))


def verificar(receita, args):
    print(f'Pergunta: {receita.pergunta}')
    if receita.execucao == 'ibm':
        print('Verificação local, com um computador sintético em linha. Os qubits reais são escolhidos no envio.\n')
    montados = montar_da_receita(receita, args.computador, online=False)
    resumir(montados, getattr(receita, 'shots', 1000), getattr(receita, 'repeticoes', 1))
    return 0 if all(verificar_ideal(m) is not False for m in montados) else 1


def enviar(pasta_exp, receita, args):
    modulo = MODULOS[receita.execucao]
    shots = getattr(receita, 'shots', 1000)
    nome = args.sessao or f'{date.today():%Y-%m-%d}_{args.computador}'
    pasta = pasta_exp / 'dados' / nome
    if pasta.exists():
        sys.exit(f'A sessão {nome} já existe. Nada foi enviado.')
    montados = montar_da_receita(receita, args.computador, online=True)
    if any(verificar_ideal(m) is False for m in montados):
        sys.exit('Algum circuito não bate com o resultado ideal. Nada foi enviado.')
    resumir(montados, shots, 1)
    if receita.execucao == 'ibm':
        pedido = input(f'\nIsto envia {len(montados)} circuitos ({len(montados) * shots} medidas) a {args.computador}. '
                       'Digite ENVIAR para confirmar: ')
        if pedido != 'ENVIAR':
            sys.exit('Cancelado. Nada foi enviado.')
    job = modulo.enviar(montados, shots, args.semente, args.computador, **getattr(receita, 'opcoes_envio', {}))
    print(f'Job: {job["job_id"]}', flush=True)  # antes de gravar: se algo falhar, o id não se perde
    ficha = dict(experimento=pasta_exp.name, pergunta=receita.pergunta, computador=args.computador,
                 tipo=receita.execucao, data=f'{date.today():%Y-%m-%d}', enviado_utc=registro.agora(),
                 job_id=job['job_id'], shots=shots, semente=args.semente, opcoes=job['opcoes'],
                 versoes=registro.versoes(), python=platform.python_version(), ordem=job['ordem'],
                 itens=[dict(nome=m['nome'], item=m['item'], qubits_fisicos=m['qubits_fisicos'],
                             arestas=m['arestas'], roteamento=m['roteamento'], compilado=job['info'][m['nome']])
                        for m in montados])
    registro.registrar_envio(pasta, ficha, [job['compilados'][n] for n in job['ordem']])
    if modulo.INSTANTANEO:
        registro.registrar_coleta(pasta, modulo.coletar(job), shots)
    print(f'Sessão gravada em {pasta}')
    return 0


def coletar(pasta_exp, args):
    if not args.sessao:
        sys.exit('Informe --sessao')
    pasta = pasta_exp / 'dados' / args.sessao
    ficha, contagens = registro.ler_sessao(pasta)
    if contagens is not None:
        sys.exit('Esta sessão já foi coletada.')
    resultado = MODULOS[ficha['tipo']].coletar(dict(job_id=ficha['job_id'], ordem=ficha['ordem']))
    if resultado is None:
        print('O job ainda não terminou.')
        return 0
    registro.registrar_coleta(pasta, resultado, ficha['shots'])
    print(f'Contagens gravadas em {pasta}')
    return 0


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('experimento')
    modo = p.add_mutually_exclusive_group(required=True)
    for opcao in ('verificar', 'enviar', 'coletar', 'listar'):
        modo.add_argument(f'--{opcao}', action='store_true')
    p.add_argument('--computador')
    p.add_argument('--sessao')
    p.add_argument('--semente', type=int, default=42)
    args = p.parse_args()
    pasta_exp = achar_experimento(args.experimento)
    if args.listar:
        for s in registro.listar_sessoes(pasta_exp):
            print(s.name, '(coletada)' if (s / 'contagens.json').exists() else '(aguardando coleta)')
        return 0
    if args.coletar:
        return coletar(pasta_exp, args)
    receita = carregar_receita(pasta_exp)
    args.computador = args.computador or getattr(receita, 'computador', 'simulador')
    return verificar(receita, args) if args.verificar else enviar(pasta_exp, receita, args)


if __name__ == '__main__':
    sys.exit(main())
