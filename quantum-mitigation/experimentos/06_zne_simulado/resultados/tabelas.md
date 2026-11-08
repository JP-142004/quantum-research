# Tabelas geradas dos dados (não editar à mão)

## sessoes

| Item | Indicador | bloco_01 | bloco_02 | bloco_03 |
| --- | --- | ---: | ---: | ---: |
| GHZ conectado, 5 qubits, base Z | PZ | 0,7940 → 0,9460 | 0,8030 → 0,9534 | 0,7880 → 0,9374 |
| GHZ conectado, 5 qubits, base Z, fator 3 | PZ | 0,7090 → 0,8436 | 0,7300 → 0,8639 | 0,7120 → 0,8454 |
| GHZ conectado, 5 qubits, base Z, fator 5 | PZ | 0,6250 → 0,7412 | 0,6210 → 0,7331 | 0,6190 → 0,7316 |
| GHZ conectado, 5 qubits, base X | CX | 0,6840 → 0,9743 | 0,6100 → 0,8820 | 0,6520 → 0,9429 |
| GHZ conectado, 5 qubits, base X, fator 3 | CX | 0,5660 → 0,8144 | 0,5160 → 0,7395 | 0,6040 → 0,8758 |
| GHZ conectado, 5 qubits, base X, fator 5 | CX | 0,4840 → 0,6931 | 0,4740 → 0,6851 | 0,4840 → 0,6979 |
| estado `00000`, 5 qubits (controle) | sucesso | 0,8700 → 1,0058 | 0,8560 → 0,9973 | 0,8470 → 0,9636 |
| estado `11111`, 5 qubits (controle) | sucesso | 0,7980 → 0,9814 | 0,8040 → 0,9730 | 0,8240 → 1,0261 |
| estado `+++++`, 5 qubits, base X (controle) | sucesso | 0,8760 → 1,0131 | 0,8630 → 1,0058 | 0,8530 → 0,9708 |
| estado `++++-`, 5 qubits, base X (controle) | sucesso | 0,7980 → 0,9655 | 0,8100 → 0,9700 | 0,8240 → 1,0274 |

## controles

| Sessão | 00000 em Z | 11111 em Z | +++++ em X | ++++- em X |
| --- | ---: | ---: | ---: | ---: |
| bloco_01 | 0,006 | -0,019 | 0,013 | -0,035 |
| bloco_02 | -0,003 | -0,027 | 0,006 | -0,030 |
| bloco_03 | -0,036 | 0,026 | -0,029 | 0,027 |

## validacao

| Sessão | Cenário | Maior desvio do bruto (EP) | Maior desvio do ajustado (EP) | Dentro do limite |
| --- | --- | ---: | ---: | --- |
| bloco_01 | leitura_e_portas | 1,83 | 1,63 | sim |
| bloco_02 | leitura_e_portas | 1,39 | 1,52 | sim |
| bloco_03 | leitura_e_portas | 2,30 | 2,44 | sim |

## zne_exato

| Fator de ruído | Portas de 2 qubits | PZ (referência exata) | CX (referência exata) |
| --- | ---: | ---: | ---: |
| 1 | 4 | 0,9463 | 0,9224 |
| 3 | 12 | 0,8490 | 0,7847 |
| 5 | 20 | 0,7637 | 0,6676 |
| 0 (extrapolado) | — | **0,9899** | **0,9826** |

## zne_blocos

| Sessão | Indicador | Ajustado, fator 1 | Após ZNE | Exato, fator 1 | Exato após ZNE |
| --- | --- | ---: | ---: | ---: | ---: |
| bloco_01 | CX | 0,9743 ± 0,0340 | 1,0381 ± 0,0421 | 0,9224 | 0,9826 |
| bloco_01 | PZ | 0,9460 ± 0,0184 | 0,9972 ± 0,0220 | 0,9463 | 0,9899 |
| bloco_02 | CX | 0,8820 ± 0,0364 | 0,9165 ± 0,0441 | 0,9224 | 0,9826 |
| bloco_02 | PZ | 0,9534 ± 0,0182 | 1,0154 ± 0,0218 | 0,9463 | 0,9899 |
| bloco_03 | CX | 0,9429 ± 0,0360 | 1,0227 ± 0,0442 | 0,9224 | 0,9826 |
| bloco_03 | PZ | 0,9374 ± 0,0185 | 0,9925 ± 0,0223 | 0,9463 | 0,9899 |
