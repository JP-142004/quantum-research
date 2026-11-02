# Comparação de construções GHZ · resultados

Cada circuito contém 1.000 medidas.

| Teste | Circuito | Indicador bruto | Portas de dois qubits | Profundidade |
| --- | --- | ---: | ---: | ---: |
| original_fez | original_Z | 0.834 | 13 | 35 |
| comparar_construcoes | original_Z | 0.833 | 13 | 35 |
| comparar_construcoes | conectado_Z | 0.888 | 4 | 13 |
| comparar_base_x | original_X | 0.566 | 13 | 38 |
| comparar_base_x | conectado_X | 0.774 | 4 | 16 |
| conectado_50 | conectado50_Z | 0.155 | 49 | 56 |

Nas linhas Z, o indicador é PZ = (zeros + uns)/1.000. Nas linhas X, é CX = (pares − ímpares)/1.000. Em Z, a comparação no mesmo job dá 0,833 para original e 0,888 para conectado. Em X, outro job dá 0,566 e 0,774. O conectado de 50 qubits dá PZ = (132 + 23)/1.000 = 0,155. Não é uma comparação controlada com a série Kingston de 50 qubits, executada em outro backend e data. Estes valores são brutos, sem mitigação de leitura.

[Valores completos e IDs](resultados_recuperados.json) · [Contagens e circuitos](../../brutos/03_ghz_conectado/README.md)
