#!/usr/bin/env python3
"""Preenche as tabelas dos documentos a partir dos arquivos de dados.

Nos arquivos Markdown, cada tabela fica entre dois marcadores:

    <!-- TABELA:nome -->
    ...conteúdo gerado...
    <!-- /TABELA:nome -->

Este script recalcula o conteúdo de cada marcador. Assim nenhum número das tabelas
é digitado à mão: tudo vem de dados/ (contagens reais, resultados processados e
referências da simulação).

Uso:
    python scripts/gerar_tabelas.py            # reescreve as tabelas
    python scripts/gerar_tabelas.py --verificar  # só confere; sai com erro se divergir

Não acessa a IBM e usa apenas a biblioteca padrão.
"""
import argparse
import csv
import json
import re
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
DADOS = BASE / 'dados'
SIM = DADOS / 'simulados' / 'validacao_2026_11_01'


def num(x, casas=4):
    """Formata com vírgula decimal, como nos textos."""
    return f'{x:.{casas}f}'.replace('.', ',')


def sgn(x, casas=3):
    """Número com sinal explícito."""
    return ('+' if x >= 0 else '−') + num(abs(x), casas)


def tabela(cabecalho, linhas, alinhar_direita=()):
    sep = ['---:' if i in alinhar_direita else '---' for i in range(len(cabecalho))]
    saida = ['| ' + ' | '.join(cabecalho) + ' |', '| ' + ' | '.join(sep) + ' |']
    saida += ['| ' + ' | '.join(str(c) for c in linha) + ' |' for linha in linhas]
    return '\n'.join(saida)


# ---------------------------------------------------------------- tabelas reais

def t_escala():
    with open(DADOS / 'processados' / 'resumo_escala.csv', encoding='utf-8') as f:
        linhas = list(csv.DictReader(f))
    corpo = [(l['qubits'], l['todos_zeros'], l['todos_uns'], l['outros'], num(float(l['populacao_z']), 3))
             for l in linhas]
    return tabela(['Qubits', 'Todos zeros', 'Todos uns', 'Outros', 'PZ'], corpo, range(5))


def _rodadas():
    return json.load(open(DADOS / 'processados' / 'comparacao_rodadas.json', encoding='utf-8'))['rodadas']


def t_rodadas():
    corpo = []
    for r in _rodadas():
        z, x = r['metricas']['populacao_z'], r['metricas']['correlacao_x']
        corpo.append((r['rodada'], f"{num(z['bruto'])} → {num(z['ajustado'])}",
                      f"{num(x['bruto'])} → {num(x['ajustado'])}"))
    return tabela(['Rodada', 'PZ bruto → ajustado', 'CX bruta → ajustada'], corpo, (0,))


def t_rodadas_ganho():
    corpo = []
    for r in _rodadas():
        for nome, rot in (('populacao_z', 'PZ'), ('correlacao_x', 'CX')):
            m = r['metricas'][nome]
            lo, hi = m['ic95_ganho_percentil']
            corpo.append((r['rodada'], rot, num(m['bruto']), num(m['se_bruto']), num(m['ajustado']),
                          num(m['se_ajustado']), num(m['ganho']), f'{num(lo)} a {num(hi)}'))
    return tabela(['Rodada', 'Indicador', 'Bruto', 'EP bruto', 'Ajustado', 'EP ajustado', 'Ganho',
                   'IC 95% do ganho'], corpo, range(8))


def t_rodadas_jobs():
    corpo = [(r['rodada'], f"`{r['job_id']}`", r['backend'], (r['enviado_utc'][:10] if r.get('enviado_utc') else 'não registrada'),
              r['circuitos'], r['shots_por_circuito'], r['circuitos'] * r['shots_por_circuito'])
             for r in _rodadas()]
    total = sum(c[6] for c in corpo)
    corpo = [c[:6] + (f'{c[6]:,}'.replace(',', '.'),) for c in corpo]
    corpo.append(('**Total**', '', '', '', '', '', f"**{f'{total:,}'.replace(',', '.')}**"))
    return tabela(['Rodada', 'Job IBM', 'Backend', 'Data de envio', 'Circuitos', 'Shots por circuito', 'Medidas'],
                  corpo, (0, 4, 5, 6))


