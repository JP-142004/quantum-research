# PIBIC — síntese para discussão com o orientador

**Data:** 1 de novembro de 2026. **Etapa:** mitigação de leitura de GHZ com cinco qubits. **Situação:** três execuções concluídas; análise exclusivamente local, sem novos envios.

## Pergunta e método

Investigamos em que medida a calibração da leitura modifica dois indicadores do GHZ conectado: a população nos estados 00000 e 11111 (PZ) e a correlação coletiva em X (CX). Cada execução no ibm_fez, nos qubits 0–4, reúne os 32 estados de calibração e dois circuitos GHZ, com 1.000 medidas por circuito. São 102.000 medidas nas três execuções.

A matriz de calibração relaciona estados preparados a resultados registrados. O ajuste resolve A q = p, mantendo quasiprobabilidades negativas. Recalculamos as três rodadas com 5.000 réplicas bootstrap por rodada, incluindo a incerteza da calibração e do GHZ. O ganho é calculado de forma pareada, usando as mesmas contagens reamostradas para o indicador bruto e o ajustado.

## Resultados

Valores acompanhados de um erro padrão de amostragem, não de intervalo de 95%:

| Rodada | PZ bruto | PZ ajustado | CX bruto | CX ajustado |
| --- | ---: | ---: | ---: | ---: |
| 1 | 0,8730 ± 0,0104 | 0,9436 ± 0,0130 | 0,7960 ± 0,0194 | 0,9440 ± 0,0235 |
| 2 | 0,8640 ± 0,0109 | 0,9360 ± 0,0136 | 0,7960 ± 0,0188 | 0,9481 ± 0,0228 |
| 3 | 0,8950 ± 0,0098 | 0,9648 ± 0,0125 | 0,8060 ± 0,0186 | 0,9702 ± 0,0229 |

O ganho em PZ foi de 0,0698 a 0,0720; em CX, de 0,1480 a 0,1642. Todos os seis intervalos percentis individuais de 95% para o ganho ficaram acima de zero. Isso descreve o efeito do ajuste sob o modelo utilizado, sem estabelecer isoladamente a origem física dos desvios.

![Comparação das três execuções](../figuras/comparacao_rodadas.png)

## Interpretação e limites

O efeito tem o mesmo sinal nas três execuções, sustentando repetibilidade preliminar neste conjunto de qubits. As matrizes têm condição próxima de 1,2 e não apresentam instabilidade numérica relevante. O ajuste aumenta a incerteza, que deve acompanhar qualquer apresentação dos valores corrigidos.

A aproximação ao ideal não prova que os erros de portas foram eliminados, nem fornece a fidelidade completa do GHZ. A calibração pode incorporar erros de preparação; o bootstrap não inclui toda a deriva do equipamento ou falhas do modelo. Três execuções não demonstram estabilidade em outros dias, backends ou tamanhos. As duas rodadas históricas não registram datas, versões ou circuitos compilados, limitando a comparação retrospectiva.

## Próxima etapa proposta

Priorizar três novos blocos experimentais que comparem, sob uma calibração comum por bloco, a construção original e a conectada, com controles independentes em Z e X. O protocolo proposto tem 40 circuitos e 40.000 medidas por bloco, totalizando 120.000 medidas. Esse é um orçamento de amostras, não uma estimativa de tempo ou custo do serviço.

Antes do hardware, validar localmente os estados ideais, o mapeamento e as operações compiladas. Só depois de avaliar esses controles, considerar um piloto de ZNE. O [plano detalhado](plano_experimentos.md) define controles, critérios de avaliação e limites de interpretação. Nenhuma nova execução foi realizada nesta etapa.

## Pontos para decidir na reunião

1. Confirmar se a prioridade é validar a mitigação de leitura e o benefício da construção conectada antes de expandir o número de qubits.
2. Discutir o orçamento proposto de três blocos e a possibilidade de executá-los em janelas distintas.
3. Definir se uma etapa posterior deve estimar fidelidade com medições adicionais ou explorar ZNE.

Os IDs, hashes dos dados, intervalos do ganho e método completo estão na [análise das rodadas](comparacao_rodadas.md). A rodada 3 corresponde ao job `dbjnndgnceqs73akbkh0`, já concluído. A modelagem de leitura segue o canal clássico de atribuição descrito pela [IBM](https://quantum.cloud.ibm.com/docs/en/tutorials/readout-error-mitigation-sampler); o cálculo local usa a matriz completa, não M3.
