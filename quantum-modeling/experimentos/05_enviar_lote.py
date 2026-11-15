"""
Passo 05: envia a IBM os circuitos de um lote (circuitos/<lote>.json).

Sem --enviar, so mostra os circuitos e o tempo de QPU estimado: nada e enviado.
Com --enviar, pede confirmacao, envia uma repeticao por job dentro de um Batch
e salva em dados/<lote>/ os job_ids e os circuitos exatamente como foram.
Com --teste-local, simula o "hardware" com o FakeKingston (sem gastar cota)
e grava em dados/<lote>_teste/, ja com as saidas prontas.

Uso:
  python experimentos/05_enviar_lote.py --lote lote01
  python experimentos/05_enviar_lote.py --lote lote01 --enviar
  python experimentos/05_enviar_lote.py --lote lote01 --teste-local
"""

import os
import sys
import shutil
import argparse
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from nucleo import lotes, registro, simulacao
from nucleo.dados_jobs import salvar_json


def mostrar(cfg, cadeia, sem_swaps, descricoes):
    print(f"\nLote {cfg['nome']} | backend {cfg['backend']} | {cfg['shots']} shots | "
          f"{cfg['repeticoes']} repeticao(oes)")
    print(f"Cadeia de {len(cadeia)} qubits fisicos: {cadeia}")
    if not sem_swaps:
        print("AVISO: a cadeia nao e uma linha de vizinhos; o GHZ maior tera SWAPs.")
    print(f"\n{'circuito':<22}{'n':>4}{'prof.':>7}{'2Q':>6}{'duracao':>12}")
    for d in descricoes:
        dur = f"{d['duracao_estimada_s'] * 1e6:.1f} us" if d["duracao_estimada_s"] else "?"
        print(f"{d['nome']:<22}{d['n']:>4}{d['profundidade']:>7}{d['portas_2q']:>6}{dur:>12}")
    seg = lotes.estimar_tempo_qpu(descricoes, cfg["shots"], cfg["repeticoes"])
    print(f"\n{len(descricoes)} circuitos por job x {cfg['repeticoes']} job(s)")
    print(f"Tempo de QPU estimado (grosseiro): ~{seg:.0f} s, sem contar o overhead da IBM por job")
    return seg


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--lote", required=True, help="nome do arquivo em circuitos/, sem .json")
    parser.add_argument("--enviar", action="store_true", help="envia de verdade (gasta cota)")
    parser.add_argument("--teste-local", action="store_true", help="simula o hardware com o FakeKingston")
    parser.add_argument("--limite-statevector", type=int, default=None,
                        help="no teste local: ate quantos qubits usar statevector (padrao 20)")
    args = parser.parse_args()

    cfg = lotes.carregar_config(args.lote)
    nome = args.lote + (lotes.SUFIXO_TESTE if args.teste_local else "")
    pasta = lotes.pasta_lote(nome)

    if args.teste_local:
        from qiskit_ibm_runtime.fake_provider import FakeKingston
        backend = FakeKingston()
        shutil.rmtree(pasta, ignore_errors=True)
    else:
        if os.path.exists(os.path.join(pasta, "envio.json")):
            sys.exit(f"O lote '{nome}' ja foi enviado ({pasta}). Para um lote novo, crie outro "
                     f"arquivo em circuitos/ (ex.: lote02.json).")
        from qiskit_ibm_runtime import QiskitRuntimeService
        service = QiskitRuntimeService()
        backend = service.backend(cfg["backend"])

    n_max = max(cfg["tamanhos_ghz"])
    if cfg.get("qubits_fisicos"):
        cadeia, sem_swaps = cfg["qubits_fisicos"], True
    else:
        cadeia, sem_swaps = lotes.escolher_cadeia(backend, n_max)
    descricoes, isas = lotes.transpilar_lote(cfg, backend, cadeia)
    segundos = mostrar(cfg, cadeia, sem_swaps, descricoes)

    if not (args.enviar or args.teste_local):
        print("\nNada foi enviado. Para enviar: acrescente --enviar")
        return

    envio = {
        "lote": nome,
        "config": cfg,
        "backend": backend.name,
        "cadeia_qubits_fisicos": cadeia,
        "circuitos": descricoes,
        "tempo_qpu_estimado_s": segundos,
        "enviado_em": datetime.now().astimezone(),
        "commit_git": registro.commit_git(),
        "versoes": registro.versoes(),
        "opcoes_sampler": {"dynamical_decoupling": False, "twirling_portas": False,
                           "twirling_medidas": False},
        "jobs": [],
    }

    if args.teste_local:
        simular_hardware_local(nome, cfg, backend, descricoes, isas, envio, args.limite_statevector)
        return

    resposta = input(f"\nEnviar {cfg['repeticoes']} job(s) para o {backend.name}? "
                     f"Isso gasta cota da IBM. Digite ENVIAR para confirmar: ")
    if resposta.strip() != "ENVIAR":
        print("Cancelado. Nada foi enviado.")
        return

    # SamplerV2 esta marcado como obsoleto no qiskit-ibm-runtime 0.50, mas segue
    # funcionando por pelo menos 3 meses. Trocar pelo novo Sampler quando sair.
    from qiskit_ibm_runtime import Batch, SamplerV2
    with Batch(backend=backend) as batch:
        sampler = SamplerV2(mode=batch)
        sampler.options.dynamical_decoupling.enable = False
        sampler.options.twirling.enable_gates = False
        sampler.options.twirling.enable_measure = False
        for r in range(1, cfg["repeticoes"] + 1):
            job = sampler.run(isas, shots=cfg["shots"])
            envio["jobs"].append({"job_id": job.job_id(), "repeticao": r})
            print(f"  repeticao {r}: job {job.job_id()}")
            lotes.salvar_envio(nome, envio, isas)  # salva a cada job enviado
        envio["batch_id"] = batch.session_id
    lotes.salvar_envio(nome, envio, isas)
    print(f"\nEnviado. Registro em {pasta}")
    print(f"Quando os jobs terminarem: python experimentos/06_baixar_saidas_lote.py --lote {nome}")


def simular_hardware_local(nome, cfg, backend, descricoes, isas, envio, limite=None):
    """Gera saidas falsas com o modelo de ruido do FakeKingston (so para testar o fluxo)."""
    from qiskit_aer.noise import NoiseModel
    modelo = NoiseModel.from_backend(backend)
    saidas = lotes.carregar_saidas(nome)
    for r in range(1, cfg["repeticoes"] + 1):
        job_id = f"local-r{r}"
        envio["jobs"].append({"job_id": job_id, "repeticao": r})
        contagens = {}
        for d, isa in zip(descricoes, isas):
            metodo = simulacao.escolher_metodo(d["n"], limite)
            contagens[d["nome"]], _, _ = simulacao.simular(isa, modelo, cfg["shots"],
                                                            simulacao.seed_independente(1000, r), metodo)
        lotes.registrar_saida_job(nome, saidas, job_id, r, backend, backend.properties(),
                                  "FakeKingston (teste local)", contagens, {})
        print(f"  repeticao {r}: simulada ({job_id})")
    lotes.salvar_envio(nome, envio, isas)
    print(f"\nTeste local gravado em {lotes.pasta_lote(nome)}")


if __name__ == "__main__":
    main()
