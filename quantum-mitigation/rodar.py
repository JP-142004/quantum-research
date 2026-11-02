#!/usr/bin/env python3
"""Comando único do projeto. O argumento é o número do experimento.

  python rodar.py 03 --verificar                     mostra o que seria enviado; não envia nada
  python rodar.py 03 --verificar --online            idem, mas consulta o computador real da IBM
                                                     e compila os circuitos nele (também não envia)
  python rodar.py 03 --enviar --computador ibm_fez   envia (pede confirmação) e grava a sessão
  python rodar.py 05 --enviar --todas                roda todas as sessões do simulador da receita
  python rodar.py 03 --coletar --sessao 2026-11-10_ibm_fez
  python rodar.py 03 --listar                        lista as sessões do experimento

Uma sessão já registrada nunca é sobrescrita nem reenviada.
"""
import argparse
import importlib.util
import sys
from pathlib import Path

from mitigacao import registro, sessao
from mitigacao.execucao import ibm, simulador  # noqa: F401  (os testes trocam estes módulos)
from mitigacao.montagem import verificar_ideal

RAIZ = Path(__file__).resolve().parent


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


def resumir(montados, shots, sessoes, compilados=None):
    cabecalho = f'{"item":44} {"n":>3}  {"qubits físicos":28} {"ideal":6}'
    print(cabecalho + ('  portas2q prof' if compilados else ''))
    for m in montados:
        ok = verificar_ideal(m)
        estado = '-' if ok is None else 'ok' if ok else 'FALHOU'
        qubits = str(m['qubits_fisicos']) if len(m['qubits_fisicos']) <= 6 else f'{len(m["qubits_fisicos"])} qubits'
        linha = f'{m["nome"]:44} {m["item"]["n"]:>3}  {qubits:28} {estado:6}'
        if compilados:
            info = ibm_info(compilados[m['nome']])
            linha += f'  {info["portas_2q"]:>8} {info["profundidade"]:>4}'
        print(linha)
    medidas = len(montados) * shots
    print(f'\n{len(montados)} circuitos x {shots} shots = {medidas:,} medidas por sessão'.replace(',', '.'))
    print(f'{sessoes} sessões previstas = {medidas * sessoes:,} medidas no total'.replace(',', '.'))


def ibm_info(qc):
    from mitigacao.execucao import info_compilado
    return info_compilado(qc)


def verificar(receita, args):
    print(f'Pergunta: {receita.pergunta}')
    online = args.online and receita.execucao == 'ibm'
    if receita.execucao == 'ibm':
        print('Consulta o computador real e compila nele; não envia nada.\n' if online else
              'Verificação local, com um computador sintético em linha. Os qubits reais são escolhidos no envio.\n')
    montados = sessao.montar_receita(receita, args.computador, online=online)
    compilados = ibm.compilar(montados, ibm.backend(args.computador)) if online else None
    resumir(montados, getattr(receita, 'shots', 1000), getattr(receita, 'repeticoes', 1), compilados)
    return 0 if all(verificar_ideal(m) is not False for m in montados) else 1


def enviar(pasta_exp, receita, args):
    padrao = getattr(receita, 'opcoes_envio', {})
    if args.todas:
        if receita.execucao != 'simulador' or not hasattr(receita, 'sessoes'):
            sys.exit('--todas só vale para receitas do simulador que declaram `sessoes`')
        lista = [{**dict(opcoes_envio=padrao, semente=args.semente), **s} for s in receita.sessoes]
    else:
        lista = [dict(nome=args.sessao or sessao.nome_padrao(args.computador), semente=args.semente,
                      opcoes_envio=padrao)]
    existentes = [s['nome'] for s in lista if (pasta_exp / 'dados' / s['nome']).exists()]
    if existentes:
        sys.exit(f'Já existem as sessões {", ".join(existentes)}. Nada foi enviado.')
    shots = getattr(receita, 'shots', 1000)
    for s in lista:
        try:
            pasta, montados = sessao.preparar(pasta_exp, receita, args.computador, s['nome'])
        except RuntimeError as erro:
            sys.exit(str(erro))
        if not args.todas:
            resumir(montados, shots, 1)
        if receita.execucao == 'ibm':
            pedido = input(f'\nIsto envia {len(montados)} circuitos ({len(montados) * shots} medidas) a '
                           f'{args.computador}. Digite ENVIAR para confirmar: ')
            if pedido != 'ENVIAR':
                sys.exit('Cancelado. Nada foi enviado.')
        sessao.enviar_e_gravar(pasta, pasta_exp, receita, montados, args.computador, s['semente'], s['opcoes_envio'])
        print(f'Sessão {s["nome"]} gravada em {pasta}')
    return 0


def coletar(pasta_exp, args):
    if not args.sessao:
        sys.exit('Informe --sessao')
    pasta = pasta_exp / 'dados' / args.sessao
    ficha, contagens = registro.ler_sessao(pasta)
    if contagens is not None:
        sys.exit('Esta sessão já foi coletada.')
    resultado = sessao.MODULOS[ficha['tipo']].coletar(dict(job_id=ficha['job_id'], ordem=ficha['ordem']))
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
    p.add_argument('--online', action='store_true')
    p.add_argument('--todas', action='store_true')
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
