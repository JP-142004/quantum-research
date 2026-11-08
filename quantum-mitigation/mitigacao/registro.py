"""Sessões de dados: uma pasta por sessão, gravada uma vez e nunca editada.

  experimentos/NN_nome/dados/AAAA-MM-DD_computador/
      ficha.json      tudo o que identifica a sessão (gravada ao enviar)
      circuitos.qpy   os circuitos compilados, como foram enviados
      contagens.json  {nome: {bits: vezes}} (gravada ao coletar)
      coleta.json     quando foi coletada
"""
import importlib.metadata
import json
from datetime import datetime, timezone
from io import BytesIO
from pathlib import Path

from qiskit import qpy

EXPERIMENTOS = Path(__file__).resolve().parents[1] / 'experimentos'
PACOTES = ['numpy', 'qiskit', 'qiskit-aer', 'qiskit-ibm-runtime']


def agora():
    return datetime.now(timezone.utc).isoformat()


def versoes():
    saida = {}
    for pacote in PACOTES:
        try:
            saida[pacote] = importlib.metadata.version(pacote)
        except importlib.metadata.PackageNotFoundError:
            saida[pacote] = None
    return saida


def gravar_novo(caminho, conteudo):
    """Grava texto ou bytes e recusa sobrescrever um arquivo que já existe."""
    caminho = Path(caminho)
    if caminho.exists():
        raise FileExistsError(f'{caminho} já existe e não pode ser sobrescrito')
    temporario = caminho.with_name(caminho.name + '.tmp')
    if isinstance(conteudo, bytes):
        temporario.write_bytes(conteudo)
    else:
        temporario.write_text(conteudo, encoding='utf-8')
    temporario.replace(caminho)


def qpy_bytes(circuitos):
    buffer = BytesIO()
    qpy.dump(list(circuitos), buffer)
    return buffer.getvalue()


def validar_contagens(contagens, shots):
    for nome, c in contagens.items():
        tamanhos = {len(bits) for bits in c}
        if len(tamanhos) != 1 or any(set(bits) - {'0', '1'} for bits in c):
            raise ValueError(f'{nome}: sequências inválidas')
        if any(type(v) is not int or v < 0 for v in c.values()):
            raise ValueError(f'{nome}: contagem inválida')
        if sum(c.values()) != shots:
            raise ValueError(f'{nome}: soma {sum(c.values())}, esperado {shots}')


def registrar_envio(pasta, ficha, circuitos_compilados):
    """Cria a pasta da sessão (recusa se já existe) com a ficha e os circuitos."""
    Path(pasta).mkdir(parents=True, exist_ok=False)
    gravar_novo(Path(pasta) / 'ficha.json', json.dumps(ficha, ensure_ascii=False, indent=2) + '\n')
    gravar_novo(Path(pasta) / 'circuitos.qpy', qpy_bytes(circuitos_compilados))


def registrar_coleta(pasta, contagens, shots):
    validar_contagens(contagens, shots)
    gravar_novo(Path(pasta) / 'contagens.json', json.dumps(contagens, ensure_ascii=False, indent=2) + '\n')
    gravar_novo(Path(pasta) / 'coleta.json', json.dumps(dict(coletado_utc=agora())) + '\n')


def ler_sessao(pasta):
    """Devolve (ficha, contagens). contagens é None se a sessão ainda não foi coletada."""
    pasta = Path(pasta)
    ficha = json.loads((pasta / 'ficha.json').read_text(encoding='utf-8'))
    arquivo = pasta / 'contagens.json'
    contagens = json.loads(arquivo.read_text(encoding='utf-8')) if arquivo.exists() else None
    return ficha, contagens


def ler_circuitos(pasta):
    """Os circuitos compilados da sessão, na ordem do campo `ordem` da ficha."""
    with (Path(pasta) / 'circuitos.qpy').open('rb') as arquivo:
        return qpy.load(arquivo)


def listar_sessoes(pasta_experimento):
    dados = Path(pasta_experimento) / 'dados'
    return sorted(p for p in dados.iterdir() if (p / 'ficha.json').exists()) if dados.exists() else []
