"""Caminhos das pastas do projeto, sempre relativos a este arquivo
(evita problemas com o acento em "Area de Trabalho")."""

import os

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # quantum-modeling/
DADOS = os.path.join(RAIZ, "dados")
HARDWARE = os.path.join(DADOS, "hardware")
CALIBRACAO = os.path.join(DADOS, "calibracao")
LISTA_JOBS = os.path.join(DADOS, "jobs_ghz.json")
RESULTADOS = os.path.join(RAIZ, "resultados")
