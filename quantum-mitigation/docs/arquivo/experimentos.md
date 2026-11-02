# Sequência dos experimentos

[Livro e estado atual da pesquisa](../../README.md). Este documento conserva a sequência histórica; o livro detalha teoria, reprodução e resultados posteriores.

## 1. GHZ original: de 5 a 50 qubits

Preparamos um GHZ com H no qubit 0 e CNOTs desse qubit para os demais. Medimos diretamente, na base Z. No caso ideal, metade das medidas dá todos zeros e metade dá todos uns. Com um número finito de medidas, não esperamos uma divisão exatamente 50/50.

Medimos a população nos dois estados esperados:

`PZ = [contagem(00...0) + contagem(11...1)] / total`.

O complemento, `1 - PZ`, é a fração dos outros resultados. O arquivo de contagens dessa rodada está em `dados/brutos/01_ghz_escala/`. Apesar do nome original da pasta conter “Simulações”, os scripts submetem jobs ao serviço IBM; o texto salvo não documenta todos os metadados necessários para reconstruir cada execução.

## 2. Controles com estados conhecidos

Medimos todos zeros, depois todos uns. Também comparamos qubits individuais com cinco qubits medidos juntos. O objetivo era verificar desvios mesmo sem preparar um GHZ.

A métrica é a fração que difere do estado preparado, para o conjunto ou para cada qubit. Esses testes incluem preparação, eventuais portas e leitura: sozinhos, não separam essas fontes de erro. Comparações feitas em backends ou momentos diferentes não isolam uma causa.

Os scripts estão preservados, mas não havia arquivos de contagens separados desses controles na pasta importada.

## 3. Construção seguindo as conexões físicas

Em cinco qubits, a construção conectada usa H na raiz 2 e CNOTs nas conexões `(2,1), (2,3), (1,0), (3,4)`. Ela prepara o mesmo estado ideal com menos operações de roteamento.

Resultados informados na conversa, no Fez, com 1.000 medidas por circuito:

| Indicador | GHZ anterior | GHZ conectado |
| --- | ---: | ---: |
| Portas de dois qubits após compilação | 13 | 4 |
| Profundidade em Z | 35 | 13 |
| PZ | 0,833 | 0,888 |
| Correlação em X, em outra rodada | 0,566 | 0,774 |

Os arquivos brutos dessas comparações não estavam na pasta importada. A melhoria observada é compatível com o benefício de reduzir a quantidade de operações, sem identificar isoladamente o tipo de ruído.

O script conectado de 50 qubits também foi importado. Não foi encontrado um arquivo de resultados dessa execução; portanto não atribuímos a ele uma melhoria medida.

## 4. Por que medir também na base X?

Somente obter zeros e uns em Z não demonstra a coerência do GHZ. Por isso, antes de medir, aplicamos H em cada qubit. Essa mudança permite medir a correlação coletiva em X usando a leitura habitual do equipamento.

Contamos quantos resultados têm número par ou ímpar de bits 1:

`CX = (N_par - N_impar) / total`.

Para o GHZ com sinal positivo, o ideal é `CX = +1`: todos os resultados têm paridade par nessa base. Em cinco qubits existem 16 sequências pares possíveis. O resultado `11111` é ímpar, mas na base X ele não é um dos dois únicos resultados ideais, como ocorre na base Z.

No GHZ conectado observado, foram 887 resultados pares e 113 ímpares: `(887 - 113)/1000 = 0,774`. Portanto, 0,774 é uma correlação; a fração de paridade par foi 88,7%.

PZ e CX verificam propriedades diferentes. Nenhum dos dois, isoladamente, é a fidelidade completa do estado.

## 5. Mitigação de leitura — análise em desenvolvimento

Foram preparados os 32 estados conhecidos de cinco qubits e medido como o equipamento os registrou. Essas contagens formam uma matriz A: cada coluna representa um estado preparado, cada linha um resultado observado. Depois medimos o GHZ em Z e X. São 34 circuitos por rodada.

O ajuste resolve `A × p_ajustada = p_observada`. Ele muda a estimativa calculada a partir das contagens; não muda o circuito executado ou suas contagens brutas. A calibração também pode incorporar erros de preparação.

| Job | PZ bruto | PZ ajustado | CX bruto | CX ajustado |
| --- | ---: | ---: | ---: | ---: |
| `dbccq67i0auc73dumdk0` | 0,8730 | 0,9436 | 0,7960 | 0,9440 |
| `dbccri9gv2cc73ea3630` | 0,8640 | 0,9360 | 0,7960 | 0,9481 |

Esses números podem ser recalculados dos dois JSONs importados. O script original usa bootstrap para estimar a incerteza de amostragem de calibração e GHZ. Isso não inclui toda a variação do hardware ou o erro do modelo.

Valores negativos pequenos após o ajuste são quasiprobabilidades produzidas pela inversão; não são frequências negativas observadas. A análise desta etapa continua em desenvolvimento. Ainda não concluímos quanto da melhora permanece em outras rodadas, tamanhos ou calibrações.

Não foi encontrado código ou resultado de ZNE na pasta histórica importada. Posteriormente foi implementado e executado um [piloto local de ZNE](livro/08-zne/README.md), com dados simulados. A execução de ZNE no hardware continua sendo uma possibilidade futura.

## 6. Comparação consolidada de três execuções

A terceira rodada foi concluída no job `dbjnndgnceqs73akbkh0`. A [comparação das três rodadas](../comparacao_rodadas.md) recalcula os indicadores e suas incertezas com 5.000 réplicas bootstrap. Consulte também o [resumo para o orientador](resumo_orientador.md) e o [plano de próximos experimentos](../plano_experimentos.md). A tabela da seção 5 permanece como registro das duas execuções históricas; não representa a totalidade dos resultados disponíveis.
