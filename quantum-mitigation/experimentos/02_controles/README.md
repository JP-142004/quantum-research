# 2. O desvio já aparece em estados simples?

**Situação:** medido na IBM. **Backends:** `ibm_kingston` e `ibm_fez`, conforme a tabela. **Datas:** 20 e 21 de outubro de 2026. **Shots por circuito:** 1.000. As contagens e os circuitos foram recuperados diretamente da conta IBM em 2 de novembro de 2026 ([recuperação](../../docs/recuperacao_etapas_02_03.json)).

## Pergunta

Preparamos um estado cuja resposta é conhecida (todos zeros, todos uns, um qubit só). O equipamento devolve o que preparamos?

## Por que esta pergunta

O experimento 1 não indica se o desvio vem do emaranhamento ou de algo mais básico. Um controle sem emaranhamento isola uma parte do problema. Ele mistura **preparação e leitura**, e não separa uma da outra.

## Método

| Programa | O que prepara |
| --- | --- |
| [todos_zeros.py](todos_zeros.py) | Cinco qubits em `0`, qubits físicos 0 a 4. |
| [todos_uns.py](todos_uns.py) | Porta X nos cinco qubits, resultado esperado `11111`. |
| [qubits_individuais.py](qubits_individuais.py) | `0` e `1` separadamente nos qubits físicos 0 e 1. |
| [comparar_zeros.py](comparar_zeros.py) | Qubit 0 sozinho, qubit 1 sozinho e os cinco juntos. |

**Indicador:** fração das medidas iguais ao estado preparado. Para o conjunto, qualquer bit diferente conta como desvio.

## Resultado

<!-- TABELA:controles -->
| Experimento | Backend | Data do job | Circuito | Preparado | Medidas iguais ao preparado | Fração |
| --- | --- | --- | --- | --- | ---: | ---: |
| todos_zeros | ibm_kingston | 2026-10-20 | zeros | `00000` | 528/1000 | 0,528 |
| todos_uns | ibm_kingston | 2026-10-20 | uns | `11111` | 768/1000 | 0,768 |
| individuais_kingston | ibm_kingston | 2026-10-21 | q0_zero | `0` | 249/1000 | 0,249 |
| individuais_kingston | ibm_kingston | 2026-10-21 | q0_um | `1` | 915/1000 | 0,915 |
| individuais_kingston | ibm_kingston | 2026-10-21 | q1_zero | `0` | 1000/1000 | 1,000 |
| individuais_kingston | ibm_kingston | 2026-10-21 | q1_um | `1` | 957/1000 | 0,957 |
| individuais_fez | ibm_fez | 2026-10-21 | q0_zero | `0` | 992/1000 | 0,992 |
| individuais_fez | ibm_fez | 2026-10-21 | q0_um | `1` | 973/1000 | 0,973 |
| individuais_fez | ibm_fez | 2026-10-21 | q1_zero | `0` | 989/1000 | 0,989 |
| individuais_fez | ibm_fez | 2026-10-21 | q1_um | `1` | 978/1000 | 0,978 |
| zeros_separados_juntos | ibm_fez | 2026-10-21 | q0_zero | `0` | 991/1000 | 0,991 |
| zeros_separados_juntos | ibm_fez | 2026-10-21 | q1_zero | `0` | 991/1000 | 0,991 |
| zeros_separados_juntos | ibm_fez | 2026-10-21 | zeros | `00000` | 942/1000 | 0,942 |
<!-- /TABELA:controles -->

![Controles de estados conhecidos](../../dados/imagens/controles_reais.png)

*Figura. Fração das 1.000 medidas iguais ao estado preparado, por teste, backend e circuito.*

## O que os números mostram

- **No Fez**, os qubits 0 e 1 preparados sozinhos acertam entre 97,3% e 99,2%.
- **No Kingston**, o qubit 0 preparado em `0` devolveu `0` em apenas 249 de 1.000 medidas, enquanto o qubit 1 devolveu `0` em todas as 1.000. O mesmo qubit 0 preparado em `1` devolveu `1` em 915 de 1.000. Nos controles do Kingston, o desvio foi maior em um qubit específico, e **os dados não permitem atribuir uma causa**: poderia ser leitura, inicialização, estado do equipamento naquele dia, ou outra.
- **Cinco qubits juntos, no Fez:** 942 de 1.000. Se cada qubit acertasse 99,1% das vezes, de forma independente, esperaríamos 0,991⁵ ≈ 0,956, ou seja, cerca de 956 de 1.000. A diferença de 0,014 é de cerca de 1,9 erro padrão (≈ 0,0074). **Não é evidência clara de que medir juntos piora a leitura.** Esta conta supõe os cinco qubits com o desempenho medido para os qubits 0 e 1.

## Limites

- Os testes foram feitos em jobs, dias e backends diferentes. **Não comparar** diretamente, por exemplo, o 528/1.000 do Kingston (cinco zeros) com o 249/1.000 do mesmo backend (qubit 0 sozinho): foram jobs distintos, em dias distintos.
- Cada teste tem uma só repetição.
- A calibração do [experimento 4](../04_mitigacao_leitura/README.md) trata a leitura de forma sistemática: mede as 32 preparações possíveis na mesma rodada do GHZ.

## Arquivos

| Arquivo | Para que serve |
| --- | --- |
| [brutos/02_controles](../../dados/brutos/02_controles/README.md) | Contagens e circuitos (JSON e QPY) dos cinco jobs. |
| [resultados_recuperados.json](../../dados/processados/02_controles/resultados_recuperados.json) | Uma linha por circuito, com job, backend e acertos. |

**Execução:** os quatro programas **enviam jobs à IBM** quando executados. Para estudar os resultados, abra os dados.

**Próxima pergunta:** como chegar ao mesmo GHZ com menos operações? [Experimento 3](../03_ghz_conectado/README.md).

[Experimentos](../README.md)
