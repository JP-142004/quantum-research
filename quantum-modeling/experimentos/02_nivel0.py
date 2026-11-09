"""
Passo 02: linha de base (Nivel 0).

Para cada job, simula o MESMO circuito ISA com o modelo de ruido padrao,
montado a partir da calibracao do dia do job (dados/calibracao/), e compara
com o hardware: Hellinger, massa GHZ, P(0...0), P(1...1) e peso de Hamming.

Roda sem internet (precisa do passo 01 antes). Cada execucao cria uma pasta
nova em resultados/ com resultados.json e manifesto.json, salvos apos cada
job. Se cair no meio, use --continuar para pular os jobs ja processados.

Uso:
  python experimentos/02_nivel0.py
  python experimentos/02_nivel0.py --tamanhos 5 10 15
  python experimentos/02_nivel0.py --continuar resultados/2026-11-09_1530_nivel0
"""

import os
import sys
import argparse
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from nucleo import dados_jobs, metricas, modelos_ruido, registro, simulacao
from nucleo.dados_jobs import ler_json, salvar_json

SEED_PADRAO = 1234


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=SEED_PADRAO, help="seed do simulador")
    parser.add_argument("--tamanhos", type=int, nargs="*", help="so estes tamanhos de GHZ")
    parser.add_argument("--continuar", help="pasta de uma execucao anterior para retomar")
    args = parser.parse_args()

    if args.continuar:
        pasta = os.path.abspath(args.continuar)
        resultados = ler_json(os.path.join(pasta, "resultados.json"))
        manifesto = ler_json(os.path.join(pasta, "manifesto.json"))
        seed = manifesto["seed_simulador"]
        print(f"Retomando {pasta} (seed {seed})")
    else:
        pasta = registro.nova_pasta_execucao("nivel0")
        resultados = []
        seed = args.seed
        manifesto = {
            "experimento": "nivel0",
            "inicio": datetime.now().astimezone(),
            "commit_git": registro.commit_git(),
            "versoes": registro.versoes(),
            "seed_simulador": seed,
            "modelo_ruido": "NoiseModel.from_backend com Target reconstruido do snapshot de calibracao do job",
            "jobs": [],
        }
        print(f"Nova execucao em {pasta}")

    feitos = {r["job_id"] for r in resultados if "erro" not in r}
    resultados = [r for r in resultados if "erro" not in r]  # erros antigos sao tentados de novo
    manifesto["jobs"] = [j for j in manifesto["jobs"] if j["job_id"] in feitos]

    def salvar():
        salvar_json(os.path.join(pasta, "resultados.json"), resultados)
        salvar_json(os.path.join(pasta, "manifesto.json"), manifesto)

    cache_modelos = {}
    for item in dados_jobs.carregar_lista_jobs():
        n, job_id = item["tamanho_ghz"], item["job_id"]
        if args.tamanhos and n not in args.tamanhos:
            continue
        if job_id in feitos:
            print(f"GHZ-{n:>2}: ja processado, pulando")
            continue
        print(f"GHZ-{n:>2} ({job_id}) ...", flush=True)
        try:
            dados = dados_jobs.carregar_job_local(n, job_id)
            info = dados["info"]
            cid = info["calibracao"]["id"]
            if cid not in cache_modelos:  # o cache e por calibracao (feedback, item 1)
                cache_modelos[cid] = modelos_ruido.nivel0(dados["propriedades"], dados["configuracao"])
            shots = sum(dados["counts_real"].values())
            metodo = simulacao.escolher_metodo(n)
            counts_sim, segundos, config = simulacao.simular(
                dados["circuito"], cache_modelos[cid], shots, seed, metodo)
            comp = metricas.comparar(dados["counts_real"], counts_sim, n)
            print(f"    {metodo} | {segundos:.1f} s | Hellinger = {comp['hellinger']:.4f} | "
                  f"massa GHZ real {comp['real']['massa_ghz']:.1%} x sim {comp['simulado']['massa_ghz']:.1%}")

            resultados.append({
                "job_id": job_id,
                "tamanho_ghz": n,
                "backend": info["backend"],
                "calibracao_id": cid,
                "shots": shots,
                "counts_real": dados["counts_real"],
                "counts_sim_nivel0": counts_sim,
                "hellinger_nivel0": comp["hellinger"],
                "metricas": comp,
                "tempo_simulacao_s": segundos,
            })
            manifesto["jobs"].append({
                "job_id": job_id,
                "tamanho_ghz": n,
                "calibracao": info["calibracao"],
                "simulador": config,
                "circuito": {k: info["circuito"][k] for k in
                             ("profundidade", "profundidade_2q", "portas_2q", "layout_inicial")},
                "opcoes_do_job": info["opcoes_do_job"],
                "avisos": info["avisos"],
            })
        except Exception as e:
            print(f"    ERRO: {e}")
            resultados.append({"job_id": job_id, "tamanho_ghz": n, "erro": str(e)})
        salvar()

    manifesto["fim"] = datetime.now().astimezone()
    salvar()

    print("\nResumo:")
    for r in sorted(resultados, key=lambda r: r["tamanho_ghz"]):
        if "erro" in r:
            print(f"  GHZ-{r['tamanho_ghz']:>2} | ERRO: {r['erro']}")
        else:
            m = r["metricas"]
            print(f"  GHZ-{r['tamanho_ghz']:>2} | Hellinger {r['hellinger_nivel0']:.4f} | "
                  f"P(0..0) {m['real']['p_todos_zeros']:.3f} x {m['simulado']['p_todos_zeros']:.3f} | "
                  f"P(1..1) {m['real']['p_todos_uns']:.3f} x {m['simulado']['p_todos_uns']:.3f}")
    print(f"\nSalvo em {pasta}")


if __name__ == "__main__":
    main()
