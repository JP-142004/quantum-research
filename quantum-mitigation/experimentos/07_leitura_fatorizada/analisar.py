"""Experimento 7: compara a calibração de leitura completa com os modelos por qubit.

Não tem `dados/` próprio: lê as sessões do experimento 4 (sem editá-las) e grava em `resultados/`.
Uso, a partir de quantum-mitigation/:   python experimentos/07_leitura_fatorizada/analisar.py
"""
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ))

from mitigacao import leitura_saida  # noqa: E402

if __name__ == '__main__':
    pasta = Path(__file__).resolve().parent
    print(leitura_saida.gerar(pasta, RAIZ / 'experimentos' / '04_calibracao_leitura'))
