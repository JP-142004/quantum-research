"""Experimento 8, parte A: tabelas, figura e resultados do modelo de leitura por qubit em 10 qubits.
Usa a conta do experimento 7 (leitura_comparacao); aqui o valor verdadeiro dos indicadores é 1."""
import json
from concurrent.futures import ProcessPoolExecutor
from itertools import repeat

from mitigacao import registro, tabelas
from mitigacao.leitura_comparacao import MODELOS, comparar
from mitigacao.leitura_saida import NOME, _ghz, figura, t_diagnostico, t_diferencas, t_metodos, t_previsao, t_controles

CONTROLES = ('zeros em Z', 'uns em Z', 'todos + em X', 'todos +, qubit 0 em −, em X')
REPLICAS = 250   # o experimento 7 usa 5.000; com 1.024 × 1.024 cada réplica custa ~1,5 s (README da parte A)


def rotulo(sessao):
    """leitura_correlacionada_bloco_02 -> correl. 2; leitura_bloco_01 -> indep. 1 (em duas linhas)."""
    return ('correl.\n' if 'correlacionada' in sessao else 'indep.\n') + str(int(sessao.split('_')[-1]))


def t_erro(res):
    """Ajustado menos o valor verdadeiro (1), por método; a primeira coluna é o observado."""
    linhas = [(s, d['indicador'], tabelas.fmt(d['observado']['valor'] - 1, 3),
               *[tabelas.fmt(d['ajustado'][m]['valor'] - 1, 3) for m in MODELOS])
              for s, r in res.items() for d in _ghz(r)]
    return tabelas.tabela(['Sessão', 'Indicador', 'Observado − 1', *[f'{NOME[m]} − 1' for m in MODELOS]], linhas, range(2, 6))


def gerar(pasta_a, repeticoes=REPLICAS):
    """Lê as sessões de pasta_a/dados e grava pasta_a/resultados e as tabelas do README."""
    sessoes = registro.listar_sessoes(pasta_a)
    with ProcessPoolExecutor(2) as pool:   # uma sessão por processo; cada uma tem a sua semente, então o resultado não muda
        res = {s.name: r for s, r in zip(sessoes, pool.map(comparar, sessoes, repeat(repeticoes)))}
    saida = pasta_a / 'resultados'
    saida.mkdir(exist_ok=True)
    (saida / 'resultados.json').write_text(json.dumps(res, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    t = dict(metodos=t_metodos(res), erro=t_erro(res), diferencas=t_diferencas(res),
             controles=t_controles(res, CONTROLES), previsao=t_previsao(res), diagnostico=t_diagnostico(res))
    (saida / 'tabelas.md').write_text('# Tabelas geradas dos dados (não editar à mão)\n\n'
                                      + '\n\n'.join(f'## {n}\n\n{x}' for n, x in t.items()) + '\n', encoding='utf-8')
    figura(res, saida / 'comparacao_leitura_10q.png', rotulo)
    readme = pasta_a / 'README.md'
    texto = readme.read_text(encoding='utf-8')
    novo = tabelas.preencher(texto, t)
    if novo != texto:
        readme.write_text(novo, encoding='utf-8')
    return dict(sessoes=list(res), tabelas=list(t), figuras=['comparacao_leitura_10q.png'])
