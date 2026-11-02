#!/usr/bin/env python3
"""Confere os links relativos dos arquivos Markdown (arquivos e âncoras).

Uso: python scripts/verificar_links.py [pasta]   (padrão: o repositório inteiro)
Não acessa a rede nem a IBM. Sai com erro se algum link estiver quebrado.
"""
import re
import sys
import unicodedata
from pathlib import Path
from urllib.parse import unquote

RAIZ = Path(__file__).resolve().parents[2]
LINK = re.compile(r'(?<!\!)\[[^\]]*\]\(([^)\s]+)(?:\s+"[^"]*")?\)|!\[[^\]]*\]\(([^)\s]+)\)')
CERCA = re.compile(r'^```.*?^```', re.S | re.M)


def ancora(titulo):
    """Gera a âncora no estilo do GitHub."""
    t = re.sub(r'[`*_]', '', titulo.strip().lower())
    t = re.sub(r'[^\w\s-]', '', t, flags=re.U)
    return re.sub(r'\s', '-', t)


def ancoras(arquivo):
    texto = CERCA.sub('', arquivo.read_text(encoding='utf-8'))
    return {ancora(m.group(2)) for m in re.finditer(r'^(#{1,6})\s+(.*)$', texto, re.M)}


def main():
    base = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else RAIZ
    quebrados, total = [], 0
    cache = {}
    for md in sorted(base.rglob('*.md')):
        if '.git' in md.parts:
            continue
        texto = CERCA.sub('', md.read_text(encoding='utf-8'))
        texto = re.sub(r'`[^`\n]*`', '', texto)
        for m in LINK.finditer(texto):
            alvo = m.group(1) or m.group(2)
            if re.match(r'^(https?:|mailto:)', alvo):
                continue
            total += 1
            caminho, _, frag = alvo.partition('#')
            destino = md if not caminho else (md.parent / unquote(caminho)).resolve()
            if not destino.exists():
                quebrados.append((md, alvo, 'arquivo inexistente'))
            elif frag and destino.suffix == '.md':
                if destino not in cache:
                    cache[destino] = ancoras(destino)
                if unquote(frag).lower() not in cache[destino]:
                    quebrados.append((md, alvo, 'âncora inexistente'))
    for md, alvo, motivo in quebrados:
        print(f'{md.relative_to(RAIZ)}: {alvo} ({motivo})')
    print(f'{total} links relativos conferidos; {len(quebrados)} quebrados.')
    sys.exit(1 if quebrados else 0)


if __name__ == '__main__':
    main()
