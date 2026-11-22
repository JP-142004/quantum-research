"""Experimento 7: calibração de leitura completa contra os modelos por qubit, em cada sessão do
experimento 4. Explicação: fundamentos/tecnicas/leitura.md e experimentos/07_leitura_fatorizada/README.md.

Bootstrap compartilhado: em cada réplica, a calibração e os circuitos são reamostrados uma vez e
a mesma réplica entra nos três ajustes, então as diferenças têm a incerteza certa.
"""
import numpy as np

from mitigacao import indicadores, registro
from mitigacao.analise import REPETICOES, e_calibracao, indicador_do_item, pesos, resumo, vetor
from mitigacao.estatistica import reamostrar
from mitigacao.tecnicas import leitura

MODELOS = ('completo', 'fatorizado', 'fatorizado_dois')
COMPARACOES = (('fatorizado', 'completo'), ('fatorizado_dois', 'completo'), ('fatorizado', 'fatorizado_dois'))
MARGEM = 0.02            # definida antes de calcular (README do experimento 7)
SEMENTE_DIVISAO = 20261122
SEMENTE_BOOTSTRAP = 2026


def decisao(ic95, margem=MARGEM):
    """Equivalente: intervalo inteiro dentro da margem. Diferente: inteiro fora, de um lado só."""
    baixo, alto = ic95
    if -margem <= baixo and alto <= margem:
        return 'equivalente'
    return 'diferente' if baixo > margem or alto < -margem else 'inconclusivo'


def _ajustar(cal, n, qubits, p, perms):
    """(q, A) de cada modelo para as distribuições p, na mesma calibração."""
    saida = {}
    for modelo in MODELOS:
        a = leitura.matriz(cal, n, qubits, modelo)
        saida[modelo] = (leitura.corrigir_varios(a, p, perms), a)
    return saida


def _previsao(contagens, itens_cal, n, qubits, semente):
    """Divide as medidas de cada calibração em duas metades ao acaso (semente fixa). Monta cada modelo
    com a primeira e compara, nos 32 estados, a distribuição prevista com a da segunda metade."""
    rng = np.random.default_rng(semente)
    primeira, segunda = {}, {}
    for it in itens_cal:
        chaves, v = list(contagens[it['nome']]), np.array(list(contagens[it['nome']].values()))
        metade = rng.multivariate_hypergeometric(v, int(v.sum()) // 2)
        primeira[it['nome']] = {k: int(x) for k, x in zip(chaves, metade) if x}
        segunda[it['nome']] = {k: int(x) for k, x in zip(chaves, v - metade) if x}
    saida = {}
    for modelo in MODELOS:
        a = leitura.matriz(primeira, n, qubits, modelo)
        d = [0.5 * np.abs(a[:, int(it['item']['variante'], 2)]
                          - vetor(segunda[it['nome']], n, sum(segunda[it['nome']].values()))).sum() for it in itens_cal]
        saida[modelo] = dict(media=float(np.mean(d)), maximo=float(np.max(d)))
    return saida


def comparar(pasta, repeticoes=REPETICOES, semente=SEMENTE_BOOTSTRAP):
    ficha, contagens = registro.ler_sessao(pasta)
    shots = ficha['shots']
    cal = [i for i in ficha['itens'] if e_calibracao(i['item'])]
    n, qubits = cal[0]['item']['n'], cal[0]['item']['qubits']
    alvos = [i for i in ficha['itens'] if i['nome'] not in {c['nome'] for c in cal} and i['item']['n'] == n]
    p = np.array([vetor(contagens[i['nome']], n, shots) for i in alvos])
    w = np.array([pesos(indicador_do_item(i['item'])[1], n) for i in alvos])
    perms = [leitura.permutacao([tuple(m) for m in i['compilado']['mapa_medidas']], n) for i in alvos]
    cal_dados = {c['nome']: contagens[c['nome']] for c in cal}
    ponto = _ajustar(cal_dados, n, qubits, p, perms)
    valor = {m: (w * ponto[m][0]).sum(1) for m in MODELOS}
    replicas, falhas, rng = {m: [] for m in MODELOS}, 0, np.random.default_rng(semente)
    for _ in range(repeticoes):
        cal_r = {nome: reamostrar(c, rng) for nome, c in cal_dados.items()}
        try:
            aj = _ajustar(cal_r, n, qubits, rng.multinomial(shots, p) / shots, perms)
        except ValueError:      # calibração instável nesta réplica: conta e segue, sem esconder
            falhas += 1
            continue
        for m in MODELOS:
            replicas[m].append((w * aj[m][0]).sum(1))
    replicas = {m: np.array(r) for m, r in replicas.items()}
    itens = []
    for j, i in enumerate(alvos):
        nome_ind, _, tipo = indicador_do_item(i['item'])
        bruto = float(w[j] @ p[j])
        d = dict(nome=i['nome'], indicador=nome_ind, circuito=i['item']['circuito'], rotulo=i['item']['rotulo'],
                 variante=i['item']['variante'], base=i['item']['base'],
                 observado=dict(valor=bruto, ep=indicadores.erro_padrao(bruto, shots, tipo)),
                 ajustado={m: resumo(valor[m][j], replicas[m][:, j]) for m in MODELOS},
                 menor_quasi={m: float(ponto[m][0][j].min()) for m in MODELOS}, diferencas={})
        for a, b in COMPARACOES:
            r = resumo(valor[a][j] - valor[b][j], replicas[a][:, j] - replicas[b][:, j])
            d['diferencas'][f'{a}-{b}'] = dict(r, decisao=decisao(r['ic95']))
        itens.append(d)
    return dict(sessao=pasta.name, computador=ficha['computador'], data=ficha['data'], shots=shots,
                repeticoes=repeticoes, replicas_com_falha=falhas, margem=MARGEM,
                condicionamento={m: float(np.linalg.cond(ponto[m][1])) for m in MODELOS}, itens=itens,
                previsao=_previsao(contagens, cal, n, qubits, SEMENTE_DIVISAO))
