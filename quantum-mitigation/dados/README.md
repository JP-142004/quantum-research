# Dados

Aqui estão os dados da pesquisa, sem análise. A interpretação de cada experimento está no relatório dele, em [experimentos](../experimentos/README.md).

Os dados são de três tipos, e cada tipo tem uma pasta:

| Pasta | O que tem | Como foi obtido |
| --- | --- | --- |
| [brutos](brutos/README.md) | Contagens e circuitos compilados. | Circuitos executados em computadores quânticos da IBM. Cada execução devolve quantas vezes cada sequência de bits apareceu. |
| [processados](processados/README.md) | Indicadores calculados (PZ, CX), ajustes de leitura e incertezas. | Scripts locais leem os dados brutos e fazem as contas. |
| [simulados](simulados/README.md) | Contagens e análises de simulações. | Simulador no PC, com ruído sintético escolhido por nós. |

## Onde estão os dados de cada experimento

| Experimento | Brutos (IBM) | Processados | Simulados |
| --- | --- | --- | --- |
| [1. Escala do GHZ](../experimentos/01_ghz_escala/README.md) | `brutos/01_ghz_escala` | `processados/01_ghz_escala` | — |
| [2. Controles](../experimentos/02_controles/README.md) | `brutos/02_controles` | `processados/02_controles` | — |
| [3. Construção com menos portas](../experimentos/03_ghz_conectado/README.md) | `brutos/03_ghz_conectado` | `processados/03_ghz_conectado` | — |
| [4. Calibração de leitura](../experimentos/04_mitigacao_leitura/README.md) | `brutos/04_mitigacao_leitura` | `processados/04_mitigacao_leitura` | — |
| [5. Validação simulada](../experimentos/05_validacao_simulada/README.md) | — | — | `simulados/validacao_2026_11_01` |
| [6. ZNE simulada](../experimentos/06_zne_simulado/README.md) | — | — | `simulados/validacao_2026_11_01` |

As figuras feitas a partir destes dados estão em [figuras](../figuras/README.md).

**Regra:** `brutos` e `simulados` são o registro original e não se editam. Os processados e as figuras podem ser refeitos pelos [scripts](../scripts/README.md).

**Novo experimento:** crie a pasta com o mesmo número do experimento (por exemplo `brutos/07_nome_curto`) e acrescente uma linha na tabela acima.
