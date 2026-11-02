# 4. Quanto a correção da leitura aproxima os indicadores do ideal?

**Situação:** medido na IBM, com três rodadas. **Backend:** `ibm_fez`, qubits físicos 0 a 4. **Shots por circuito:** 1.000. A rodada 3 foi enviada em 1º de novembro de 2026. As rodadas 1 e 2 não registram a data nos arquivos.

## Pergunta

Se medirmos como o equipamento registra estados conhecidos, podemos usar essa informação para estimar melhor PZ e CX do GHZ?

## Por que esta pergunta

Recebemos `00001`. O circuito pode ter produzido `00001`, ou ter produzido `00000` e o leitor errou o último bit. Uma medida isolada não distingue os dois casos. Um conjunto de preparações conhecidas permite estimar com que frequência o leitor troca cada resposta por outra ([ruído de leitura](../../fundamentos/ruido.md)).

## Método

Cada rodada executou 34 circuitos de cinco qubits, 1.000 vezes cada:

| Circuitos | O que preparamos | Para quê |
| ---: | --- | --- |
| 32 | Cada sequência de `00000` a `11111`. Há 2 × 2 × 2 × 2 × 2 = 32. | Medir como cada preparação é registrada (calibração). |
| 1 | GHZ medido em Z. | Calcular PZ. |
| 1 | GHZ medido em X. | Calcular CX. |

**Ajuste.** Dividimos as contagens de cada preparação conhecida por 1.000 e formamos a matriz **A** (32 × 32). Cada coluna diz: "quando preparei esta sequência, quais respostas apareceram e com que frequência?". Seja **p** o vetor das frequências observadas do GHZ. Resolvemos **A q = p** e chamamos **q** de estimativa ajustada. PZ e CX ajustados saem de **q**.

**Exemplo com um bit (ilustrativo, não é dado real).** Suponha que o leitor registra 0 em 90% das vezes quando preparamos 0, e registra 0 em 20% das vezes quando preparamos 1. Se a fração verdadeira de zeros for x, observamos 0,90 x + 0,20 (1 − x). Observando 0,55, resolvemos 0,55 = 0,90 x + 0,20 (1 − x) e obtemos x = 0,50.

**Incerteza.** Bootstrap com 5.000 réplicas por rodada ([método](../../fundamentos/indicadores.md)).

## Dados

<!-- TABELA:rodadas_jobs -->
| Rodada | Job IBM | Backend | Data de envio | Circuitos | Shots por circuito | Medidas |
| ---: | --- | --- | --- | ---: | ---: | ---: |
| 1 | `dbccq67i0auc73dumdk0` | ibm_fez | não registrada | 34 | 1000 | 34.000 |
| 2 | `dbccri9gv2cc73ea3630` | ibm_fez | não registrada | 34 | 1000 | 34.000 |
| 3 | `dbjnndgnceqs73akbkh0` | ibm_fez | 2026-11-01 | 34 | 1000 | 34.000 |
| **Total** |  |  |  |  |  | **102.000** |
<!-- /TABELA:rodadas_jobs -->

As rodadas 1 e 2 estão em arquivos nomeados com o ID do job. A rodada 3 está na pasta [rodada_03](../../dados/brutos/04_mitigacao_leitura/rodada_03/README.md), que guarda também os circuitos compilados (QPY). A pasta se chamava `repeticoes` e foi renomeada. As três rodadas são o mesmo experimento. [Mapa dos arquivos](../../dados/brutos/04_mitigacao_leitura/README.md).

## Conta passo a passo: rodada 3

Abra o JSON da [rodada 3](../../dados/brutos/04_mitigacao_leitura/rodada_03/rodada_03.json) e procure `contagens` e `GHZ_Z`:

1. O Fez registrou `00000` 454 vezes e `11111` 441 vezes. Outras sequências: 105.
2. **PZ observado** = (454 + 441) / 1.000 = **0,895**.
3. Com a calibração da rodada 3, resolvemos **A q = p** para as 32 sequências e somamos as componentes de `00000` e `11111` em **q**. Resultado: **0,9648**.

O **0,895 foi observado e o 0,9648 foi calculado a partir das mesmas contagens.** Não houve uma segunda execução com 965 resultados corretos.

