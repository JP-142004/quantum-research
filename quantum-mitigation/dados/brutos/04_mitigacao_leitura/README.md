# Calibração da leitura · três rodadas reais

Em cada rodada, medimos 32 preparações de calibração e o GHZ em Z e X, com 1.000 medidas por circuito. O número da rodada leva às contagens originais.

| Rodada | Z: 00000 | Z: 11111 | Z: outros | X: par | X: ímpar |
| --- | --- | --- | --- | --- | --- |
| [1](GHZ_leitura_dbccq67i0auc73dumdk0.json) | 439 | 434 | 127 | 898 | 102 |
| [2](GHZ_leitura_dbccri9gv2cc73ea3630.json) | 445 | 419 | 136 | 898 | 102 |
| [3](rodada_03/rodada_03.json) | 454 | 441 | 105 | 903 | 97 |

Em X, a paridade depende do número de bits 1 em cada sequência. [Resultados ajustados](../../processados/04_mitigacao_leitura/README.md)


## Arquivos

| Arquivo | Conteúdo |
| --- | --- |
| [GHZ_leitura_dbccq67i0auc73dumdk0.json](GHZ_leitura_dbccq67i0auc73dumdk0.json) | Rodada 1. Contagens das 32 calibrações e do GHZ em Z e X, ID, backend e qubits. |
| [GHZ_leitura_dbccri9gv2cc73ea3630.json](GHZ_leitura_dbccri9gv2cc73ea3630.json) | Rodada 2. Mesmos tipos de contagens e metadados. |
| [rodada_03](rodada_03/README.md) | JSON e QPY da rodada 3. O JSON inclui versões, opções e análise original; o QPY guarda os circuitos enviados. |

![Indicadores das três rodadas antes e depois do ajuste](../../../figuras/04_comparacao_rodadas.png)

Os pontos resumem as contagens após o cálculo dos indicadores. As barras são um erro padrão e o eixo vertical é ampliado. As contagens originais estão na tabela e nos arquivos acima.
