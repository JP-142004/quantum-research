# 1. Como o desvio cresce com o tamanho do circuito?

**Situação:** medido na IBM. **Backend e data:** os programas preservados usam `ibm_kingston` (o de cinco qubits escolhe o backend livre com `least_busy`). O arquivo de contagens não registra backend nem data, então a origem de cada seção não pode ser comprovada. **Shots por circuito:** 1.000.

## Pergunta

Se um GHZ ideal produz apenas `00…0` ou `11…1` em Z, que fração das medidas cai nesses dois resultados quando o número de qubits aumenta?

## Método

- **Circuito de teste:** H no qubit 0 e uma porta CX do qubit 0 para cada um dos outros. Medida em Z. O compilador adapta o circuito às conexões do equipamento.
- **Tamanhos:** de 5 a 50 qubits, de 5 em 5.
- **Indicador:** PZ, a fração das medidas todos zeros ou todos uns ([definição](../../fundamentos/indicadores.md)). Valor ideal: 1.
- **Técnica avaliada:** nenhuma. Este experimento mede o desvio antes de qualquer intervenção.

## Conta passo a passo

Na seção de cinco qubits do [arquivo de contagens](../../dados/brutos/01_ghz_escala/ghz_05_a_50.txt):

- `00000` apareceu 477 vezes e `11111` apareceu 445 vezes.
- PZ = (477 + 445) / 1.000 = **0,922**. Restaram 78 resultados diferentes.

Para cinquenta qubits: (106 + 3) / 1.000 = **0,109**, com 891 resultados diferentes. O programa [resumir_resultados.py](../../scripts/resumir_resultados.py) repete essa conta para os dez tamanhos.

## Resultado

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

![PZ em função do número de qubits](../../dados/imagens/escala_observada.png)

*Figura. Fração das 1.000 medidas que deram todos zeros ou todos uns, para GHZ de 5 a 50 qubits. Cada ponto é uma execução.*

O desvio cresce de forma contínua com o tamanho do circuito nessa série. O erro padrão de cada ponto, só por amostragem, é de cerca de 0,01.

## Limites

- O tamanho do circuito varia junto com o número de portas, o roteamento e a profundidade. O experimento **não separa** esses fatores.
- Não há metadados de backend e data no arquivo. Não comparar diretamente com resultados de outros dias ou equipamentos.
- É uma única execução por tamanho, sem repetição.

## Arquivos

| Arquivo | Para que serve |
| --- | --- |
| [ghz_05.py](ghz_05.py), [ghz_10.py](ghz_10.py), [ghz_15.py](ghz_15.py), [ghz_20.py](ghz_20.py), [ghz_25.py](ghz_25.py) | Programas para 5 a 25 qubits. |
| [ghz_30.py](ghz_30.py), [ghz_35.py](ghz_35.py), [ghz_40.py](ghz_40.py), [ghz_45.py](ghz_45.py), [ghz_50.py](ghz_50.py) | Programas para 30 a 50 qubits. |
| [ghz_05_a_50.txt](../../dados/brutos/01_ghz_escala/ghz_05_a_50.txt) | Contagens originais. |
| [resumo_escala.csv](../../dados/processados/resumo_escala.csv) | Tabela de PZ calculada das contagens. |

**Execução:** os programas `ghz_*.py` **enviam novos jobs à IBM**. Para recalcular a tabela sem acessar a IBM, execute `scripts/resumir_resultados.py`.

**Próxima pergunta:** parte desse desvio já aparece ao preparar estados muito simples? [Experimento 2](../02_controles/README.md).

[Experimentos](../README.md)
