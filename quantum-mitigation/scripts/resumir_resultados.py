"""Recalcula as tabelas de resumo dos experimentos 1 e 4. Não acessa a IBM nem envia circuitos."""
import csv
import json
import re
from pathlib import Path

import numpy as np

BASE = Path(__file__).resolve().parents[1]
SAIDA = BASE / 'dados' / 'processados'


def salvar(nome, linhas):
    """nome é relativo a dados/processados, por exemplo '01_ghz_escala/resumo_escala.csv'."""
    with (SAIDA / nome).open('w', newline='', encoding='utf-8') as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=list(linhas[0]))
        escritor.writeheader()
        escritor.writerows(linhas)


def escala():
    texto = (BASE / 'dados/brutos/01_ghz_escala/ghz_05_a_50.txt').read_text(encoding='utf-8')
    secoes = re.split(r'^\s*(\d+)\s+QUBITS\s*$', texto, flags=re.M)
    linhas = []
    for tamanho, bloco in zip(secoes[1::2], secoes[2::2]):
        n = int(tamanho)
        pares = re.findall(r'^\s*([01]{5,})\s*:?\s+(\d+)\s*$', bloco, flags=re.M)
        counts = {}
        for bits, quantidade in pares:
            if len(bits) != n or bits in counts:
                raise ValueError(f'Contagem inválida na seção de {n} qubits')
            counts[bits] = int(quantidade)
        total = sum(counts.values())
        if total != 1000:
            raise ValueError(f'Total inesperado em {n} qubits: {total}')
        zeros, uns = counts.get('0' * n, 0), counts.get('1' * n, 0)
        linhas.append(dict(qubits=n, shots=total, todos_zeros=zeros,
                           todos_uns=uns, outros=total-zeros-uns, populacao_z=(zeros+uns)/total))
    if [linha['qubits'] for linha in linhas] != list(range(5, 51, 5)):
        raise ValueError('Esperadas dez seções de 5 a 50 qubits')
    salvar('01_ghz_escala/resumo_escala.csv', linhas)


def mitigacao():
    linhas = []
    pasta = BASE / 'dados/brutos/04_mitigacao_leitura'
    arquivos = sorted(pasta.glob('*.json')) + [pasta / 'rodada_03/rodada_03.json']
    for rodada, caminho in enumerate(arquivos, 1):
        dados = json.loads(caminho.read_text(encoding='utf-8'))
        counts = dados['contagens']
        n = len(dados['qubits'])
        dim = 2 ** n
        esperados = {f'cal_{i:0{n}b}' for i in range(dim)} | {'GHZ_Z', 'GHZ_X'}
        if set(counts) != esperados:
            raise ValueError(f'Circuitos inesperados em {caminho.name}')

        def vetor(nome):
            v = np.zeros(dim)
            for bits, quantidade in counts[nome].items():
                if len(bits) != n or set(bits) - {'0', '1'} or quantidade < 0:
                    raise ValueError(f'Contagem inválida: {nome}')
                v[int(bits, 2)] += quantidade
            if v.sum() != dados['shots_por_circuito']:
                raise ValueError(f'Total inesperado: {nome}')
            return v / v.sum()

        matriz = np.column_stack([vetor(f'cal_{i:0{n}b}') for i in range(dim)])
        observado = np.column_stack([vetor('GHZ_Z'), vetor('GHZ_X')])
        ajustado = np.linalg.solve(matriz, observado)
        paridade = np.array([(-1) ** i.bit_count() for i in range(dim)])
        linhas.append(dict(rodada=rodada, job_id=dados['job_id'], backend=dados['backend'],
                           populacao_z_bruta=observado[[0, -1], 0].sum(),
                           populacao_z_ajustada=ajustado[[0, -1], 0].sum(),
                           correlacao_x_bruta=paridade @ observado[:, 1],
                           correlacao_x_ajustada=paridade @ ajustado[:, 1],
                           condicionamento=np.linalg.cond(matriz),
                           menor_quasi_z=ajustado[:, 0].min(),
                           menor_quasi_x=ajustado[:, 1].min()))
    if len(linhas) != 3:
        raise ValueError('Esperadas as três rodadas da calibração de leitura')
    salvar('04_mitigacao_leitura/resumo_mitigacao.csv', linhas)


if __name__ == '__main__':
    for pasta in ('01_ghz_escala', '04_mitigacao_leitura'):
        (SAIDA / pasta).mkdir(parents=True, exist_ok=True)
    escala()
    mitigacao()
    print(f'Tabelas recalculadas em: {SAIDA}')