def _data_job(job_id):
    """Data de criação do job, lida do JSON recuperado da IBM (etapas 2 e 3)."""
    for pasta in ('02_controles', '03_ghz_conectado'):
        arq = DADOS / 'brutos' / pasta / f'{job_id}.json'
        if arq.exists():
            return json.load(open(arq, encoding='utf-8'))['criado'][:10]
    return 'não registrada'


def _linhas(pasta):
    return json.load(open(DADOS / 'processados' / pasta / 'resultados_recuperados.json', encoding='utf-8'))


def t_construcoes():
    corpo = []
    for l in _linhas('03_ghz_conectado'):
        rot = 'PZ' if l['circuito'].endswith('_Z') else 'CX'
        corpo.append((l['experimento'], l['circuito'], l['bits'], l['portas_duplas'], l['profundidade'],
                      f"{rot} = {num(l['indicador'], 3)}", _data_job(l['job_id']), f"`{l['job_id']}`"))
    return tabela(['Experimento', 'Circuito', 'Qubits', 'Portas de 2 qubits', 'Profundidade', 'Indicador',
                   'Data do job', 'Job'], corpo, (2, 3, 4))


def t_construcoes_testes():
    """Diferenças entre circuitos, em unidades de erro padrão analítico (só amostragem)."""
    por_circ = {(l['job_id'], l['circuito']): l for l in _linhas('03_ghz_conectado')}
    n = 1000

    def ep(ind, valor):
        return ((valor * (1 - valor)) / n) ** 0.5 if ind == 'PZ' else ((1 - valor ** 2) / n) ** 0.5

    pares = [
        ('Mesmo circuito original em dois jobs', 'PZ', ('dbccaqpgv2cc73ea21fg', 'original_Z'),
         ('dbcccpc24mrc73cjb6bg', 'original_Z')),
        ('Conectado menos original, base Z', 'PZ', ('dbcccpc24mrc73cjb6bg', 'original_Z'),
         ('dbcccpc24mrc73cjb6bg', 'conectado_Z')),
        ('Conectado menos original, base X', 'CX', ('dbcco2fi0auc73dum8i0', 'original_X'),
         ('dbcco2fi0auc73dum8i0', 'conectado_X')),
    ]
    corpo = []
    for rot, ind, a, b in pares:
        va, vb = por_circ[a]['indicador'], por_circ[b]['indicador']
        e = (ep(ind, va) ** 2 + ep(ind, vb) ** 2) ** 0.5
        corpo.append((rot, ind, num(va, 3), num(vb, 3), num(vb - va, 3), num(e, 3), num((vb - va) / e, 1)))
    return tabela(['Comparação', 'Indicador', 'Primeiro', 'Segundo', 'Diferença', 'EP da diferença',
                   'Diferença em EP'], corpo, range(2, 7))


def t_controles():
    corpo = []
    for l in _linhas('02_controles'):
        corpo.append((l['experimento'], l['backend'], _data_job(l['job_id']), l['circuito'],
                      f"`{l['estado_preparado']}`", f"{l['acertos']}/{l['shots']}",
                      num(l['acertos'] / l['shots'], 3)))
    return tabela(['Experimento', 'Backend', 'Data do job', 'Circuito', 'Preparado',
                   'Medidas iguais ao preparado', 'Fração'], corpo, (5, 6))


# ------------------------------------------------------------ tabelas simuladas

def _manifesto():
    return json.load(open(SIM / 'manifesto.json', encoding='utf-8'))


def _pz(p):
    return p[0] + p[-1]


