"""Baixa os jobs da IBM uma unica vez e depois le tudo do disco (sem internet).

Para cada job ficam salvos em dados/hardware/ghzNN_<job_id>/:
  circuito.qpy    circuito ISA exatamente como foi executado
  contagens.json  contagens reais do hardware
  info.json       procedencia: datas, opcoes do job, layout, checagens
e em dados/calibracao/ o snapshot de calibracao usado (<id>.json) e a
configuracao do backend (<backend>_configuracao.json).
"""

import os
import json
from datetime import datetime

from qiskit import qpy
from qiskit_ibm_runtime.models import BackendProperties, QasmBackendConfiguration

from . import caminhos

OPERACOES_SEM_ERRO = {"barrier", "delay", "measure", "reset"}


# ---------------------------------------------------------------- utilidades

def _json_padrao(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    return str(obj)


def salvar_json(caminho, dados):
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=2, ensure_ascii=False, default=_json_padrao)


def ler_json(caminho):
    with open(caminho, "r", encoding="utf-8") as f:
        return json.load(f)


def carregar_lista_jobs():
    return ler_json(caminhos.LISTA_JOBS)["jobs"]


def pasta_job(tamanho, job_id):
    return os.path.join(caminhos.HARDWARE, f"ghz{tamanho:02d}_{job_id}")


def _para_datetime(valor):
    if valor is None or isinstance(valor, datetime):
        return valor
    return datetime.fromisoformat(str(valor).replace("Z", "+00:00"))


def _horas_entre(inicio, fim):
    """Horas de inicio ate fim (positivo = calibracao anterior a execucao)."""
    try:
        return round((fim - inicio).total_seconds() / 3600, 2)
    except Exception:
        return None


# ---------------------------------------------------------------- circuito

def descrever_circuito(circ):
    """Informacoes do circuito ISA pedidas no manifesto (feedback, item 6)."""
    idx = lambda b: circ.find_bit(b).index
    ativos = sorted({idx(q) for ins in circ.data if ins.operation.name not in ("barrier", "delay")
                     for q in ins.qubits})
    medicoes = [{"qubit_fisico": idx(ins.qubits[0]), "bit_classico": idx(ins.clbits[0])}
                for ins in circ.data if ins.operation.name == "measure"]
    layout = None
    if circ.layout is not None:
        layout = list(circ.layout.initial_index_layout(filter_ancillas=True))
    return {
        "qubits_no_circuito": circ.num_qubits,
        "bits_classicos": circ.num_clbits,
        "registradores_classicos": [r.name for r in circ.cregs],
        "profundidade": circ.depth(lambda ins: ins.operation.name != "barrier"),
        "profundidade_2q": circ.depth(lambda ins: ins.operation.num_qubits == 2),
        "portas_2q": sum(1 for ins in circ.data if ins.operation.num_qubits == 2),
        "contagem_operacoes": dict(circ.count_ops()),
        "qubits_fisicos_usados": ativos,
        "layout_inicial": layout,
        "medicoes": medicoes,
    }


def checar_consistencia(tamanho, n_pubs, registradores, nome_registrador, counts, circ_info, propriedades):
    """Confere se circuito, execucao e leitura batem (feedback, item 2).
    Devolve a lista de avisos (vazia = tudo certo)."""
    avisos = []
    if n_pubs != 1:
        avisos.append(f"job tem {n_pubs} PUBs; foi usado o primeiro")
    if len(registradores) != 1:
        avisos.append(f"resultado tem registradores {registradores}; foi usado '{nome_registrador}'")
    tamanhos_chaves = {len(k) for k in counts}
    if tamanhos_chaves != {tamanho}:
        avisos.append(f"cadeias com comprimento {sorted(tamanhos_chaves)}, esperado {tamanho}")
    if len(circ_info["medicoes"]) != tamanho:
        avisos.append(f"circuito mede {len(circ_info['medicoes'])} qubits, esperado {tamanho}")
    portas_calibradas = {g.gate for g in propriedades.gates}
    sem_calibracao = sorted(set(circ_info["contagem_operacoes"]) - portas_calibradas - OPERACOES_SEM_ERRO)
    if sem_calibracao:
        avisos.append(f"portas sem erro na calibracao (o modelo trata como ideais): {sem_calibracao}")
    qubits_calibrados = len(propriedades.qubits)
    fora = [q for q in circ_info["qubits_fisicos_usados"] if q >= qubits_calibrados]
    if fora:
        avisos.append(f"qubits sem calibracao: {fora}")
    return avisos


# ---------------------------------------------------------------- calibracao

def obter_calibracao(job, service, backend_name, momento):
    """Tenta, em ordem: (1) a calibracao anexada ao proprio job,
    (2) a calibracao historica do backend no momento do job,
    (3) a calibracao atual (defasada, fica marcado)."""
    try:
        props = job.properties()
        if props is not None:
            return props, "job.properties (calibracao anexada ao job)"
    except Exception as e:
        print(f"    job.properties() falhou: {e}")
    backend = service.backend(backend_name)
    try:
        props = backend.properties(datetime=momento)
        if props is not None:
            return props, "backend.properties(datetime=momento do job)"
    except Exception as e:
        print(f"    backend.properties(datetime=...) falhou: {e}")
    return backend.properties(), "backend.properties() ATUAL (defasada em relacao ao job)"


