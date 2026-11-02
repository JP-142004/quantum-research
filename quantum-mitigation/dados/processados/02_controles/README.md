# Controles com estados conhecidos · resultados

Cada circuito contém 1.000 medidas.

| Teste | Backend | Circuito | Estado preparado | Acertos / 1.000 | Desvio |
| --- | --- | --- | --- | ---: | ---: |
| todos_zeros | ibm_kingston | zeros | 00000 | 528 | 47.2% |
| todos_uns | ibm_kingston | uns | 11111 | 768 | 23.2% |
| individuais_kingston | ibm_kingston | q0_zero | 0 | 249 | 75.1% |
| individuais_kingston | ibm_kingston | q0_um | 1 | 915 | 8.5% |
| individuais_kingston | ibm_kingston | q1_zero | 0 | 1000 | 0.0% |
| individuais_kingston | ibm_kingston | q1_um | 1 | 957 | 4.3% |
| individuais_fez | ibm_fez | q0_zero | 0 | 992 | 0.8% |
| individuais_fez | ibm_fez | q0_um | 1 | 973 | 2.7% |
| individuais_fez | ibm_fez | q1_zero | 0 | 989 | 1.1% |
| individuais_fez | ibm_fez | q1_um | 1 | 978 | 2.2% |
| zeros_separados_juntos | ibm_fez | q0_zero | 0 | 991 | 0.9% |
| zeros_separados_juntos | ibm_fez | q1_zero | 0 | 991 | 0.9% |
| zeros_separados_juntos | ibm_fez | zeros | 00000 | 942 | 5.8% |

Desvio é a fração de medidas diferente do estado preparado. Os controles de 1 incluem portas X. Os valores incluem preparação, inicialização e leitura. O qubit 0 no teste individual Kingston apresentou 751 resultados 1 ao preparar 0; esse desvio observado é real, mas sua causa isolada não pode ser inferida dessas contagens. Comparações entre backends ou datas são descritivas.

[Valores completos e IDs](resultados_recuperados.json) · [Contagens e circuitos](../../brutos/02_controles/README.md)
