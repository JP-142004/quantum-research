# Experimento 1 · Como o desvio cresce com o tamanho do circuito?

**Onde e quando:** IBM. Os programas preservados usam `ibm_kingston`, mas o arquivo de contagens não registra backend nem data, então a origem de cada seção não pode ser comprovada. **Shots por circuito:** 1.000.

## Pergunta

Um GHZ ideal só produz `00…0` ou `11…1`. Que fração das medidas cai nesses dois resultados quando o número de qubits aumenta? É o ponto de partida: mede o desvio **antes** de qualquer técnica de mitigação.

## Como foi feito

- **Circuito:** H no qubit 0 e uma CX do qubit 0 para cada um dos outros ([conceitos](../../fundamentos/conceitos.md)), medido em Z. O compilador adapta o circuito às conexões do equipamento.
- **Tamanhos:** de 5 a 50 qubits, de 5 em 5. Um circuito de cada tamanho.
- **Indicador:** **PZ**, a fração das medidas que deram todos zeros ou todos uns. Vale 1 no caso ideal ([definição](../../fundamentos/indicadores.md)).

## Resultado

Conta para 5 qubits, nas contagens originais: `00000` apareceu 477 vezes e `11111`, 445. PZ = (477 + 445) / 1.000 = **0,922**; sobraram 78 resultados diferentes. Para 50 qubits: (106 + 3) / 1.000 = **0,109**.

<!-- TABELA:escala -->
| Qubits | Todos zeros | Todos uns | Outros | PZ |
| ---: | ---: | ---: | ---: | ---: |
| 5 | 477 | 445 | 78 | 0,922 |
| 10 | 407 | 333 | 260 | 0,740 |
| 15 | 368 | 233 | 399 | 0,601 |
| 20 | 299 | 178 | 523 | 0,477 |
| 25 | 310 | 144 | 546 | 0,454 |
| 30 | 245 | 63 | 692 | 0,308 |
| 35 | 242 | 43 | 715 | 0,285 |
| 40 | 194 | 25 | 781 | 0,219 |
| 45 | 184 | 3 | 813 | 0,187 |
| 50 | 106 | 3 | 891 | 0,109 |
<!-- /TABELA:escala -->

![PZ em função do número de qubits](../../figuras/01_escala_observada.png)

*Fração das 1.000 medidas que deram todos zeros ou todos uns, para GHZ de 5 a 50 qubits. Cada ponto é uma execução; o erro padrão de cada um, só por amostragem, é de cerca de 0,01.*

## Conclusão

Nessa série, o desvio cresce de forma contínua com o tamanho do circuito: PZ cai de 0,922 para 0,109. O experimento **não separa** o efeito do número de qubits do efeito do número de portas e do roteamento, que crescem juntos. É uma única execução por tamanho e não há backend nem data registrados, então a série não deve ser comparada diretamente com outros resultados.

## Próximo passo

Parte desse desvio já aparece ao preparar estados muito simples, sem emaranhamento? [Experimento 2](../02_controles/README.md).

## Arquivos

| Arquivo | Para que serve |
| --- | --- |
| `ghz_05.py` a `ghz_50.py` (dez programas) | Um programa por tamanho. |
| [Contagens originais](../../dados/brutos/README.md#01--escala-do-ghz) | Dados brutos. |
| [resumo_escala.csv](../../dados/processados/resumo_escala.csv) | Tabela de PZ calculada das contagens por [resumir_resultados.py](../../scripts/resumir_resultados.py). |

**Execução:** os programas `ghz_*.py` **enviam novos jobs à IBM**. Para recalcular a tabela sem acessar a IBM, use `scripts/resumir_resultados.py`.

[Experimentos](../README.md)
