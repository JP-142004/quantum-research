"""
Passo 07: ajusta o modelo em UM circuito do lote e aplica aos demais (offline).

1. Ajuste: evolucao diferencial encontra os 6 multiplicadores do Nivel 1
   (erro 1Q, erro 2Q, leitura 1|0, leitura 0|1, T1, T2) que minimizam a
   Hellinger no circuito de ajuste (circuito_de_ajuste em circuitos/<lote>.json).
2. Validacao: os mesmos multiplicadores sao aplicados a calibracao de cada job
   e comparados, em todos os outros circuitos e repeticoes, com o Nivel 0.
3. Referencias de variabilidade:
   - simulacao x simulacao: o mesmo modelo com outra seed (efeito so dos shots);
   - hardware x hardware: a mesma saida entre repeticoes (variacao do hardware).

Uso:
  python experimentos/07_analisar_lote.py --lote lote01 --rapido   # teste: poucas geracoes
  python experimentos/07_analisar_lote.py --lote lote01
"""

import os
import sys
import time
import argparse
from itertools import combinations
from datetime import datetime

import numpy as np
from scipy.optimize import differential_evolution
from qiskit.quantum_info import hellinger_distance

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from nucleo import lotes, metricas, modelos_ruido, registro, simulacao
from nucleo.dados_jobs import salvar_json

SEED_PADRAO = 1234
CONFIG_DE = {
    "rapido": {"maxiter": 2, "popsize": 4, "polish": False},
    "completo": {"maxiter": 20, "popsize": 10, "polish": True},
}