def _cx(p):
    return sum(v if bin(i).count('1') % 2 == 0 else -v for i, v in enumerate(p))


def t_cenarios():
    ref = _manifesto()['referencias']['comparacao']
    rotulos = {'ideal': 'Ideal', 'leitura': 'Só leitura', 'leitura_e_portas': 'Leitura e portas'}
    corpo = []
    for cen in ('ideal', 'leitura', 'leitura_e_portas'):
        for cons in ('original', 'conectado'):
            z, x = ref[cen][f'{cons}_Z'], ref[cen][f'{cons}_X']
            corpo.append((rotulos[cen], cons, num(_pz(z['antes_leitura'])), num(_pz(z['observado'])),
                          num(_cx(x['antes_leitura'])), num(_cx(x['observado']))))
    return tabela(['Cenário', 'Construção', 'PZ antes da leitura', 'PZ após a leitura',
                   'CX antes da leitura', 'CX após a leitura'], corpo, range(2, 6))


def _reta(xs, ys):
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    b = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs)
    return my - b * mx


def t_zne():
    z = _manifesto()['referencias']['zne']['leitura_e_portas']
    fatores, cx_portas = (1, 3, 5), (4, 12, 20)
    pzs = [_pz(z[f'zne_{f}_Z']['antes_leitura']) for f in fatores]
    cxs = [_cx(z[f'zne_{f}_X']['antes_leitura']) for f in fatores]
    corpo = [(f, p, num(a), num(b)) for f, p, a, b in zip(fatores, cx_portas, pzs, cxs)]
    corpo.append(('0 (extrapolado)', '—', f'**{num(_reta(fatores, pzs))}**', f'**{num(_reta(fatores, cxs))}**'))
    return tabela(['Fator de ruído', 'Portas CX', 'PZ (referência do modelo)', 'CX (referência do modelo)'],
                  corpo, (0, 1, 2, 3))


def t_zne_blocos():
    """Resultado da extrapolação nos três blocos amostrados (com erro padrão do bootstrap)."""
    corpo = []
    for b in (1, 2, 3):
        a = json.load(open(SIM / f'zne_leitura_e_portas_bloco_0{b}_analise.json', encoding='utf-8'))
        z1, x1 = a['circuitos']['zne_1_Z']['ajustado'], a['circuitos']['zne_1_X']['ajustado']
        zz, zx = a['contrastes']['Z']['zne'], a['contrastes']['X']['zne']
        corpo.append((b, f"{num(z1['valor'])} ± {num(z1['erro_padrao'])}", f"{num(zz['valor'])} ± {num(zz['erro_padrao'])}",
                      f"{num(x1['valor'])} ± {num(x1['erro_padrao'])}", f"{num(zx['valor'])} ± {num(zx['erro_padrao'])}"))
    return tabela(['Bloco', 'PZ, fator 1, ajustado', 'PZ após ZNE', 'CX, fator 1, ajustada', 'CX após ZNE'],
                  corpo, range(5))


