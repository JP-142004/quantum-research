# Dados brutos (IBM)

Contagens medidas em computadores quânticos da IBM, como foram devolvidas. Cada arquivo `.json` guarda as contagens de um job (uma execução na IBM); o `.qpy` de mesmo nome guarda os circuitos compilados desse job, na ordem dos índices do JSON. O nome do arquivo é o identificador do job.

[Dados](../README.md)

## 01 · Escala do GHZ

| Arquivo | O que é |
| --- | --- |
| `01_ghz_escala/ghz_05_a_50.txt` | Contagens por sequência de bits, em dez seções (5, 10, … 50 qubits), 1.000 medidas cada. Backend e data não foram registrados. |

Figura: [01_escala_observada](../../figuras/01_escala_observada.png). Tabela calculada: [resumo_escala.csv](../processados/resumo_escala.csv).

## 02 · Controles de estados conhecidos

Recuperados da IBM em 2 de novembro de 2026.

| Job | Circuitos | Backend |
| --- | --- | --- |
| `02_controles/dbbrrnpgv2cc73e922r0` | todos zeros | ibm_kingston |
| `02_controles/dbbsd47i0auc73948300` | todos uns | ibm_kingston |
| `02_controles/dbcbsopgv2cc73ea1300` | qubits individuais | ibm_kingston |
| `02_controles/dbcc4g9gv2cc73ea1j10` | qubits individuais | ibm_fez |
| `02_controles/dbcc5ggc77vs7385vfsg` | zeros medidos separados e juntos | ibm_fez |

Figura: [02_controles_reais](../../figuras/02_controles_reais.png).

## 03 · Construções do GHZ

Recuperados da IBM em 2 de novembro de 2026. Todos no ibm_fez.

| Job | Circuitos |
| --- | --- |
| `03_ghz_conectado/dbccaqpgv2cc73ea21fg` | GHZ original de 5 qubits |
| `03_ghz_conectado/dbcccpc24mrc73cjb6bg` | original e conectado, medidos em Z |
| `03_ghz_conectado/dbcco2fi0auc73dum8i0` | original e conectado, medidos em X |
| `03_ghz_conectado/dbch2kpgv2cc73eabim0` | GHZ conectado de 50 qubits |

Figura: [03_construcoes_reais](../../figuras/03_construcoes_reais.png).

## 04 · Calibração de leitura

Cada rodada tem 34 circuitos (32 de calibração, mais o GHZ em Z e em X), 1.000 medidas por circuito, no ibm_fez. A tabela mostra as contagens do GHZ.

| Rodada | Arquivo | Z: 00000 | Z: 11111 | Z: outros | X: par | X: ímpar |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| 1 | `04_mitigacao_leitura/GHZ_leitura_dbccq67i0auc73dumdk0.json` | 439 | 434 | 127 | 898 | 102 |
| 2 | `04_mitigacao_leitura/GHZ_leitura_dbccri9gv2cc73ea3630.json` | 445 | 419 | 136 | 898 | 102 |
| 3 | `04_mitigacao_leitura/rodada_03/rodada_03.json` (+ `.qpy`) | 454 | 441 | 105 | 903 | 97 |

Em X, "par" e "ímpar" contam as sequências com número par ou ímpar de bits 1. A rodada 3 (job `dbjnndgnceqs73akbkh0`) é a única com os circuitos salvos em QPY; sua pasta se chamava `repeticoes` e foi renomeada.

Figuras: [04_comparacao_rodadas](../../figuras/04_comparacao_rodadas.png) e [04_contagens_rodada3](../../figuras/04_contagens_rodada3.png).
