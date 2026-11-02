# Como estudamos a mitigação de ruído

Quando um computador quântico dá um resultado inesperado, em que momento surgiu o erro? Ele pode ter ocorrido **durante o circuito**, enquanto as operações transformavam os qubits, ou **na leitura**, quando o aparelho registrou a resposta. Mitigar ruído significa tentar diminuir o efeito desses erros sobre o resultado que queremos medir.

Começamos com um circuito chamado GHZ porque sabemos o que esperar dele. Na primeira medida, os cinco bits deveriam aparecer todos iguais: `00000` ou `11111`. Se aparecer `00001`, temos um desvio. Só olhando esses cinco bits, não sabemos onde ele surgiu. Foi essa dúvida que orientou a pesquisa.

## A história dos experimentos

**1. Observamos o problema.** Com cinco qubits, 922 de 1.000 medidas deram todos zeros ou todos uns. Com cinquenta, apenas 109 de 1.000 deram esses resultados. Isso mostrou o tamanho do desvio naquela série. Para investigar sua origem, o projeto incluiu testes mais simples, como preparar apenas zeros. O código desses controles foi preservado, mas faltam as contagens para dizer o que cada teste encontrou. [Medidas de 5 a 50 qubits](experimentos/01_ghz_escala/README.md) · [Controles](experimentos/02_controles/README.md)

**2. Mudamos o caminho do circuito.** Duas construções podiam preparar o mesmo estado ideal. Uma delas seguia as conexões físicas do aparelho. A comparação histórica relata que isso reduziu de 13 para 4 as operações de dois qubits após a compilação. Cada operação a menos elimina uma oportunidade de introduzir erro. Para essa comparação, temos o relato, mas não as contagens originais. [Ver os dois desenhos](experimentos/03_ghz_conectado/README.md)

**3. Calibramos a leitura na IBM.** Preparamos respostas conhecidas e contamos como o aparelho as registrava. Depois usamos essas contagens para ajustar a estimativa do GHZ. Na terceira rodada, **895 de 1.000 medidas** deram todos zeros ou todos uns. Isso é **89,5% observado**. Com a calibração, a estimativa passou a **96,48%**. A diferença veio de um cálculo sobre as mesmas medidas. Nas três rodadas reais, o ajuste aproximou os dois indicadores analisados dos valores ideais. [Acompanhar a conta a partir das contagens](experimentos/04_mitigacao_leitura/README.md)

**4. No PC, separamos as causas.** No simulador, conseguimos escolher onde introduzir o erro. Quando havia apenas erro de leitura, a calibração exata recuperava o valor anterior à leitura. Quando acrescentamos erros nas operações, esse segundo efeito permanecia. Assim conseguimos testar o que cada intervenção fazia em condições conhecidas. [Comparar os cenários simulados](dados/simulados/README.md)

**5. Experimentamos outra técnica no simulador.** Executamos três versões do circuito com quantidades crescentes de operações sujeitas a erro. Usamos a tendência dos três resultados para estimar o que aconteceria se o ruído fosse reduzido a zero. Essa técnica se chama **ZNE**. Ela já foi testada no PC. A comparação com controles no equipamento real é uma próxima etapa planejada. [Ver o gráfico de ZNE](dados/simulados/zne/README.md) · [Plano experimental](docs/plano_experimentos.md)

## Para aprofundar

Os guias de cada etapa acima contêm os dados, as contas e os limites de interpretação. Para consultar um conceito específico ou reproduzir o código, use o [índice dos 12 capítulos](docs/livro/README.md). Para uma reunião, comece pelo [resumo das três rodadas reais](docs/resumo_orientador.md).

## Continuidade da pesquisa

Para cada novo circuito ou técnica, crie uma pasta com README e acrescente uma linha ao percurso. Registre a **pergunta**, o **circuito de teste** e seu resultado ideal, o **tipo de ruído** investigado, o **controle**, a **origem dos dados**, o **cálculo**, o **resultado com incerteza** e as **limitações**. Uma comparação com outro circuito pode ser acrescentada mesmo que seu indicador de interesse seja diferente de PZ ou CX.

| Técnica | O que investigar | Situação nesta pesquisa |
| --- | --- | --- |
| Extrapolação a ruído zero (ZNE) | Variar a exposição ao ruído e estimar o indicador no limite de ruído zero. A escolha do ajuste altera o resultado. | Piloto simulado concluído. [Método de dobramento](https://arxiv.org/abs/2005.10921) |
| Pauli twirling | Sortear operações de Pauli compensadas que preservam o circuito ideal e mudam como erros coerentes se acumulam na média. Requer várias versões do circuito. | Possibilidade futura. |
| Desacoplamento dinâmico | Inserir pulsos durante esperas para reduzir efeitos de certas perturbações. A duração das esperas e os erros dos pulsos influenciam o benefício. | Possibilidade futura. |
| Cancelamento probabilístico de erros (PEC) | Combinar amostras com pesos positivos e negativos com base em um modelo de ruído. A variância pode exigir muitos shots. | Possibilidade futura. |

Para comparar os mecanismos dessas técnicas, veja o [guia da IBM](https://quantum.cloud.ibm.com/docs/en/guides/error-mitigation-and-suppression-techniques) e o [trabalho de Temme e colaboradores](https://arxiv.org/abs/1612.02058). A escolha do próximo circuito e da próxima técnica permanece aberta.
