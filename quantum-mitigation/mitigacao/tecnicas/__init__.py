"""Registro de técnicas de mitigação.

Cada módulo desta pasta é uma técnica. Ele define NOME e as funções próprias dela
(por exemplo, quais circuitos extras ela precisa e como corrige as contagens).
Explicação de cada uma: fundamentos/tecnicas/<nome>.md.
"""
import importlib
import pkgutil


def listar():
    return sorted(m.name for m in pkgutil.iter_modules(__path__))


def obter(nome):
    return importlib.import_module(f'{__name__}.{nome}')
