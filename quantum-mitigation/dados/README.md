# Dados da pesquisa

| Tipo | Como os dados são obtidos |
| --- | --- |
| [Brutos](brutos/README.md) | Circuitos executados no hardware da IBM produzem sequências de bits. As contagens registram quantas vezes cada sequência apareceu. |
| [Processados](processados/README.md) | Scripts locais leem as contagens reais e calculam indicadores, ajustes de leitura e incertezas. |
| [Simulados](simulados/README.md) | Um simulador no PC executa os circuitos com um modelo de ruído definido. As contagens e a análise ficam associadas à execução que as gerou. |

Dentro de cada tipo, escolha o experimento para consultar o método, os resultados e os arquivos de origem. Para incluir outra técnica ou circuito, acrescente uma pasta no tipo correspondente, registre a origem dos dados e liste o experimento no índice dessa categoria.

## Por que os dados brutos têm pastas 01 e 04?

Os números identificam as etapas dos experimentos. Cada rodada é uma nova execução de uma etapa.

| Etapa | Dados disponíveis |
| --- | --- |
| [01 — Escala GHZ](brutos/01_ghz_escala/README.md) | Contagens dos circuitos de 5 a 50 qubits. |
| [02 — Controles](../experimentos/02_controles/README.md) | Temos os scripts. As contagens históricas separadas não foram recuperadas na importação. |
| [03 — Construção conectada](../experimentos/03_ghz_conectado/README.md) | Temos os scripts e resultados relatados. As contagens históricas dessas comparações e do circuito conectado de 50 qubits não foram recuperadas. |
| [04 — Calibração da leitura](brutos/04_mitigacao_leitura/README.md) | Temos as contagens das três rodadas reais. |

As pastas brutas 02 e 03 poderão ser acrescentadas quando houver registros de contagens disponíveis. Os resultados de comparação e ZNE produzidos no PC estão em simulados, identificados por experimento.

## Onde fica cada rodada da etapa 04?

| Rodada | Arquivo |
| --- | --- |
| 1 | [GHZ_leitura_dbccq67i0auc73dumdk0.json](brutos/04_mitigacao_leitura/GHZ_leitura_dbccq67i0auc73dumdk0.json) |
| 2 | [GHZ_leitura_dbccri9gv2cc73ea3630.json](brutos/04_mitigacao_leitura/GHZ_leitura_dbccri9gv2cc73ea3630.json) |
| 3 | [rodada_03/rodada_03.json](brutos/04_mitigacao_leitura/rodada_03/rodada_03.json) |

As duas primeiras rodadas foram importadas com nomes que contêm o ID do job IBM. A terceira foi registrada pelo programa de repetição, que também salvou os circuitos compilados em QPY. Seus dois arquivos ficaram juntos na pasta chamada originalmente `repeticoes`, agora chamada `rodada_03`. Essa pasta reúne os registros da terceira execução do mesmo protocolo. Uma nova rodada será salva em sua própria pasta numerada.
