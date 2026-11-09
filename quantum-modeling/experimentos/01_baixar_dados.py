"""
Passo 01: baixa da IBM, uma unica vez, tudo o que os outros scripts precisam.

Para cada job de dados/jobs_ghz.json salva o circuito ISA, as contagens reais,
a procedencia (datas, opcoes, layout) e o snapshot de calibracao do dia do job.
Depois disso os passos seguintes rodam sem internet.

Uso:
  python experimentos/01_baixar_dados.py               # baixa so o que falta
  python experimentos/01_baixar_dados.py --sobrescrever
"""

import os
import sys
import argparse

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from qiskit_ibm_runtime import QiskitRuntimeService
from nucleo import dados_jobs


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sobrescrever", action="store_true", help="baixa de novo mesmo o que ja existe")
    args = parser.parse_args()

    service = QiskitRuntimeService()
    falhas = 0
    for item in dados_jobs.carregar_lista_jobs():
        n, job_id = item["tamanho_ghz"], item["job_id"]
        if dados_jobs.job_ja_baixado(n, job_id) and not args.sobrescrever:
            print(f"GHZ-{n:>2} ({job_id}): ja baixado, pulando")
            continue
        print(f"GHZ-{n:>2} ({job_id}): baixando...")
        try:
            info = dados_jobs.baixar_job(service, job_id, n)
        except Exception as e:
            falhas += 1
            print(f"    ERRO: {e}")
            continue
        c = info["calibracao"]
        print(f"    calibracao {c['id']} | origem: {c['origem']} | defasagem: {c['defasagem_horas']} h")
        for aviso in info["avisos"]:
            print(f"    AVISO: {aviso}")

    print("\nConcluido." if not falhas else f"\nConcluido com {falhas} falha(s).")


if __name__ == "__main__":
    main()
