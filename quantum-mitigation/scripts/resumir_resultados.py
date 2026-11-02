"""Recalcula a tabela de PZ do experimento 1. Não acessa a IBM nem envia circuitos."""
import csv
import re
from pathlib import Path

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


if __name__ == '__main__':
    (SAIDA / '01_ghz_escala').mkdir(parents=True, exist_ok=True)
    escala()
    print(f'Tabela recalculada em: {SAIDA / "01_ghz_escala"}')