Em `GHZ_X`, contamos as sequências com número par de 1 (903) e ímpar (97). **CX observada** = (903 − 97) / 1.000 = **0,806**. Após o ajuste: **0,9702**.

## Resultado

<!-- TABELA:rodadas -->
| Rodada | PZ bruto → ajustado | CX bruta → ajustada |
| ---: | --- | --- |
| 1 | 0,8730 → 0,9436 | 0,7960 → 0,9440 |
| 2 | 0,8640 → 0,9360 | 0,7960 → 0,9481 |
| 3 | 0,8950 → 0,9648 | 0,8060 → 0,9702 |
<!-- /TABELA:rodadas -->

![Indicadores das três rodadas](../../figuras/comparacao_rodadas.png)

*Figura. Indicadores brutos e ajustados em cada rodada, com um erro padrão.*

### Quanto foi o ganho e qual a sua incerteza?

<!-- TABELA:rodadas_ganho -->
| Rodada | Indicador | Bruto | EP bruto | Ajustado | EP ajustado | Ganho | IC 95% do ganho |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | PZ | 0,8730 | 0,0104 | 0,9436 | 0,0130 | 0,0706 | 0,0585 a 0,0829 |
| 1 | CX | 0,7960 | 0,0194 | 0,9440 | 0,0235 | 0,1480 | 0,1359 a 0,1600 |
| 2 | PZ | 0,8640 | 0,0109 | 0,9360 | 0,0136 | 0,0720 | 0,0599 a 0,0849 |
| 2 | CX | 0,7960 | 0,0188 | 0,9481 | 0,0228 | 0,1521 | 0,1399 a 0,1644 |
| 3 | PZ | 0,8950 | 0,0098 | 0,9648 | 0,0125 | 0,0698 | 0,0580 a 0,0828 |
| 3 | CX | 0,8060 | 0,0186 | 0,9702 | 0,0229 | 0,1642 | 0,1519 a 0,1775 |
<!-- /TABELA:rodadas_ganho -->

![Ganho em cada rodada, com intervalo de 95%](../../figuras/ganho_rodadas.png)

*Figura. Ganho (ajustado menos bruto) e intervalo bootstrap de 95%.*

Os seis intervalos de 95% do ganho ficam acima de zero. O ajuste também **aumenta o erro padrão** do indicador: o custo de inverter a matriz. Relatório completo: [comparacao_rodadas.md](../../docs/comparacao_rodadas.md).

## O que este experimento mostra e o que não mostra

- **Mostra** que, nas três rodadas, os dois indicadores ficaram mais próximos de 1 depois do ajuste de leitura.
- **Não mostra** que erros das portas desapareceram. Um qubit que já saiu errado do circuito e foi lido corretamente não é corrigido.
- **Não separa** erro de leitura de erro de preparação: os estados de calibração também são preparados por portas.
- **Não é fidelidade:** PZ e CX não determinam o estado completo.
- O bootstrap contém só a variação de amostragem dentro de cada rodada, não a deriva entre dias.
- Os valores ajustados são estimativas e podem conter quasiprobabilidades negativas.

## Arquivos

| Arquivo | Para que serve |
| --- | --- |
| [mitigacao_leitura.py](mitigacao_leitura.py) | Programa que salva arquivos `GHZ_leitura_<job>.json`, o formato das rodadas 1 e 2. **Envia um job** ao ser executado. |
| [repetir_mitigacao.py](repetir_mitigacao.py) | Programa da rodada 3, com três ações: `--verificar` (local), `--enviar` e `--coletar`. Sem `--enviar`, nenhum job é enviado, e uma rodada já registrada não é reenviada. |
| [comparar_rodadas.py](../../scripts/comparar_rodadas.py) | Calcula os ajustes e o bootstrap das três rodadas, sem acessar a IBM. |

**Execução:** `mitigacao_leitura.py` **envia um job à IBM**; `repetir_mitigacao.py` só envia com `--enviar`. O job `dbjnndgnceqs73akbkh0` (rodada 3) já está concluído e não deve ser reenviado.

**Próxima pergunta:** se a leitura for corrigida, o que acontece com um erro que ocorreu dentro do circuito? [Experimento 5](../05_validacao_simulada/README.md).

[Experimentos](../README.md)
