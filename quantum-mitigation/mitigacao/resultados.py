"""Gera `resultados/` de um experimento: resultados.json, tabelas.md, figuras e as tabelas
dos marcadores do README. Tudo vem dos dados das sessões e pode ser refeito."""
import json

from mitigacao import analise, graficos, registro, tabelas


def gerar(pasta_exp, tecnicas=(), repeticoes=analise.REPETICOES):
    sessoes = [s for s in registro.listar_sessoes(pasta_exp) if (s / 'contagens.json').exists()]
    if not sessoes:
        raise ValueError('Nenhuma sessão coletada neste experimento')
    res = {}
    for s in sessoes:
        print(f'Analisando {s.name}...', flush=True)
        res[s.name] = analise.analisar(s, tecnicas, repeticoes=repeticoes)
    saida = pasta_exp / 'resultados'
    saida.mkdir(exist_ok=True)
    (saida / 'resultados.json').write_text(json.dumps(res, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    t = tabelas.gerar(res)
    (saida / 'tabelas.md').write_text(
        '# Tabelas geradas dos dados (não editar à mão)\n\n'
        + '\n\n'.join(f'## {nome}\n\n{tab}' for nome, tab in t.items()) + '\n', encoding='utf-8')
    figuras = _figuras(res, saida)
    readme = pasta_exp / 'README.md'
    if readme.exists():
        texto = readme.read_text(encoding='utf-8')
        novo = tabelas.preencher(texto, t)
        if novo != texto:
            readme.write_text(novo, encoding='utf-8')
    return dict(sessoes=list(res), tabelas=list(t), figuras=figuras)


def _figuras(res, saida):
    feitas = []
    if all(r['tipo'] == 'ibm' for r in res.values()):
        return _figuras_ibm(res, saida)
    if any(r['tipo'] == 'simulador' and r['contrastes'] for r in res.values()):
        for cenario in sorted({r['validacao']['cenario'] for r in res.values()}):
            graficos.comparacao(res, cenario, saida / f'comparacao_{cenario}.png')
            feitas.append(f'comparacao_{cenario}.png')
    if any(r['zne'] for r in res.values()):
        graficos.zne_blocos(res, saida / 'zne_blocos.png')
        graficos.zne_fatores(res, saida / 'zne_fatores.png')
        feitas += ['zne_blocos.png', 'zne_fatores.png']
    return feitas


def _figuras_ibm(res, saida):
    """Uma figura por experimento da IBM, escolhida pelo conteúdo: circuitos simples (2), GHZ com
    calibração (4), original e conectado (3) ou só original (1). Cada sessão aparece separada."""
    from mitigacao import graficos_ibm
    itens = [d for d in next(iter(res.values()))['itens'].values()]
    if all(d['circuito'] == 'simples' for d in itens):
        f, nome = graficos_ibm.controles, 'controles.png'
    elif any(d['ajustado'] for d in itens):
        f, nome = graficos_ibm.calibracao, 'calibracao.png'
    elif {d['variante'] for d in itens} == {'original', 'conectado'}:
        f, nome = graficos_ibm.construcao, 'construcao.png'
    else:
        f, nome = graficos_ibm.escala, 'escala.png'
    f(res, saida / nome)
    return [nome]
