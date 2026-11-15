"""
Passo 06: baixa as saidas dos jobs de um lote e grava dados/<lote>/saidas.json.

O saidas.json tem so o que veio do hardware: para cada job, as contagens de cada
circuito (pelo nome) e a calibracao daquele job. Jobs ja baixados sao pulados;
jobs ainda na fila sao avisados. Pode rodar quantas vezes quiser.

Uso:
  python experimentos/06_baixar_saidas_lote.py --lote lote01
"""

import os
import sys
import argparse

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from nucleo import lotes


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--lote", required=True)
    args = parser.parse_args()

    envio, _ = lotes.carregar_envio(args.lote)
    saidas = lotes.carregar_saidas(args.lote)
    feitos = {j["job_id"] for j in saidas["jobs"]}
    pendentes = [j for j in envio["jobs"] if j["job_id"] not in feitos]
    if not pendentes:
        print(f"Todas as {len(feitos)} saidas ja estao em {lotes.caminho_saidas(args.lote)}")
        return

    from qiskit_ibm_runtime import QiskitRuntimeService
    service = QiskitRuntimeService()
    for item in pendentes:
        print(f"repeticao {item['repeticao']} ({item['job_id']}) ...", end=" ", flush=True)
        try:
            status = lotes.baixar_job(service, args.lote, saidas, item, envio["circuitos"])
            print("baixado" if status == "DONE" else f"ainda nao terminou ({status})")
        except Exception as e:
            print(f"ERRO: {e}")

    total = len(lotes.carregar_saidas(args.lote)["jobs"])
    print(f"\n{total} de {len(envio['jobs'])} job(s) em {lotes.caminho_saidas(args.lote)}")


if __name__ == "__main__":
    main()
