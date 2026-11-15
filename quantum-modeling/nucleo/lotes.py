"""Lotes de circuitos enviados a IBM.

circuitos/<lote>.json        o que enviar (configuracao)
dados/<lote>/envio.json      job_ids, cadeia de qubits, descricao de cada circuito
dados/<lote>/circuitos.qpy   circuitos ISA exatamente como foram enviados
dados/<lote>/saidas.json     so as saidas do hardware: contagens por circuito e por job
dados/<lote>/calibracao/     calibracao de cada job
"""

import os
from datetime import datetime

from qiskit import qpy, transpile

from . import caminhos, circuitos
from .dados_jobs import (ler_json, salvar_json, obter_calibracao, salvar_calibracao,
                         salvar_configuracao, carregar_calibracao, carregar_configuracao,
                         _para_datetime, _horas_entre)

SEED_TRANSPILADOR = 42
REP_DELAY_S = 250e-6  # espera tipica entre shots nos processadores Heron (para a estimativa)
SUFIXO_TESTE = "_teste"


def carregar_config(nome):
    base = nome[:-len(SUFIXO_TESTE)] if nome.endswith(SUFIXO_TESTE) else nome
    return ler_json(os.path.join(caminhos.RAIZ, "circuitos", f"{base}.json"))


def pasta_lote(nome):
    return os.path.join(caminhos.DADOS, nome)


def pasta_calibracao(nome):
    return os.path.join(pasta_lote(nome), "calibracao")


# ---------------------------------------------------------------- montagem

def escolher_cadeia(backend, n):
    """Cadeia de n qubits fisicos vizinhos escolhida pelo transpilador para um GHZ-n.
    Devolve (cadeia, sem_swaps)."""
    isa = transpile(circuitos.ghz(n), backend, optimization_level=3, seed_transpiler=SEED_TRANSPILADOR)
    cadeia = list(isa.layout.initial_index_layout(filter_ancillas=True))
    portas_2q = sum(1 for ins in isa.data if ins.operation.num_qubits == 2)
    return cadeia, portas_2q == n - 1


def transpilar_lote(cfg, backend, cadeia):
    """Cada circuito usa os primeiros n qubits da mesma cadeia."""
    descricoes, isas = [], []
    for desc, circ in circuitos.montar_lote(cfg):
        isa = transpile(circ, backend, initial_layout=cadeia[:desc["n"]],
                        optimization_level=1, seed_transpiler=SEED_TRANSPILADOR)
        desc = dict(desc)
        desc["qubits_fisicos"] = cadeia[:desc["n"]]
        desc["profundidade"] = isa.depth(lambda ins: ins.operation.name != "barrier")
        desc["portas_2q"] = sum(1 for ins in isa.data if ins.operation.num_qubits == 2)
        try:
            desc["duracao_estimada_s"] = isa.estimate_duration(backend.target, unit="s")
        except Exception:
            desc["duracao_estimada_s"] = None
        descricoes.append(desc)
        isas.append(isa)
    return descricoes, isas


def estimar_tempo_qpu(descricoes, shots, repeticoes):
    """Estimativa grosseira: shots x (duracao do circuito + espera entre shots)."""
    por_job = sum(shots * ((d["duracao_estimada_s"] or 0) + REP_DELAY_S) for d in descricoes)
    return por_job * repeticoes


# ---------------------------------------------------------------- envio

def salvar_envio(nome, envio, isas):
    pasta = pasta_lote(nome)
    os.makedirs(pasta, exist_ok=True)
    with open(os.path.join(pasta, "circuitos.qpy"), "wb") as f:
        qpy.dump(isas, f)
    salvar_json(os.path.join(pasta, "envio.json"), envio)


def carregar_envio(nome):
    pasta = pasta_lote(nome)
    envio = ler_json(os.path.join(pasta, "envio.json"))
    with open(os.path.join(pasta, "circuitos.qpy"), "rb") as f:
        isas = qpy.load(f)
    return envio, isas


# ---------------------------------------------------------------- saidas

def caminho_saidas(nome):
    return os.path.join(pasta_lote(nome), "saidas.json")


def carregar_saidas(nome):
    caminho = caminho_saidas(nome)
    if os.path.exists(caminho):
        return ler_json(caminho)
    return {"lote": nome, "jobs": []}


def registrar_saida_job(nome, saidas, job_id, repeticao, backend, propriedades, origem_calibracao,
                        contagens_por_circuito, timestamps):
    """Guarda as contagens de um job e a calibracao usada, e salva o saidas.json."""
    cid = salvar_calibracao(propriedades, origem_calibracao, pasta=pasta_calibracao(nome))
    salvar_configuracao(backend, pasta=pasta_calibracao(nome))
    execucao = _para_datetime(timestamps.get("running")) if timestamps else None
    saidas["jobs"] = [j for j in saidas["jobs"] if j["job_id"] != job_id]
    saidas["jobs"].append({
        "job_id": job_id,
        "repeticao": repeticao,
        "backend": backend.name,
        "timestamps": timestamps,
        "calibracao": {
            "id": cid,
            "origem": origem_calibracao,
            "defasagem_horas": _horas_entre(_para_datetime(propriedades.last_update_date), execucao)
            if execucao else None,
        },
        "contagens": contagens_por_circuito,
    })
    saidas["jobs"].sort(key=lambda j: j["repeticao"])
    saidas["atualizado_em"] = datetime.now().astimezone()
    salvar_json(caminho_saidas(nome), saidas)


def baixar_job(service, nome, saidas, item, descricoes):
    """Baixa as contagens de um job do lote, se ele ja terminou. Devolve o status."""
    job = service.job(item["job_id"])
    status = str(job.status())
    if status not in ("DONE", "JobStatus.DONE"):
        return status
    resultado = job.result()
    if len(resultado) != len(descricoes):
        raise ValueError(f"job tem {len(resultado)} resultados, esperado {len(descricoes)}")
    contagens = {d["nome"]: resultado[k].data.c.get_counts() for k, d in enumerate(descricoes)}
    try:
        timestamps = job.metrics().get("timestamps", {}) or {}
    except Exception:
        timestamps = {}
    backend = job.backend()
    momento = _para_datetime(timestamps.get("running")) or job.creation_date
    props, origem = obter_calibracao(job, service, backend.name, momento)
    registrar_saida_job(nome, saidas, item["job_id"], item["repeticao"], backend, props, origem,
                        contagens, timestamps)
    return "DONE"


def calibracao_do_job(nome, job):
    """(propriedades, configuracao) da calibracao registrada para um job."""
    props, _ = carregar_calibracao(job["calibracao"]["id"], pasta=pasta_calibracao(nome))
    conf = carregar_configuracao(job["backend"], pasta=pasta_calibracao(nome))
    return props, conf
