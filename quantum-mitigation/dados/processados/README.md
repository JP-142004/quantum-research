# Dados processados

Resultados calculados localmente a partir dos [dados brutos](../brutos/README.md), sem acessar a IBM. Os arquivos são refeitos pelos [scripts](../../scripts/README.md).

[Dados](../README.md)

| Arquivo | Experimento | O que tem |
| --- | --- | --- |
| `resumo_escala.csv` | 1 | Uma linha por tamanho de circuito: medidas, todos zeros, todos uns, outros e PZ. |
| `02_controles/resultados_recuperados.json` | 2 | Uma linha por circuito: job, backend, contagens resumidas, indicadores e custo compilado. |
| `03_ghz_conectado/resultados_recuperados.json` | 3 | Idem, para as construções do GHZ. |
| `comparacao_rodadas.json` | 4 | As três rodadas: valores brutos e ajustados, erros padrão, ganhos, intervalos de 95% e hashes dos arquivos de origem. |
| `resumo_mitigacao.csv` | 4 | Resumo histórico das duas primeiras rodadas, sem erros padrão. |

Relatório completo das rodadas, gerado a partir de `comparacao_rodadas.json`: [docs/comparacao_rodadas.md](../../docs/comparacao_rodadas.md).