def id_calibracao(propriedades):
    data = _para_datetime(propriedades.last_update_date)
    return f"{propriedades.backend_name}_{data.strftime('%Y%m%dT%H%M%S%z')}"


def salvar_calibracao(propriedades, origem):
    cid = id_calibracao(propriedades)
    caminho = os.path.join(caminhos.CALIBRACAO, f"{cid}.json")
    if not os.path.exists(caminho):
        salvar_json(caminho, {
            "id": cid,
            "origem": origem,
            "backend": propriedades.backend_name,
            "last_update_date": propriedades.last_update_date,
            "propriedades": propriedades.to_dict(),
        })
    return cid


def salvar_configuracao(backend):
    """Configuracao fixa do backend (portas, acoplamento, dt). Junto com a
    calibracao, permite reconstruir o Target sem acessar a IBM."""
    caminho = os.path.join(caminhos.CALIBRACAO, f"{backend.name}_configuracao.json")
    if not os.path.exists(caminho):
        salvar_json(caminho, backend.configuration().to_dict())


def carregar_configuracao(backend_name):
    dados = ler_json(os.path.join(caminhos.CALIBRACAO, f"{backend_name}_configuracao.json"))
    return QasmBackendConfiguration.from_dict(dados)


def carregar_calibracao(cid):
    dados = ler_json(os.path.join(caminhos.CALIBRACAO, f"{cid}.json"))
    return BackendProperties.from_dict(dados["propriedades"]), dados


# ---------------------------------------------------------------- download

def baixar_job(service, job_id, tamanho):
    job = service.job(job_id)
    backend = job.backend()
    backend_name = backend.name
    salvar_configuracao(backend)
    resultado = job.result()
    inputs = job.inputs
    pubs = inputs["pubs"]
    circ = pubs[0][0]

    data = resultado[0].data
    registradores = list(data.keys())
    nome_reg = "c" if "c" in registradores else registradores[0]
    counts = getattr(data, nome_reg).get_counts()

    timestamps = {}
    try:
        timestamps = job.metrics().get("timestamps", {}) or {}
    except Exception as e:
        print(f"    job.metrics() falhou: {e}")
    criacao = job.creation_date
    execucao = _para_datetime(timestamps.get("running")) or criacao

    props, origem = obter_calibracao(job, service, backend_name, execucao)
    cid = salvar_calibracao(props, origem)
    data_calib = _para_datetime(props.last_update_date)

    circ_info = descrever_circuito(circ)
    avisos = checar_consistencia(tamanho, len(pubs), registradores, nome_reg, counts, circ_info, props)

    pasta = pasta_job(tamanho, job_id)
    os.makedirs(pasta, exist_ok=True)
    with open(os.path.join(pasta, "circuito.qpy"), "wb") as f:
        qpy.dump(circ, f)
    salvar_json(os.path.join(pasta, "contagens.json"), counts)
    info = {
        "job_id": job_id,
        "tamanho_ghz": tamanho,
        "backend": backend_name,
        "data_criacao": criacao,
        "timestamps_execucao": timestamps,
        "registrador_usado": nome_reg,
        "opcoes_do_job": {k: v for k, v in inputs.items() if k != "pubs"},
        "calibracao": {
            "id": cid,
            "origem": origem,
            "data_calibracao": data_calib,
            "defasagem_horas": _horas_entre(data_calib, execucao),
        },
        "circuito": circ_info,
        "avisos": avisos,
    }
    salvar_json(os.path.join(pasta, "info.json"), info)
    return info


# ---------------------------------------------------------------- leitura local

def job_ja_baixado(tamanho, job_id):
    pasta = pasta_job(tamanho, job_id)
    return all(os.path.exists(os.path.join(pasta, a)) for a in ("circuito.qpy", "contagens.json", "info.json"))


def carregar_job_local(tamanho, job_id):
    """Tudo o que uma simulacao precisa, lido do disco."""
    pasta = pasta_job(tamanho, job_id)
    if not job_ja_baixado(tamanho, job_id):
        raise FileNotFoundError(
            f"GHZ-{tamanho} ({job_id}) ainda nao foi baixado. Rode antes: python experimentos/01_baixar_dados.py")
    with open(os.path.join(pasta, "circuito.qpy"), "rb") as f:
        circ = qpy.load(f)[0]
    info = ler_json(os.path.join(pasta, "info.json"))
    propriedades, _ = carregar_calibracao(info["calibracao"]["id"])
    return {
        "circuito": circ,
        "counts_real": ler_json(os.path.join(pasta, "contagens.json")),
        "info": info,
        "propriedades": propriedades,
        "configuracao": carregar_configuracao(info["backend"]),
    }
