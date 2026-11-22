"""Experimento 8, parte B: analisa as sessões da IBM (10 e 20 qubits, calibração por qubit).

Lê as sessões de dados/ (sem editá-las) e grava resultados/ e as tabelas do README.
Uso, a partir de quantum-mitigation/:   python experimentos/08_leitura_escala/b_ibm/analisar.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from mitigacao import leitura_ibm_saida  # noqa: E402

if __name__ == '__main__':
    print(leitura_ibm_saida.gerar(Path(__file__).resolve().parent))