def comparar(desc, real, sim):
    if desc["tipo"] == "leitura":
        return metricas.comparar_leitura(real, sim, desc["n"], desc["estado"])
    if desc["tipo"] == "paridade":
        return metricas.comparar_paridade(real, sim)
    return metricas.comparar(real, sim, desc["n"])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--lote", required=True)
    parser.add_argument("--rapido", action="store_true", help="poucas geracoes, para medir o tempo")
    parser.add_argument("--seed", type=int, default=SEED_PADRAO, help="seed do simulador")
    parser.add_argument("--limite-statevector", type=int, default=None,
                        help="ate quantos qubits usar statevector (padrao 20; acima, MPS)")
    args = parser.parse_args()

    envio, isas = lotes.carregar_envio(args.lote)
    saidas = lotes.carregar_saidas(args.lote)
    if not saidas["jobs"]:
        sys.exit("Nenhuma saida baixada ainda. Rode antes o 06_baixar_saidas_lote.py")
    cfg = envio["config"]
    descricoes = envio["circuitos"]
    indice = {d["nome"]: k for k, d in enumerate(descricoes)}
    cadeia = envio["cadeia_qubits_fisicos"]
    seed = args.seed

    def rodar(nome_circ, modelo, s=seed):
        d = descricoes[indice[nome_circ]]
        counts, seg, config = simulacao.simular(isas[indice[nome_circ]], modelo, cfg["shots"], s,
                                                simulacao.escolher_metodo(d["n"], args.limite_statevector))
        return counts, seg, config

    # ------------------------------------------------------------ 1. ajuste
    ajuste = cfg["circuito_de_ajuste"]
    job_ajuste = next((j for j in saidas["jobs"] if j["repeticao"] == ajuste["repeticao"]), None)
    if job_ajuste is None:
        sys.exit(f"A repeticao {ajuste['repeticao']} (usada no ajuste) ainda nao foi baixada.")
    props, _ = lotes.calibracao_do_job(args.lote, job_ajuste)
    calib_ajuste = modelos_ruido.calibracao_media(props, cadeia)

    avaliacoes = [0]

    def aptidao(escalas):
        modelo = modelos_ruido.nivel1(escalas, calib_ajuste)
        h = float(np.mean([hellinger_distance(job_ajuste["contagens"][c], rodar(c, modelo)[0])
                           for c in ajuste["circuitos"]]))
        avaliacoes[0] += 1
        if avaliacoes[0] % 10 == 0:
            print(f"    {avaliacoes[0]} avaliacoes | ultima Hellinger = {h:.4f}", flush=True)
        return h

    modo = "rapido" if args.rapido else "completo"
    print(f"Ajuste ({modo}) em {ajuste['circuitos']}, repeticao {ajuste['repeticao']}")
    inicio = time.perf_counter()
    res = differential_evolution(aptidao, modelos_ruido.LIMITES, seed=42, workers=1, **CONFIG_DE[modo])
    tempo_ajuste = time.perf_counter() - inicio
    escalas = [float(x) for x in res.x]
    print(f"  {avaliacoes[0]} avaliacoes em {tempo_ajuste:.0f} s "
          f"({tempo_ajuste / avaliacoes[0]:.2f} s cada) | Hellinger no ajuste = {res.fun:.4f}")
    for g, v in zip(modelos_ruido.GENES, escalas):
        print(f"    {g:<18} x {v:.3f}")
    if args.rapido:
        n_completo = (CONFIG_DE["completo"]["maxiter"] + 1) * CONFIG_DE["completo"]["popsize"] * len(escalas)
        print(f"  Estimativa do modo completo: ~{n_completo} avaliacoes, "
              f"~{n_completo * tempo_ajuste / avaliacoes[0] / 60:.0f} min (+ polimento)")

    # ------------------------------------------------------------ 2. validacao
    pasta = registro.nova_pasta_execucao(f"{args.lote}_analise")
    manifesto = {
        "lote": args.lote, "inicio": datetime.now().astimezone(), "commit_git": registro.commit_git(),
        "versoes": registro.versoes(), "seed_simulador": seed, "modo_ajuste": modo,
        "limite_statevector": args.limite_statevector or simulacao.LIMITE_STATEVECTOR,
        "config_evolucao_diferencial": CONFIG_DE[modo], "circuito_de_ajuste": ajuste,
        "genes": modelos_ruido.GENES, "limites": modelos_ruido.LIMITES,
        "escalas_ajustadas": dict(zip(modelos_ruido.GENES, escalas)),
        "hellinger_no_ajuste": float(res.fun), "avaliacoes": avaliacoes[0],
        "tempo_ajuste_s": tempo_ajuste, "calibracao_media_do_ajuste": calib_ajuste,
    }
    linhas = []

    def salvar():
        salvar_json(os.path.join(pasta, "resultados.json"), linhas)
        salvar_json(os.path.join(pasta, "manifesto.json"), manifesto)

    print("\nAplicando aos demais circuitos e repeticoes...")
    for job in saidas["jobs"]:
        props, conf = lotes.calibracao_do_job(args.lote, job)
        modelo0 = modelos_ruido.nivel0(props, conf)
        modelo1 = modelos_ruido.nivel1(escalas, modelos_ruido.calibracao_media(props, cadeia))
        for d in descricoes:
            nome = d["nome"]
            real = job["contagens"][nome]
            sim0, seg0, config = rodar(nome, modelo0)
            sim0b, _, _ = rodar(nome, modelo0, simulacao.seed_independente(seed, 1))
            sim1, seg1, _ = rodar(nome, modelo1)
            no_ajuste = nome in ajuste["circuitos"] and job["repeticao"] == ajuste["repeticao"]
            linhas.append({
                "circuito": nome, "tipo": d["tipo"], "n": d["n"], "repeticao": job["repeticao"],
                "job_id": job["job_id"], "calibracao_id": job["calibracao"]["id"],
                "conjunto": "ajuste" if no_ajuste else "validacao",
                "nivel0": comparar(d, real, sim0),
                "nivel1": comparar(d, real, sim1),
                "hellinger_sim_x_sim": float(hellinger_distance(sim0, sim0b)),
                "simulador": config, "tempo_s": {"nivel0": seg0, "nivel1": seg1},
                "counts_sim_nivel0": sim0, "counts_sim_nivel1": sim1,
            })
            salvar()
        print(f"  repeticao {job['repeticao']} concluida")

    # ------------------------------------------------------------ 3. hardware x hardware
    variab = {}
    for d in descricoes:
        cont = [j["contagens"][d["nome"]] for j in saidas["jobs"]]
        pares = [float(hellinger_distance(a, b)) for a, b in combinations(cont, 2)]
        variab[d["nome"]] = float(np.mean(pares)) if pares else None
    manifesto["hellinger_hardware_x_hardware"] = variab
    manifesto["fim"] = datetime.now().astimezone()
    salvar()

    # ------------------------------------------------------------ resumo
    print(f"\n{'circuito':<20}{'H Nivel0':>10}{'H Nivel1':>10}{'sim x sim':>11}{'hw x hw':>9}  extra")
    for d in descricoes:
        ls = [l for l in linhas if l["circuito"] == d["nome"]]
        m = lambda f: np.mean([f(l) for l in ls])
        h0, h1 = m(lambda l: l["nivel0"]["hellinger"]), m(lambda l: l["nivel1"]["hellinger"])
        ss = m(lambda l: l["hellinger_sim_x_sim"])
        hw = f"{variab[d['nome']]:.3f}" if variab[d["nome"]] is not None else "-"
        if d["tipo"] == "leitura":
            extra = (f"erro real {m(lambda l: l['nivel0']['erro_medio_real']):.4f} | "
                     f"N0 {m(lambda l: l['nivel0']['erro_medio_simulado']):.4f} | "
                     f"N1 {m(lambda l: l['nivel1']['erro_medio_simulado']):.4f}")
        elif d["tipo"] == "paridade":
            extra = (f"paridade ideal {d['paridade_ideal']:+.2f} | real {m(lambda l: l['nivel0']['paridade_real']):+.3f} | "
                     f"N0 {m(lambda l: l['nivel0']['paridade_simulada']):+.3f} | "
                     f"N1 {m(lambda l: l['nivel1']['paridade_simulada']):+.3f}")
        else:
            extra = (f"massa GHZ real {m(lambda l: l['nivel0']['real']['massa_ghz']):.1%} | "
                     f"N0 {m(lambda l: l['nivel0']['simulado']['massa_ghz']):.1%} | "
                     f"N1 {m(lambda l: l['nivel1']['simulado']['massa_ghz']):.1%}")
        marca = " *" if d["nome"] in ajuste["circuitos"] else ""
        print(f"{d['nome'] + marca:<20}{h0:>10.3f}{h1:>10.3f}{ss:>11.3f}{hw:>9}  {extra}")
    print("\n* circuito de ajuste (nas outras repeticoes, ele tambem serve de validacao)")
    print(f"Medias sobre {len(saidas['jobs'])} repeticao(oes). Salvo em {pasta}")


if __name__ == "__main__":
    main()
