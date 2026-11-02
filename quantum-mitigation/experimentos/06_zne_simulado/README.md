# 6. A extrapolação a ruído zero reduz o erro das portas?

**Situação:** simulado no PC (CPU, Qiskit Aer). **Data da execução:** 1º de novembro de 2026. **Shots por circuito:** 1.000. **Total:** 3 blocos × 42 circuitos × 1.000 = **126.000 shots simulados**. **Não foi executado na IBM.**

## Pergunta

Se executarmos o circuito com ruído de portas crescente e extrapolarmos o indicador até ruído zero, chegamos mais perto do valor ideal do que o circuito sem modificação?

## Por que esta pergunta

O [experimento 5](../05_validacao_simulada/README.md) mostrou que a calibração de leitura não desfaz o erro das portas. A extrapolação a ruído zero (ZNE) ataca esse erro ([técnica](../../fundamentos/tecnicas.md)).

## Método

1. **Versões com mais ruído.** Para o GHZ conectado, criamos três versões com o mesmo resultado ideal. As versões maiores inserem pares de operações que se anulam no caso ideal. Os **fatores de ruído** são 1, 3 e 5, e os circuitos compilados têm **4, 12 e 20 portas CX**.
2. **Correção de leitura.** Cada versão é ajustada pela calibração do bloco ([experimento 4](../04_mitigacao_leitura/README.md)).
3. **Extrapolação.** Ajustamos uma **reta** aos três valores, em função do fator, e lemos o valor em fator 0.

Cada bloco tem 42 circuitos: 32 de calibração, 6 versões do GHZ (3 fatores × Z e X) e 4 controles independentes.

## Conta passo a passo

Pelas referências exatas do modelo, sem flutuação de shots:

- PZ nos fatores 1, 3 e 5: 0,9463, 0,8490 e 0,7637. A cada fator, PZ cai.
- Reta ajustada por mínimos quadrados e lida em fator 0: **0,9899**.

O valor 0,9899 é uma **previsão**, não uma medida. Nenhum GHZ com zero portas foi executado.

## Resultado

<!-- TABELA:zne -->
| Fator de ruído | Portas CX | PZ (referência do modelo) | CX (referência do modelo) |
| ---: | ---: | ---: | ---: |
| 1 | 4 | 0,9463 | 0,9224 |
| 3 | 12 | 0,8490 | 0,7847 |
| 5 | 20 | 0,7637 | 0,6676 |
| 0 (extrapolado) | — | **0,9899** | **0,9826** |
<!-- /TABELA:zne -->

![Referência exata dos fatores e reta extrapolada](../../figuras/06_zne_fatores.png)

*Figura. Cálculo exato do modelo. Círculos: fatores 1, 3 e 5. Losangos: valor extrapolado no fator 0. A linha tracejada marca o ideal.*

A extrapolação aproximou os dois indicadores de 1, mas **não chegou a 1**: 1 − 0,9899 = 0,0101 em Z e 1 − 0,9826 = 0,0174 em X. A queda do indicador com o número de portas não é perfeitamente linear. Esse resíduo é o **viés** do ajuste linear.

### Com contagens finitas (três blocos amostrados)

<!-- TABELA:zne_blocos -->
| Bloco | PZ, fator 1, ajustado | PZ após ZNE | CX, fator 1, ajustada | CX após ZNE |
| ---: | ---: | ---: | ---: | ---: |
| 1 | 0,9639 ± 0,0188 | 1,0072 ± 0,0226 | 0,9190 ± 0,0351 | 0,9532 ± 0,0434 |
| 2 | 0,8868 ± 0,0185 | 0,9135 ± 0,0218 | 0,9579 ± 0,0353 | 1,0582 ± 0,0435 |
| 3 | 0,9763 ± 0,0188 | 1,0065 ± 0,0224 | 0,8914 ± 0,0375 | 0,9283 ± 0,0455 |
<!-- /TABELA:zne_blocos -->

![Fatores e extrapolação nos três blocos](../../figuras/06_zne_blocos.png)

*Figura. Círculos: fatores 1, 3 e 5 após correção de leitura. Losango: extrapolação. Barras: um erro padrão. Linha em 1: ideal.*

Com 1.000 shots por circuito:

- **A incerteza aumenta.** O erro padrão após a ZNE é maior que o do fator 1 em todos os blocos.
- **Os valores variam entre blocos.** O bloco 2 ficou mais de 3 erros padrão abaixo da referência de 0,9463 já no fator 1 (0,8868 ± 0,0185). Esse é o maior desvio da auditoria (ver [limites do experimento 5](../05_validacao_simulada/README.md#limites)), e não investigamos sua causa.
- **Estimativas acima de 1** (por exemplo, 1,0072) são possíveis, porque a inversão da leitura e a extrapolação não ficam restritas ao espaço físico.

## Limites

- Apenas simulação, com ruído sintético depolarizante nas portas. A ZNE no hardware depende de como o ruído real cresce com as portas, o que não testamos.
- A reta é uma escolha. Outras curvas dariam outro resultado e outro viés.
- Três blocos não bastam para estimar a cobertura dos intervalos.
- Só um circuito, GHZ de cinco qubits na construção conectada.
- O custo não foi comparado com o de outras técnicas: a ZNE usou 3 versões do circuito, com até 5 vezes mais portas.

## Arquivos

| Arquivo | Para que serve |
| --- | --- |
| [protocolo_local.py](../../scripts/protocolo_local.py) | Constrói as versões do circuito e calcula a extrapolação. |
| [validar_protocolo_local.py](../../scripts/validar_protocolo_local.py) | Executa os blocos. |
| [zne.qpy](../../dados/simulados/validacao_2026_11_01/zne.qpy) | Circuitos compilados dos fatores. |
| [zne_leitura_e_portas_bloco_01_analise.json](../../dados/simulados/validacao_2026_11_01/zne_leitura_e_portas_bloco_01_analise.json) | Análise do bloco 1. Os blocos 2 e 3 têm os arquivos correspondentes na mesma pasta. |

**Execução:** locais, sem acesso à IBM.

**Próxima pergunta:** a ZNE se comporta assim no hardware? Esse é um dos [próximos passos](../../README.md#o-que-vem-a-seguir).

[Experimentos](../README.md)
