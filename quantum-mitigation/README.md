# Avaliação de técnicas de mitigação de ruído em circuitos quânticos

## Resumo

Estudamos quanto diferentes técnicas de mitigação aproximam os resultados de um circuito quântico dos valores esperados. A primeira etapa usa o estado GHZ como referência experimental. Em três execuções no IBM Fez, a calibração de leitura aumentou a população nos estados esperados em cerca de sete pontos percentuais por execução. Em simulação, avaliamos também o efeito da construção do circuito e da extrapolação a ruído zero. Esses ensaios estabelecem um protocolo para testar outras técnicas no GHZ antes de estender a comparação a outros circuitos.

**Para acompanhar uma medida do começo ao fim:** [1. Escala](experimentos/01_ghz_escala/README.md) → [2. Controles](experimentos/02_controles/README.md) → [3. Reconstrução](experimentos/03_ghz_conectado/README.md) → [4. Calibração na IBM](experimentos/04_mitigacao_leitura/README.md) → [5. Teste no PC](dados/simulados/README.md) → [6. ZNE no PC](dados/simulados/zne/README.md).

## 1. Introdução e objetivo

Um circuito pode produzir resultados diferentes dos ideais porque as operações físicas são imperfeitas ou porque o equipamento registra incorretamente o resultado da medição. Essas duas fontes de desvio pedem intervenções diferentes. Por exemplo, encurtar o circuito pode reduzir sua exposição a erros de portas. Já calibrar a leitura permite ajustar a estimativa calculada a partir das medidas.

Nosso objetivo é avaliar, para um mesmo circuito de referência, quanto cada intervenção muda os indicadores medidos e qual incerteza acompanha essa mudança. Escolhemos o GHZ porque conhecemos sua resposta ideal em duas bases de medição. Isso permite avaliar cada técnica com uma referência comum.

## 2. Método

**Circuito e indicadores.** Para cinco qubits, o GHZ ideal produz apenas `00000` ou `11111` na base Z. Calculamos **PZ** somando as contagens dessas duas sequências e dividindo pelo total. Como essa medida sozinha também seria compatível com uma mistura clássica de zeros e uns, medimos uma segunda propriedade na base X. A **correlação em X** é a fração de resultados com número par de bits 1 menos a fração com número ímpar. Os dois indicadores valem 1 para o GHZ positivo ideal.

**Intervenções.** Mantivemos o estado ideal como alvo e avaliamos três mudanças, cada uma com sua própria referência experimental.

| Intervenção | Comparação |
| --- | --- |
| Construção do circuito | Comparamos o GHZ original, que exige interações a partir de um único qubit, com uma construção que segue as conexões físicas. [Circuitos](experimentos/03_ghz_conectado/README.md) |
| Mitigação de leitura | Em cada rodada no Fez, preparamos os 32 estados conhecidos de cinco qubits e medimos como foram registrados. Usamos essa matriz de calibração para ajustar as medidas do GHZ em Z e X. Foram 34 circuitos e 1.000 medidas por circuito. [Protocolo e contas](experimentos/04_mitigacao_leitura/README.md) |
| Extrapolação a ruído zero (ZNE) | No simulador, aumentamos o número de operações da preparação sem mudar seu resultado ideal. Ajustamos uma reta aos indicadores de três versões e estimamos o valor no fator de ruído zero. [Protocolo e gráfico](dados/simulados/zne/README.md) |

**Incerteza.** Para as três rodadas reais, sorteamos 5.000 novas amostras de contagens por rodada a partir das frequências observadas (*bootstrap*). Em cada amostra, recalculamos a calibração e o indicador. Assim estimamos a incerteza da diferença entre o resultado bruto e o ajustado, que usam as mesmas medidas.

## 3. Resultados

**Hardware.** Uma série inicial de 5 a 50 qubits mostrou queda de PZ de 0,922 para 0,109. Isso motivou investigar os desvios em um circuito menor. Na comparação histórica de cinco qubits, a construção conectada reduziu a contagem relatada de portas de dois qubits de 13 para 4. Os arquivos brutos dessa comparação de construções não foram recuperados. [Série de escala](experimentos/01_ghz_escala/README.md)

A comparação de leitura dispõe das contagens das três rodadas no Fez, totalizando 102.000 medidas. A tabela mostra os indicadores antes e depois do ajuste.

| Rodada | PZ bruto → ajustado | Correlação em X bruta → ajustada |
| --- | ---: | ---: |
| 1 | 0,8730 → 0,9436 | 0,7960 → 0,9440 |
| 2 | 0,8640 → 0,9360 | 0,7960 → 0,9481 |
| 3 | 0,8950 → 0,9648 | 0,8060 → 0,9702 |

Na terceira rodada, 454 medidas deram todos zeros e 441 deram todos uns. Logo, PZ bruto foi (454 + 441)/1.000 = 0,895. O valor 0,9648 é a estimativa obtida após aplicar a calibração às mesmas contagens. O ganho foi 0,0698, com intervalo bootstrap de 95% de aproximadamente 0,0580 a 0,0828. [Resultados e incertezas das três rodadas](docs/comparacao_rodadas.md)

**Simulação.** Com ruído de portas conhecido, o PZ antes da leitura foi 0,8409 na construção original e 0,9463 na conectada, pelas referências exatas do modelo. No piloto de ZNE com a construção conectada, os circuitos com 4, 12 e 20 portas CX produziram referências de PZ de 0,9463, 0,8490 e 0,7637. A extrapolação desses valores resultou em 0,9899. [Resultados simulados e controles](dados/simulados/validacao_2026_11_01/relatorio.md)

## 4. Discussão

A mitigação de leitura aproximou os dois indicadores do ideal nas três rodadas reais. A calibração, porém, depende de preparar estados conhecidos e pode incorporar erros de preparação. O intervalo calculado representa a variação de amostragem dentro de uma rodada. A estabilidade em outras condições de hardware continua em aberto.

No modelo simulado, a construção conectada reduziu a exposição a portas ruidosas, enquanto a calibração compensou os desvios introduzidos na leitura. O piloto de ZNE aproximou o PZ de 1, com resultado dependente da reta usada e maior incerteza nas estimativas amostradas. Como as técnicas foram avaliadas em condições diferentes, os números atuais não sustentam uma classificação geral entre elas.

## 5. Conclusão e continuidade

O próximo passo é **manter o GHZ como circuito de teste**. Para cada nova técnica, compararemos uma execução de referência com a intervenção, usando os mesmos indicadores, registrando as condições, o custo em medidas e as incertezas. A proposta imediata é comparar as duas construções com calibração e controles independentes no hardware. Depois de caracterizar as técnicas no GHZ, repetiremos as comparações selecionadas em outros circuitos, definindo para cada um seu resultado ideal e seu indicador de desempenho. [Plano experimental](docs/plano_experimentos.md)

[Dados do projeto](dados/README.md) · [Reprodução local](docs/livro/09-reproducao/README.md) · [Teoria e referências complementares](docs/livro/README.md)
