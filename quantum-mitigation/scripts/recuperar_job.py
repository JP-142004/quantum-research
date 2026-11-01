from qiskit_ibm_runtime import QiskitRuntimeService

service = QiskitRuntimeService(channel="ibm_quantum_platform")
job = service.job('dbaa20fi0auc7391ncu0')
job_result = job.result()
print(f"Status do job: {job.status()}")

pub_result = job_result[0]
counts = pub_result.data.c.get_counts()

print(f"\n{'RESULTADO':<32} {'CONTAGEM':>10}")
print("-" * 44)

# Ordem crescente: de 000...0 até 111...1
for estado in sorted(counts):
    print(f"{estado:<32} {counts[estado]:>10}")

total = sum(counts.values())
print("-" * 44)
print(f"{'Total de medições:':<32} {total:>10}")
# To get counts for a particular pub result, use
#
# pub_result = job_result[<idx>].data.<classical register>.get_counts()
#
# where <idx> is the index of the pub and <classical register> is the name of the classical register.
# You can use circuit.cregs to find the name of the classical registers.