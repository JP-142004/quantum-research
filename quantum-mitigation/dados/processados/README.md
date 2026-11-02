# Dados processados

Resultados calculados localmente a partir dos [dados brutos](../brutos/README.md), sem acessar a IBM. Cada experimento tem sua pasta, com o mesmo número. Os arquivos são refeitos pelos [scripts](../../scripts/README.md).

[Dados](../README.md)

| Pasta | Arquivo | O que tem | Feito por |
| --- | --- | --- | --- |
| `01_ghz_escala` | `resumo_escala.csv` | Uma linha por tamanho de circuito (5 a 50 qubits): medidas, todos zeros, todos uns, outros e PZ. | `resumir_resultados.py` |
| `02_controles` | `resultados_recuperados.json` | Uma linha por circuito: job, backend, contagens resumidas, indicadores e custo compilado. | Recuperação da IBM |
| `03_ghz_conectado` | `resultados_recuperados.json` | Idem, para as construções do GHZ. | Recuperação da IBM |
| `04_mitigacao_leitura` | `resumo_mitigacao.csv` | Uma linha por rodada (1 a 3): PZ e CX brutos e ajustados, condicionamento da matriz de calibração e menor quasiprobabilidade. Sem erros padrão. | `resumir_resultados.py` |
| `04_mitigacao_leitura` | `comparacao_rodadas.json` | As três rodadas com erros padrão, ganhos, intervalos de 95% e hashes dos arquivos de origem. | `comparar_rodadas.py` |

Relatório completo das rodadas, gerado a partir de `comparacao_rodadas.json`: [docs/comparacao_rodadas.md](../../docs/comparacao_rodadas.md).
