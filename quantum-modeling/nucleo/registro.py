"""Uma pasta por execucao em resultados/, com manifesto (feedback, item 6)."""

import os
import platform
import subprocess
from datetime import datetime
from importlib.metadata import version, PackageNotFoundError

from . import caminhos

PACOTES = ["qiskit", "qiskit-aer", "qiskit-ibm-runtime", "numpy", "scipy"]


def versoes():
    v = {"python": platform.python_version()}
    for p in PACOTES:
        try:
            v[p] = version(p)
        except PackageNotFoundError:
            v[p] = None
    return v


def commit_git():
    """Commit atual do repositorio (e se ha alteracoes nao commitadas)."""
    try:
        h = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], cwd=caminhos.RAIZ, text=True).strip()
        sujo = subprocess.check_output(["git", "status", "--porcelain"], cwd=caminhos.RAIZ, text=True).strip()
        return h + ("-com-alteracoes-locais" if sujo else "")
    except Exception:
        return None


def nova_pasta_execucao(nome):
    carimbo = datetime.now().strftime("%Y-%m-%d_%H%M")
    pasta = os.path.join(caminhos.RESULTADOS, f"{carimbo}_{nome}")
    os.makedirs(pasta, exist_ok=False)
    return pasta


def ultima_pasta_execucao(nome):
    """Pasta mais recente de resultados/ que termina com _<nome>."""
    pastas = sorted(p for p in os.listdir(caminhos.RESULTADOS) if p.endswith(f"_{nome}"))
    if not pastas:
        raise FileNotFoundError(f"nenhuma execucao '{nome}' em {caminhos.RESULTADOS}")
    return os.path.join(caminhos.RESULTADOS, pastas[-1])
