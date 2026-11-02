# 4. Quanto do desvio pode vir da leitura?

Imagine receber `00001`. O circuito pode ter produzido exatamente esse resultado, ou o leitor pode ter registrado incorretamente um dos bits. Uma medida isolada não permite escolher entre essas explicações. No IBM Fez, primeiro medimos como o leitor respondia a preparações conhecidas. Depois usamos essa informação ao analisar o GHZ.

## O que rodou na IBM

Uma **rodada** é um conjunto de circuitos. Um **shot** é uma repetição de um circuito. Cada rodada usou os qubits físicos 0–4 e teve:

| Quantos circuitos? | O que fizemos? | Para quê? |
| ---: | --- | --- |
| 32 | Preparamos cada sequência de cinco bits, de `00000` a `11111`. | Medir como cada preparação era registrada. |
| 1 | Medimos o GHZ em Z. | Contar todos zeros e todos uns. |
| 1 | Medimos o GHZ em X. | Avaliar a correlação coletiva, sensível à coerência. |

Há 32 preparações porque cada um dos cinco bits tem duas possibilidades: 2 × 2 × 2 × 2 × 2 = 32. Cada circuito foi medido 1.000 vezes. Portanto, **34.000 shots por rodada e 102.000 nas três rodadas reais**.

## Como funciona o ajuste? Um exemplo de um bit

Imagine um leitor que registra zero em 90% das vezes quando preparamos zero, mas também registra zero em 20% das vezes quando preparamos um. Se metade das entradas fosse zero, a fração de zeros observados seria 0,90 × 0,50 + 0,20 × 0,50 = **0,55**.

Agora faça a conta ao contrário. Chamando de x a fração de zeros antes da leitura, temos 0,55 = 0,90x + 0,20(1 − x). Resolvendo, x = 0,50. Nesse **exemplo didático**, observar 55% de zeros leva a uma estimativa de 50% antes da leitura.

No experimento real, há 32 sequências. Cada preparação conhecida fornece uma coluna da tabela de confusão A. Dividimos suas contagens por 1.000. Depois resolvemos A q = p, em que p reúne as frequências observadas do GHZ e q reúne as estimativas ajustadas. A preparação dos estados conhecidos também pode introduzir erros, uma limitação do modelo.

## Siga uma rodada real

Abra a [rodada 3](../../dados/brutos/04_mitigacao_leitura/repeticoes/rodada_03.json) e procure `contagens.GHZ_Z`. O Fez registrou 454 vezes `00000` e 441 vezes `11111`. As outras sequências apareceram 105 vezes. Logo, **PZ observado = (454 + 441)/1.000 = 0,895**.

No PC, ajustamos todas as 32 frequências com a calibração daquela rodada. A soma dos dois extremos de q foi **0,9648**. Essa é uma estimativa sobre as mesmas medidas. O arquivo bruto continua contendo exatamente 895 resultados esperados.

Em `GHZ_X`, agrupamos as sequências pelo número de bits 1. Foram 903 resultados com quantidade par e 97 com quantidade ímpar. A correlação observada foi **(903 − 97)/1.000 = 0,806**. Após o ajuste, a correlação estimada foi **0,9702**. Essa grandeza vai de −1 a 1 para a distribuição física e tem alvo ideal +1 neste circuito.

| Rodada | PZ observado → ajustado | Correlação X observada → ajustada |
| --- | --- | --- |
| 1 | 0,8730 → 0,9436 | 0,7960 → 0,9440 |
| 2 | 0,8640 → 0,9360 | 0,7960 → 0,9481 |
| 3 | 0,8950 → 0,9648 | 0,8060 → 0,9702 |

A conclusão é que os dois indicadores se aproximaram do ideal nas três rodadas. Com outras mil repetições, as contagens poderiam variar. Para estimar essa incerteza, o [programa de análise local](../../scripts/comparar_rodadas.py) sorteia novas contagens com base nas frequências salvas e refaz o cálculo 5.000 vezes por rodada. Esse procedimento chama-se *bootstrap*. Na rodada 3, PZ passou de 0,8950 ± 0,0098 para 0,9648 ± 0,0125, com um erro padrão de amostragem. O ajuste aproximou a estimativa do ideal e aumentou sua incerteza.

![Indicadores das três rodadas reais com um erro padrão](../../figuras/comparacao_rodadas.png)

## Onde estão o código e os resultados?

O [programa histórico](mitigacao_leitura.py) pode iniciar um job real quando executado com ID vazio. O [programa de repetição](repetir_mitigacao.py) separa verificação local, submissão e coleta. O job da terceira rodada, `dbjnndgnceqs73akbkh0`, está concluído. Para estudar o resultado, consulte a [comparação com intervalos e diagnósticos](../../docs/comparacao_rodadas.md).

**Próxima pergunta:** se a leitura for corrigida, o que acontece com um erro que já ocorreu dentro do circuito? Investigamos isso no [passo 5, no PC](../../dados/simulados/README.md).
