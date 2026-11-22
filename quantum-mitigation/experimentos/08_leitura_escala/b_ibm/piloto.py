"""Experimento 8, parte B, teste prévio: a verificação de independência (mitigacao/leitura_independencia.py)
aplicada a dados que já existem, sem gastar tempo da IBM:

- parte A (simulador, 10 qubits): sabemos quando o erro é conjunto, então vemos se a verificação o detecta;
- experimento 4 (IBM, `ibm_fez`, 5 qubits): o que a verificação diz sobre um computador real.

Só lê `dados/` dos outros experimentos. Uso, a partir de quantum-mitigation/:
  python experimentos/08_leitura_escala/b_ibm/piloto.py
"""
import json
import sys
from pathlib import Path

import numpy as np

RAIZ = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(RAIZ))

from mitigacao import leitura_independencia as li, registro, tabelas  # noqa: E402
from mitigacao.tecnicas import leitura  # noqa: E402

EXP = RAIZ / 'experimentos'
ORIGENS = (('A · simulador, 10 qubits', EXP / '08_leitura_escala' / 'a_simulador', 10, list(range(10))),
           ('Experimento 4 · IBM, 5 qubits', EXP / '04_calibracao_leitura', 5, [0, 1, 2, 3, 4]))
SEMENTE = 2026
PERMUTACOES = 1000


def analisar(pasta_exp, n, qubits):
    saida = {}
    for sessao in registro.listar_sessoes(pasta_exp):
        _, contagens = registro.ler_sessao(sessao)
        for nome, j in (('zeros', 0), ('uns', 2 ** n - 1)):
            e = li.erros(leitura._contagens_do_estado(contagens, n, j, qubits), f'{j:0{n}b}')
            r = li.teste(e, np.random.default_rng(SEMENTE), PERMUTACOES)
            i, k, obs, esp = li.pares_mais_ligados(e, 1)[0]
            saida[f'{sessao.name} · {nome}'] = dict(r, par=[i, k], juntos_observados=obs, juntos_esperados=esp)
    return saida


def main():
    res = {origem: analisar(pasta, n, q) for origem, pasta, n, q in ORIGENS}
    pasta = Path(__file__).resolve().parent
    (pasta / 'resultados').mkdir(exist_ok=True)
    (pasta / 'resultados' / 'piloto_independencia.json').write_text(
        json.dumps(res, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    linhas = [(origem, nome, tabelas.fmt(r['taxa_de_erro'], 3), tabelas.fmt(r['T'], 3),
               f"{tabelas.fmt(r['nulo_media'], 3)} ± {tabelas.fmt(r['nulo_dp'], 3)}", tabelas.fmt(r['p_valor'], 3),
               f"{r['par'][0]}–{r['par'][1]}: {r['juntos_observados']} (esperado {tabelas.fmt(r['juntos_esperados'], 1)})")
              for origem, itens in res.items() for nome, r in itens.items()]
    tabela = tabelas.tabela(['Origem', 'Sessão · estado', 'Taxa de erro por qubit', 'T', 'T com qubits embaralhados',
                             'p-valor', 'Par com mais erros juntos'], linhas, (2, 3, 5))
    (pasta / 'resultados' / 'piloto_independencia.md').write_text(
        '# Teste prévio da verificação de independência (gerado dos dados; não editar à mão)\n\n' + tabela + '\n', encoding='utf-8')
    readme = pasta / 'README.md'
    texto = readme.read_text(encoding='utf-8')
    novo = tabelas.preencher(texto, dict(piloto=tabela), parcial=True)   # as outras vêm do analisar.py
    if novo != texto:
        readme.write_text(novo, encoding='utf-8')
    return tabela


if __name__ == '__main__':
    print(main())
