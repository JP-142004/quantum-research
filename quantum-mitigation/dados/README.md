# Dados da pesquisa

| Tipo | Como os dados são obtidos |
| --- | --- |
| [Brutos](brutos/README.md) | Circuitos executados no hardware da IBM produzem sequências de bits. As contagens registram quantas vezes cada sequência apareceu. |
| [Processados](processados/README.md) | Scripts locais leem as contagens reais e calculam indicadores, ajustes de leitura e incertezas. |
| [Simulados](simulados/README.md) | Um simulador no PC executa os circuitos com um modelo de ruído definido. As contagens e a análise ficam associadas à execução que as gerou. |

Dentro de cada tipo, escolha o experimento para consultar o método, os resultados e os arquivos de origem. Para incluir outra técnica ou circuito, acrescente uma pasta no tipo correspondente, registre a origem dos dados e liste o experimento no índice dessa categoria.

## Onde estão os dados de cada experimento

A interpretação, as contas e os limites de cada experimento estão em [experimentos](../experimentos/README.md). Esta tabela só indica onde ficam os arquivos.

| Experimento | Brutos (IBM) | Processados | Simulados |
| --- | --- | --- | --- |
| [1. Escala](../experimentos/01_ghz_escala/README.md) | [01_ghz_escala](brutos/01_ghz_escala/README.md) | [01_ghz_escala](processados/01_ghz_escala/README.md) | — |
| [2. Controles](../experimentos/02_controles/README.md) | [02_controles](brutos/02_controles/README.md) | [02_controles](processados/02_controles/README.md) | — |
| [3. Construção](../experimentos/03_ghz_conectado/README.md) | [03_ghz_conectado](brutos/03_ghz_conectado/README.md) | [03_ghz_conectado](processados/03_ghz_conectado/README.md) | — |
| [4. Calibração de leitura](../experimentos/04_mitigacao_leitura/README.md) | [04_mitigacao_leitura](brutos/04_mitigacao_leitura/README.md) | [04_mitigacao_leitura](processados/04_mitigacao_leitura/README.md) | — |
| [5. Validação simulada](../experimentos/05_validacao_simulada/README.md) | — | — | [validacao_2026_11_01](simulados/validacao_2026_11_01/README.md) |
| [6. ZNE simulada](../experimentos/06_zne_simulado/README.md) | — | — | [validacao_2026_11_01](simulados/validacao_2026_11_01/README.md) |

**Novo experimento:** crie a pasta de dados com o mesmo número, por exemplo `brutos/07_nome_curto`, e acrescente uma linha nesta tabela.

## Etapas dos dados brutos e recuperação das pastas 02 e 03

Os números identificam as etapas dos experimentos. Cada rodada é uma nova execução de uma etapa.

| Etapa | Dados disponíveis |
| --- | --- |
| [01 — Escala GHZ](brutos/01_ghz_escala/README.md) | Contagens dos circuitos de 5 a 50 qubits. |
| [02 — Controles](brutos/02_controles/README.md) | Contagens e circuitos históricos recuperados da IBM em 2 de novembro de 2026. |
| [03 — Construção conectada](brutos/03_ghz_conectado/README.md) | Comparações em Z e X e GHZ conectado de 50 qubits recuperados da IBM. |
| [04 — Calibração da leitura](brutos/04_mitigacao_leitura/README.md) | Temos as contagens das três rodadas reais. |

As pastas brutas 02 e 03 foram acrescentadas após recuperar os jobs históricos diretamente da IBM. Os resultados de comparação e ZNE produzidos no PC estão em simulados, identificados por experimento.

## Onde fica cada rodada da etapa 04?

| Rodada | Arquivo |
| --- | --- |
| 1 | [GHZ_leitura_dbccq67i0auc73dumdk0.json](brutos/04_mitigacao_leitura/GHZ_leitura_dbccq67i0auc73dumdk0.json) |
| 2 | [GHZ_leitura_dbccri9gv2cc73ea3630.json](brutos/04_mitigacao_leitura/GHZ_leitura_dbccri9gv2cc73ea3630.json) |
| 3 | [rodada_03/rodada_03.json](brutos/04_mitigacao_leitura/rodada_03/rodada_03.json) |

As duas primeiras rodadas foram importadas com nomes que contêm o ID do job IBM. A terceira foi registrada pelo programa de repetição, que também salvou os circuitos compilados em QPY. Seus dois arquivos ficaram juntos na pasta chamada originalmente `repeticoes`, agora chamada `rodada_03`. Essa pasta reúne os registros da terceira execução do mesmo protocolo. Uma nova rodada será salva em sua própria pasta numerada.
