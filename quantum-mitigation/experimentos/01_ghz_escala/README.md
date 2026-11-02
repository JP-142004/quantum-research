# 1. O que muda quando o circuito cresce?

## Refazendo a primeira comparação

Na seção de cinco qubits do [texto de contagens](../../dados/brutos/01_ghz_escala/ghz_05_a_50.txt), some as frequências dos dois resultados esperados: 477 + 445 = 922. Divida pelos 1.000 shots: PZ = 0,922. Restaram 78 resultados intermediários. Para cinquenta qubits, a mesma conta dá (106 + 3)/1.000 = 0,109, com 891 resultados intermediários. O [programa de resumo](../../scripts/resumir_resultados.py) aplica essa operação a cada tamanho. Aqui observamos o desvio antes de aplicar uma técnica. A pergunta seguinte é se parte dele já aparece ao preparar um estado simples.

[Experimentos](../README.md) · [Teoria de construção e medidas](../../docs/livro/03-circuitos-medidas/README.md)

## Pergunta

Como a população nos resultados todos zeros e todos uns muda ao aumentar o tamanho do GHZ? Os circuitos usam H no qubit 0 e CX de 0 para cada outro qubit, depois medem em Z. O compilador adapta essa construção às conexões do backend.

## Arquivos

| Scripts | Tamanhos |
| --- | --- |
| [ghz_05.py](ghz_05.py), [ghz_10.py](ghz_10.py), [ghz_15.py](ghz_15.py), [ghz_20.py](ghz_20.py), [ghz_25.py](ghz_25.py) | 5, 10, 15, 20 e 25 qubits |
| [ghz_30.py](ghz_30.py), [ghz_35.py](ghz_35.py), [ghz_40.py](ghz_40.py), [ghz_45.py](ghz_45.py), [ghz_50.py](ghz_50.py) | 30, 35, 40, 45 e 50 qubits |

Todos usam 1.000 shots. O script de cinco qubits seleciona `least_busy`; apesar de conter uma constante com nome de backend, a seleção efetiva é feita por essa chamada. Os demais usam `ibm_kingston` no código preservado. Isso não prova, sozinho, qual backend gerou cada seção do texto histórico: os metadados do arquivo são incompletos.

## Dados disponíveis

As contagens estão em [ghz_05_a_50.txt](../../dados/brutos/01_ghz_escala/ghz_05_a_50.txt); a tabela derivada está em [resumo_escala.csv](../../dados/processados/resumo_escala.csv). O parser exige dez seções, tamanhos esperados, bitstrings válidas e 1.000 contagens por seção.

PZ cai de 0,922 em cinco qubits para 0,109 em cinquenta nessa série. A interpretação precisa considerar compilação, quantidade de portas, diferenças de execução e ausência de metadados completos. O experimento não separa essas causas.

**Execução:** esses programas submetem novos circuitos reais quando executados. Para recalcular a tabela, execute apenas `scripts/resumir_resultados.py` conforme o guia local; isso não usa a IBM.
