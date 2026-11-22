"""Experimento 8, parte A: compara a matriz completa com as tabelas por qubit em 10 qubits.

Lê as sessões de dados/ (sem editá-las) e grava resultados/ e as tabelas do README.
Uso, a partir de quantum-mitigation/:   python experimentos/08_leitura_escala/a_simulador/analisar.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from mitigacao import leitura_escala_saida  # noqa: E402

if __name__ == '__main__':
    print(leitura_escala_saida.gerar(Path(__file__).resolve().parent))
