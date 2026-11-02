# 04 — Calibração e mitigação de leitura

[Experimentos](../README.md) · [Teoria da mitigação](../../docs/livro/04-mitigacao-leitura/README.md) · [Resultados reais](../../docs/livro/05-experimentos-reais/README.md)

O protocolo real prepara 32 estados de calibração e GHZ conectado em Z/X, com 1.000 shots por circuito. Os cinco qubits físicos são 0–4 e o backend registrado é `ibm_fez`. As opções registradas da rodada 3 deixam DD e twirling desativados e inicialização habilitada.

## Dois programas, comportamentos diferentes

| Programa | Funcionamento |
| --- | --- |
| [mitigacao_leitura.py](mitigacao_leitura.py) | Versão histórica: `JOB_ID` vazio envia um job; preenchido consulta o job indicado. O corpo do arquivo executa essas ações. Salva contagens e imprime análise com 300 bootstraps. |
| [repetir_mitigacao.py](repetir_mitigacao.py) | Versão que separa verificação ideal, envio e coleta por argumentos; grava registro e QPY da rodada. |

`repetir_mitigacao.py --verificar` confere idealmente os 34 circuitos sem acessar o serviço, embora o módulo importe a dependência Runtime. `--coletar` consulta o job já registrado e pode salvar contagens/análise; se ainda não terminou, retorna sem aguardar indefinidamente. `--enviar` exige que o arquivo daquela rodada não exista, compila e submete uma rodada real. Números menores que 3 são reservados às históricas.

A semente de ordem é 42 + número da rodada; a semente de compilação é 42. A análise da coleta usa 300 réplicas e semente 2000 + rodada. O limite de execução solicitado é 120 segundos, diferente de tempo de fila. O envio recusa mapeamento inesperado; as conexões precisam existir no backend escolhido.

## Rodada 3 concluída

O job `dbjnndgnceqs73akbkh0` já terminou. O [JSON](../../dados/brutos/04_mitigacao_leitura/repeticoes/rodada_03.json), o [QPY](../../dados/brutos/04_mitigacao_leitura/repeticoes/rodada_03.qpy) e o [relatório original](../../docs/rodada_03.md) estão preservados. Não é necessário consultar ou enviar esse job para reproduzir a análise consolidada: use [comparar_rodadas.py](../../scripts/comparar_rodadas.py), que é local.

O script de repetição implementa o protocolo antigo de 34 circuitos. Ele **não** implementa a proposta nova de 40 circuitos com duas construções e controles; essa proposta foi implementada e validada apenas no executor local.

## Uma calibração que dá para resolver à mão

Suponha, como exemplo didático, que o detector leia 1 em 10% dos zeros e leia 0 em 20% dos uns. Se a fração de zeros antes da leitura era x, a fração observada de zeros é 0,90x + 0,20(1 − x). Se observamos 0,55, a conta fica x = (0,55 − 0,20)/0,70 = 0,50. O ajuste usa as taxas de confusão que medimos.

Com cinco qubits existem 32 sequências. Cada coluna de A descreve uma preparação conhecida. Por exemplo, a coluna de `00001` é construída dividindo cada contagem de `cal_00001` por 1.000. As linhas indicam qual sequência foi lida. Repetimos para todas as colunas. Para cada base, montamos o vetor p das frequências GHZ e resolvemos A q = p. O vetor q fornece as estimativas ajustadas. Como as colunas também dependem de preparar os estados corretamente, a calibração pode incluir erros de preparação.

## Seguindo a rodada 3

1. No [JSON do job](../../dados/brutos/04_mitigacao_leitura/repeticoes/rodada_03.json), abra `contagens.GHZ_Z`. Os extremos têm 454 e 441 registros. Portanto PZ bruto = (454 + 441)/1.000 = **0,895**.
2. Resolva o sistema em Z com as 32 colunas daquela rodada. Some os componentes de q para `00000` e `11111`: **PZ ajustado = 0,9648**. O ganho de aproximadamente 0,0698 foi calculado sobre os mesmos shots.
3. Em `GHZ_X`, separe as sequências conforme tenham quantidade par ou ímpar de bits 1. São 903 pares e 97 ímpares. A correlação bruta vale (903 − 97)/1.000 = **0,806**. Após a inversão em X, some as estimativas pares e subtraia as ímpares: **0,9702**.

| Rodada | PZ bruto → ajustado | Correlação em X bruta → ajustada |
| --- | --- | --- |
| 1 | 0,8730 → 0,9436 | 0,7960 → 0,9440 |
| 2 | 0,8640 → 0,9360 | 0,7960 → 0,9481 |
| 3 | 0,8950 → 0,9648 | 0,8060 → 0,9702 |

Mil repetições fornecem uma estimativa. Se repetíssemos a coleta, as frequências variariam, inclusive as usadas para estimar A. Para avaliar essa variação, o [programa de comparação](../../scripts/comparar_rodadas.py) sorteia novas contagens a partir das frequências salvas e refaz o cálculo 5.000 vezes por rodada. Esse procedimento é o *bootstrap*. Cada réplica usa a mesma amostra GHZ para o bruto e o ajustado. Na terceira rodada, o erro padrão de PZ foi aproximadamente 0,0098 antes do ajuste e 0,0125 depois. Ele mede incerteza de amostragem sob o modelo. A variação do equipamento entre dias é outra questão.

![PZ e correlação em X nas três rodadas reais, com um erro padrão](../../figuras/comparacao_rodadas.png)

[Contagens, indicadores e intervalos das três rodadas](../../docs/comparacao_rodadas.md).
