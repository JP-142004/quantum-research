"""Tabelas em Markdown geradas dos resultados da análise, e o preenchimento dos marcadores
`<!-- TABELA:nome -->` dos READMEs. Nenhum número é digitado à mão."""
import re


def fmt(x, casas=4):
    return f'{x:.{casas}f}'.replace('.', ',')


def pm(d, casas=4):
    return f"{fmt(d['valor'], casas)} ± {fmt(d['ep'], casas)}"


def tabela(cabecalho, linhas, direita=()):
    sep = ['---:' if i in direita else '---' for i in range(len(cabecalho))]
    corpo = ['| ' + ' | '.join(str(c) for c in linha) + ' |' for linha in linhas]
    return '\n'.join(['| ' + ' | '.join(cabecalho) + ' |', '| ' + ' | '.join(sep) + ' |'] + corpo)


def rotulo(d):
    if d['circuito'] == 'ghz':
        nome = f"GHZ {d['variante']}, {d['n']} qubits, base {d['base']}"
    else:
        onde = f"qubit {d['qubits'][0]}" if d['n'] == 1 and d['qubits'] else f"{d['n']} qubits"
        nome = f"estado `{d['variante']}`, {onde}" + (', base X' if d['base'] == 'X' else '')
    if d['fator'] != 1:
        nome += f", fator {d['fator']}"
    return nome + (f" ({d['rotulo']})" if d['rotulo'] else '')


def _celula(d):
    return fmt(d['bruto']['valor']) + (f" → {fmt(d['ajustado']['valor'])}" if d['ajustado'] else '')


def curto(sessao, cenario):
    """Tira o nome do cenário do começo do nome da sessão (leitura_bloco_01 -> bloco_01)."""
    return sessao[len(cenario) + 1:] if cenario and sessao.startswith(cenario + '_') else sessao


def t_sessoes(res, cenario=None):
    """Cada item em cada sessão: valor bruto e, quando há calibração, bruto → ajustado."""
    nomes = list(res)
    linhas = [(rotulo(d), d['indicador'], *[_celula(res[s]['itens'][n]) if n in res[s]['itens'] else '—' for s in nomes])
              for n, d in res[nomes[0]]['itens'].items()]
    return tabela(['Item', 'Indicador', *[curto(s, cenario) for s in nomes]], linhas, range(2, 2 + len(nomes)))


def t_contrastes(res, cenario=None):
    """Conectado menos original, por sessão, e se o sinal é o mesmo em todas."""
    nomes, linhas = list(res), []
    for k, c0 in enumerate(res[nomes[0]]['contrastes']):
        celulas, sinais = [], []
        for s in nomes:
            c = res[s]['contrastes'][k]
            alvo = c['ajustado'] or c['bruto']
            celulas.append(pm(alvo, 3))
            sinais.append((alvo['valor'] > 1e-12) - (alvo['valor'] < -1e-12))  # +1, 0 ou -1
        sinal = ('positivo em todas' if all(x == 1 for x in sinais) else 'negativo em todas' if all(x == -1 for x in sinais)
                 else 'zero em todas' if not any(sinais) else 'sinais diferentes')
        linhas.append((f"{c0['indicador']}, {c0['n']} qubits", *celulas, sinal))
    return tabela(['Conectado menos original', *[curto(s, cenario) for s in nomes], 'Sinal'], linhas,
                  range(1, 1 + len(nomes)))


def t_controles(res):
    """Controles independentes: valor (ajustado, se houver) menos o ideal, que é 1."""
    nomes = ['00000 em Z', '11111 em Z', '+++++ em X', '++++- em X']
    linhas = []
    for s, r in res.items():
        ctr = [d for d in r['itens'].values() if d['rotulo'] == 'controle']
        if ctr:
            linhas.append((s, *[fmt((d['ajustado'] or d['bruto'])['valor'] - 1, 3) for d in ctr]))
    return tabela(['Sessão', *nomes], linhas, range(1, 5))


def t_portas(res):
    """Portas de dois qubits depois de compilar, por tamanho e construção (valores distintos entre sessões, se houver)."""
    ghz = [d for r in res.values() for d in r['itens'].values() if d['circuito'] == 'ghz' and d['base'] == 'Z']
    linhas = []
    for n in sorted({d['n'] for d in ghz}):
        cel = [' / '.join(str(p) for p in sorted({d['portas_2q'] for d in ghz if d['n'] == n and d['variante'] == v}))
               for v in ('original', 'conectado')]
        linhas.append((n, *cel))
    return tabela(['Qubits', 'Portas de 2 qubits, original', 'Portas de 2 qubits, conectado'], linhas, range(3))


def t_ganhos(res):
    """Ganho (ajustado menos observado) do GHZ, com o intervalo de 95% do bootstrap, por sessão."""
    nomes = list(res)
    base = [(n, d) for n, d in res[nomes[0]]['itens'].items() if d['circuito'] == 'ghz' and d['ganho']]
    linhas = [(d['indicador'], *[f"{fmt(g['valor'], 3)} [{fmt(g['ic95'][0], 3)}; {fmt(g['ic95'][1], 3)}]"
                                 for g in (res[s]['itens'][n]['ganho'] for s in nomes)]) for n, d in base]
    return tabela(['Indicador', *nomes], linhas, range(1, 1 + len(nomes)))


def por_cenario(res):
    """No simulador com vários cenários, um grupo por cenário; nos demais casos, um grupo só."""
    grupos = {}
    for s, r in res.items():
        grupos.setdefault(r.get('validacao', {}).get('cenario'), {})[s] = r
    return grupos if len(grupos) > 1 else {None: res}


def gerar(res):
    from mitigacao import tabelas_simulacao as sim  # aqui dentro, para não importar em círculo
    """Todas as tabelas que se aplicam a estes resultados. Com vários cenários, as tabelas
    de sessões e de contrastes ganham o nome do cenário no fim (sessoes_leitura, ...)."""
    primeira = next(iter(res.values()))
    t = {}
    for cenario, sub in por_cenario(res).items():
        sufixo = f'_{cenario}' if cenario else ''
        t['sessoes' + sufixo] = t_sessoes(sub, cenario)
        if primeira['contrastes']:
            t['contrastes' + sufixo] = t_contrastes(sub, cenario)
    if any(d['rotulo'] == 'controle' for d in primeira['itens'].values()):
        t['controles'] = t_controles(res)
    if primeira['tipo'] == 'ibm':
        if primeira['contrastes']:
            t['portas'] = t_portas(res)
        if any(d['ganho'] and d['circuito'] == 'ghz' for d in primeira['itens'].values()):
            t['ganhos'] = t_ganhos(res)
    if primeira['tipo'] == 'simulador':
        t['validacao'] = sim.t_validacao(res)
        if primeira['contrastes']:
            t['cenarios'] = sim.t_cenarios(res)
    if any(r['zne'] for r in res.values()):
        t['zne_exato'], t['zne_blocos'] = sim.t_zne_exato(res), sim.t_zne_blocos(res)
    return t


MARCADOR = re.compile(r'(<!-- TABELA:(\w+) -->)\n(.*?)\n?(<!-- /TABELA:\2 -->)', re.S)


def preencher(texto, tabelas):
    """Troca o miolo de cada marcador pela tabela de mesmo nome. Marcador sem tabela vira erro."""
    def troca(m):
        if m.group(2) not in tabelas:
            raise KeyError(f'Não há tabela "{m.group(2)}" para este experimento')
        return f'{m.group(1)}\n{tabelas[m.group(2)]}\n{m.group(4)}'
    return MARCADOR.sub(troca, texto)
