# Resultados históricos da modelagem

[Visão da modelagem](../README.md) · [JSON salvo](resultados_ghz_nivel0.json)

O JSON contém uma lista de dez registros, um por tamanho GHZ. Não foi alterado pela documentação da mitigação.

| Campo | Significado |
| --- | --- |
| `job_id` | Identificador do job real recuperado |
| `tamanho_ghz` | Número de qubits do caso |
| `backend` | Backend registrado, Kingston nesses resultados |
| `data_hardware` | Data do job convertida para texto pelo script |
| `metodo_simulacao` | Método do Aer selecionado |
| `shots` | Número de medidas usado na comparação |
| `counts_real` | Contagens recuperadas do hardware |
| `counts_sim_nivel0` | Contagens da simulação local ruidosa |
| `hellinger_nivel0` | Distância entre as duas distribuições amostradas |
| `erro` | Campo possível quando o processamento de um job falha |

Os registros reais e simulados compartilham um arquivo, mas continuam identificados por campos distintos. Não confunda essas contagens simuladas históricas com os 486.000 shots da validação nova de mitigação. O programa gerador sobrescreve este JSON quando executado; preserve o registro antes de qualquer nova análise de modelagem.
