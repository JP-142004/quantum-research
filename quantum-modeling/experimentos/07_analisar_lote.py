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
    ghz = [d for d in descricoes if d["tipo"] == "ghz"]
    outros = [d for d in descricoes if d["tipo"] != "ghz"]

    def media(nome, f):
        return float(np.mean([f(l) for l in linhas if l["circuito"] == nome]))

    def rotulo(d):
        return f"GHZ-{d['n']}" + (" *" if d["nome"] in ajuste["circuitos"] else "")

    if ghz:
        print("\nBLOCO 1 - O simulador acerta quanto ruido existe?")
        print("(massa GHZ = % dos shots que saiu 00..0 ou 11..1; ideal = 100%)")
        print(f"{'circuito':<10}{'Real':>8}{'N0':>8}{'N1':>8}{'Erro N0':>10}{'Erro N1':>10}  Resultado")
        for d in ghz:
            n = d["nome"]
            real = media(n, lambda l: l["nivel0"]["real"]["massa_ghz"])
            m0 = media(n, lambda l: l["nivel0"]["simulado"]["massa_ghz"])
            m1 = media(n, lambda l: l["nivel1"]["simulado"]["massa_ghz"])
            e0 = media(n, lambda l: abs(l["nivel0"]["simulado"]["massa_ghz"] - l["nivel0"]["real"]["massa_ghz"])) * 100
            e1 = media(n, lambda l: abs(l["nivel1"]["simulado"]["massa_ghz"] - l["nivel1"]["real"]["massa_ghz"])) * 100
            res = "melhorou" if e1 < e0 else "piorou"
            print(f"{rotulo(d):<10}{real:>8.1%}{m0:>8.1%}{m1:>8.1%}{e0:>8.1f}pp{e1:>8.1f}pp  {res}")
        print("Real = hardware da IBM | N0 = simulacao com a calibracao | N1 = simulacao ajustada")
        print("Erro = diferenca para o Real em pontos percentuais (menor e melhor). Incerteza com 1000 shots: ~1,5 pp.")

        print("\nBLOCO 2 - A distribuicao inteira esta parecida? (distancia de Hellinger, menor e melhor)")
        print(f"{'circuito':<10}{'H N0':>8}{'H N1':>8}{'Piso':>8}{'Var. hw':>9}")
        for d in ghz:
            n = d["nome"]
            h0 = media(n, lambda l: l["nivel0"]["hellinger"])
            h1 = media(n, lambda l: l["nivel1"]["hellinger"])
            piso = media(n, lambda l: l["hellinger_sim_x_sim"])
            hw = f"{variab[n]:.3f}" if variab[n] is not None else "-"
            print(f"{rotulo(d):<10}{h0:>8.3f}{h1:>8.3f}{piso:>8.3f}{hw:>9}")
        print("Piso = menor valor possivel so pelo sorteio de 1000 shots. O que importa e a distancia ate ele.")
        print("Var. hw = diferenca entre dois jobs reais do mesmo circuito ('-' se houver so 1 repeticao).")

    print("\nBLOCO 3 - O que o ajuste mudou? (multiplicador sobre a calibracao da IBM; 1.00 = sem mudanca)")
    for g, v, (lo, hi) in zip(modelos_ruido.GENES, escalas, modelos_ruido.LIMITES):
        aviso = "   <- no limite permitido" if (v <= lo * 1.02 or v >= hi * 0.98) else ""
        print(f"  {g:<20} x {v:.2f}{aviso}")

    if outros:
        print("\nOUTROS CIRCUITOS (leitura / paridade)")
        for d in outros:
            n = d["nome"]
            h0 = media(n, lambda l: l["nivel0"]["hellinger"])
            h1 = media(n, lambda l: l["nivel1"]["hellinger"])
            print(f"  {n:<22} H N0 {h0:.3f} | H N1 {h1:.3f}")

    print("\n* circuito usado no ajuste (nas outras repeticoes ele tambem serve de validacao)")
    print(f"Medias sobre {len(saidas['jobs'])} repeticao(oes). Salvo em {pasta}")
    
if __name__ == "__main__":
    main()
