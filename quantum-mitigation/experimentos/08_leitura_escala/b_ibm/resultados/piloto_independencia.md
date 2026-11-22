# Teste prévio da verificação de independência (gerado dos dados; não editar à mão)

| Origem | Sessão · estado | Taxa de erro por qubit | T | T com qubits embaralhados | p-valor | Par com mais erros juntos |
| --- | --- | ---: | ---: | --- | ---: | --- |
| A · simulador, 10 qubits | leitura_bloco_01 · zeros | 0,029 | 0,015 | 0,000 ± 0,012 | 0,130 | 5–7: 4 (esperado 1,3) |
| A · simulador, 10 qubits | leitura_bloco_01 · uns | 0,040 | -0,009 | 0,000 ± 0,016 | 0,741 | 3–7: 5 (esperado 1,9) |
| A · simulador, 10 qubits | leitura_bloco_02 · zeros | 0,030 | 0,034 | 0,000 ± 0,012 | 0,011 | 2–6: 5 (esperado 1,1) |
| A · simulador, 10 qubits | leitura_bloco_02 · uns | 0,038 | -0,004 | -0,000 ± 0,015 | 0,605 | 3–9: 5 (esperado 2,5) |
| A · simulador, 10 qubits | leitura_bloco_03 · zeros | 0,030 | 0,015 | 0,000 ± 0,012 | 0,134 | 0–6: 5 (esperado 2,3) |
| A · simulador, 10 qubits | leitura_bloco_03 · uns | 0,039 | -0,004 | -0,001 ± 0,016 | 0,608 | 4–9: 8 (esperado 3,4) |
| A · simulador, 10 qubits | leitura_correlacionada_bloco_01 · zeros | 0,058 | 0,294 | 0,001 ± 0,023 | 0,001 | 8–9: 34 (esperado 2,3) |
| A · simulador, 10 qubits | leitura_correlacionada_bloco_01 · uns | 0,064 | 0,209 | 0,001 ± 0,024 | 0,001 | 8–9: 38 (esperado 7,4) |
| A · simulador, 10 qubits | leitura_correlacionada_bloco_02 · zeros | 0,059 | 0,294 | 0,001 ± 0,023 | 0,001 | 8–9: 37 (esperado 2,5) |
| A · simulador, 10 qubits | leitura_correlacionada_bloco_02 · uns | 0,067 | 0,271 | 0,002 ± 0,026 | 0,001 | 6–7: 37 (esperado 5,1) |
| A · simulador, 10 qubits | leitura_correlacionada_bloco_03 · zeros | 0,058 | 0,286 | 0,001 ± 0,024 | 0,001 | 2–3: 37 (esperado 3,8) |
| A · simulador, 10 qubits | leitura_correlacionada_bloco_03 · uns | 0,066 | 0,296 | 0,000 ± 0,026 | 0,001 | 8–9: 35 (esperado 6,9) |
| Experimento 4 · IBM, 5 qubits | 2026-11-08_ibm_fez · zeros | 0,015 | -0,001 | -0,000 ± 0,002 | 0,806 | 1–3: 1 (esperado 0,7) |
| Experimento 4 · IBM, 5 qubits | 2026-11-08_ibm_fez · uns | 0,022 | 0,003 | -0,000 ± 0,004 | 0,289 | 1–3: 3 (esperado 1,0) |
| Experimento 4 · IBM, 5 qubits | 2026-11-09_ibm_fez · zeros | 0,009 | -0,001 | -0,000 ± 0,002 | 0,979 | 0–2: 0 (esperado 0,0) |
| Experimento 4 · IBM, 5 qubits | 2026-11-09_ibm_fez · uns | 0,022 | -0,007 | 0,000 ± 0,004 | 0,947 | 1–3: 1 (esperado 0,7) |
| Experimento 4 · IBM, 5 qubits | 2026-11-10_ibm_fez · zeros | 0,015 | 0,001 | 0,000 ± 0,003 | 0,501 | 0–1: 1 (esperado 0,1) |
| Experimento 4 · IBM, 5 qubits | 2026-11-10_ibm_fez · uns | 0,024 | 0,001 | -0,000 ± 0,004 | 0,352 | 0–2: 1 (esperado 0,1) |