def t_sintese():
    """Síntese das três técnicas testadas. As condições são diferentes: não é um ranking."""
    c = {(l['job_id'], l['circuito']): l for l in _linhas('03_ghz_conectado')}
    zo, zc = c[('dbcccpc24mrc73cjb6bg', 'original_Z')], c[('dbcccpc24mrc73cjb6bg', 'conectado_Z')]
    xo, xc = c[('dbcco2fi0auc73dum8i0', 'original_X')], c[('dbcco2fi0auc73dum8i0', 'conectado_X')]
    rod = _rodadas()
    gz = [r['metricas']['populacao_z']['ganho'] for r in rod]
    gx = [r['metricas']['correlacao_x']['ganho'] for r in rod]
    z = _manifesto()['referencias']['zne']['leitura_e_portas']
    pzs = [_pz(z[f'zne_{f}_Z']['antes_leitura']) for f in (1, 3, 5)]
    ext = _reta((1, 3, 5), pzs)
    linhas = [
        ('Construção com menos portas', 'IBM Fez, valores brutos',
         f"PZ {sgn(zc['indicador'] - zo['indicador'])}; CX {sgn(xc['indicador'] - xo['indicador'])}",
         f"{zo['portas_duplas'] - zc['portas_duplas']} portas CX a menos ({zo['portas_duplas']} → {zc['portas_duplas']}); nenhum shot extra"),
        ('Calibração de leitura', 'IBM Fez, 3 rodadas',
         f"PZ {sgn(min(gz))} a {sgn(max(gz))}; CX {sgn(min(gx))} a {sgn(max(gx))}",
         f"{rod[0]['circuitos'] - 2} circuitos de calibração por rodada; erro padrão maior"),
        ('Extrapolação a ruído zero', 'Simulação, referência exata',
         f"PZ {num(pzs[0])} → {num(ext)} (fator 1 → extrapolado)",
         '3 versões do circuito, até 20 CX; erro padrão maior; viés da reta'),
    ]
    return tabela(['Técnica', 'Onde', 'Variação nos indicadores', 'Custo'], linhas)


def t_parametros():
    p = _manifesto()['parametros']
    corpo = [(q, num(a, 2), num(b, 2)) for q, (a, b) in enumerate(zip(p['e01'], p['e10']))]
    cab = tabela(['Qubit', 'Erro 0→1 na leitura', 'Erro 1→0 na leitura'], corpo, (0, 1, 2))
    return cab + f"\n\nRuído depolarizante após cada CX: {num(p['depolarizante_cx'], 2)}. " \
        f"Conexões usadas: {', '.join(f'{a}→{b}' for a, b in p['arestas'])}."


TABELAS = {
    'escala': t_escala, 'rodadas': t_rodadas, 'rodadas_ganho': t_rodadas_ganho, 'rodadas_jobs': t_rodadas_jobs,
    'construcoes': t_construcoes, 'construcoes_testes': t_construcoes_testes, 'controles': t_controles, 'cenarios': t_cenarios, 'zne': t_zne, 'zne_blocos': t_zne_blocos,
    'parametros': t_parametros, 'sintese': t_sintese,
}
MARCADOR = re.compile(r'(<!-- TABELA:(\w+) -->)\n(.*?)\n?(<!-- /TABELA:\2 -->)', re.S)


def processar(caminho, verificar):
    texto = caminho.read_text(encoding='utf-8')
    divergiu = []

    def troca(m):
        nome = m.group(2)
        if nome not in TABELAS:
            raise SystemExit(f'{caminho}: tabela desconhecida "{nome}"')
        novo = TABELAS[nome]()
        if novo != m.group(3).strip('\n'):
            divergiu.append(nome)
        return m.group(1) + '\n' + novo + '\n' + m.group(4)

    novo_texto = MARCADOR.sub(troca, texto)
    if divergiu and not verificar:
        caminho.write_text(novo_texto, encoding='utf-8')
    return divergiu


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--verificar', action='store_true', help='apenas confere se as tabelas estão atualizadas')
    args = ap.parse_args()
    total_marcadores, pendentes = 0, 0
    for md in sorted(BASE.rglob('*.md')):
        if '.git' in md.parts or '_modelo' in md.parts:
            continue
        texto = md.read_text(encoding='utf-8')
        if '<!-- TABELA:' not in texto:
            continue
        total_marcadores += len(MARCADOR.findall(texto))
        div = processar(md, args.verificar)
        for nome in div:
            pendentes += 1
            acao = 'desatualizada' if args.verificar else 'atualizada'
            print(f'{md.relative_to(BASE)}: tabela "{nome}" {acao}')
    print(f'{total_marcadores} tabelas conferidas; {pendentes} {"desatualizadas" if args.verificar else "atualizadas"}.')
    if args.verificar and pendentes:
        sys.exit(1)


if __name__ == '__main__':
    main()
