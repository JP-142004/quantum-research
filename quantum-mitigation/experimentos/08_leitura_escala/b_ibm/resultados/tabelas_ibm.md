# Tabelas geradas dos dados (não editar à mão)

## independencia

| Sessão | n | Estado | Taxa de erro | T | p-valor | Pares com mais erros juntos (observado/esperado) |
| --- | ---: | --- | ---: | ---: | ---: | --- |
| 2026-11-23_ibm_fez | 10 | zeros | 0,008 | -0,000 | 0,672 | 6–8: 2/0,6, 0–1: 0/0,0 |
| 2026-11-23_ibm_fez | 10 | uns | 0,021 | -0,006 | 0,795 | 4–6: 2/0,8, 3–4: 3/1,8 |
| 2026-11-23_ibm_fez | 20 | zeros | 0,007 | 0,008 | 0,065 | 9–12: 2/0,0, 12–16: 2/0,2 |
| 2026-11-23_ibm_fez | 20 | uns | 0,018 | -0,031 | 0,981 | 3–13: 6/3,3, 12–14: 2/0,6 |

## contexto

| Sessão | n | Maior diferença | Equivalentes | Inconclusivas | Diferentes | Resultado |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| 2026-11-23_ibm_fez | 10 | 0,013 | 17 | 3 | 0 | inconclusivo |
| 2026-11-23_ibm_fez | 20 | 0,011 | 35 | 5 | 0 | inconclusivo |

## ghz

| Sessão | n | Indicador | Observado | Ajustado (2 estados) | Ganho [IC 95%] | Ajustado (4 estados) |
| --- | ---: | --- | ---: | ---: | ---: | ---: |
| 2026-11-23_ibm_fez | 10 | PZ | 0,7820 ± 0,0129 | 0,8986 ± 0,0170 | 0,117 [0,101; 0,134] | 0,8970 ± 0,0160 |
| 2026-11-23_ibm_fez | 10 | CX | 0,6640 ± 0,0235 | 0,8920 ± 0,0351 | 0,228 [0,195; 0,265] | 0,8862 ± 0,0331 |
| 2026-11-23_ibm_fez | 20 | PZ | 0,6160 ± 0,0153 | 0,7894 ± 0,0222 | 0,173 [0,153; 0,195] | 0,7805 ± 0,0208 |
| 2026-11-23_ibm_fez | 20 | CX | 0,5160 ± 0,0269 | 0,8670 ± 0,0491 | 0,351 [0,301; 0,406] | 0,8469 ± 0,0458 |

## controles

| Sessão | n | Controle | Observado | Ajustado (2 estados) | (ajustado − 1) / erro padrão |
| --- | ---: | --- | ---: | ---: | ---: |
| 2026-11-23_ibm_fez | 10 | `0000000000` em Z | 0,9270 ± 0,0081 | 1,0021 ± 0,0129 | 0,2 |
| 2026-11-23_ibm_fez | 10 | `1111111111` em Z | 0,8300 ± 0,0119 | 1,0272 ± 0,0211 | 1,3 |
| 2026-11-23_ibm_fez | 10 | `++++++++++` em X | 0,9200 ± 0,0086 | 0,9942 ± 0,0131 | -0,4 |
| 2026-11-23_ibm_fez | 10 | `+++++++++-` em X | 0,9070 ± 0,0092 | 1,0066 ± 0,0152 | 0,4 |
| 2026-11-23_ibm_fez | 20 | `00000000000000000000` em Z | 0,8710 ± 0,0108 | 1,0044 ± 0,0183 | 0,2 |
| 2026-11-23_ibm_fez | 20 | `11111111111111111111` em Z | 0,7020 ± 0,0143 | 1,0234 ± 0,0287 | 0,8 |
| 2026-11-23_ibm_fez | 20 | `++++++++++++++++++++` em X | 0,8350 ± 0,0116 | 0,9620 ± 0,0185 | -2,1 |
| 2026-11-23_ibm_fez | 20 | `+++++++++++++++++++-` em X | 0,8280 ± 0,0118 | 0,9797 ± 0,0198 | -1,0 |

## criterios

| n | Erros conjuntos | Dependência dos vizinhos | GHZ melhorou (PZ e CX) | Controles a 2 erros padrão |
| --- | --- | --- | --- | --- |
| 10 | não rejeitada | inconclusivo | sim | sim (só 1 de 3 sessões) |
| 20 | não rejeitada | inconclusivo | sim | não (só 1 de 3 sessões) |
