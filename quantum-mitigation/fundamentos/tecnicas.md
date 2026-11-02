# Técnicas de mitigação

**Mitigação não é correção de erros.** A correção de erros protege os qubits durante a computação e exige qubits adicionais. A mitigação, segundo van den Berg et al. (2023), só busca estimativas corretas de valores esperados, tratando o equipamento como ele é. Este projeto estuda mitigação.

## Situação de cada técnica

| # | Técnica | Fonte que ataca | Situação neste projeto | Onde |
| --- | --- | --- | --- | --- |
| 1 | Construção do circuito com menos portas | Portas, decoerência | **Medida na IBM** (5 qubits) | [Experimento 3](../experimentos/03_ghz_conectado/README.md) |
| 2 | Mitigação de leitura por matriz de calibração completa | Leitura | **Medida na IBM**, três rodadas | [Experimento 4](../experimentos/04_mitigacao_leitura/README.md) |
| 3 | Extrapolação a ruído zero (ZNE) | Portas | **Simulada** no PC | [Experimento 6](../experimentos/06_zne_simulado/README.md) |
| 4 | Twirling de Pauli e compilação aleatória | Ruído coerente | Planejada | — |
| 5 | Desacoplamento dinâmico (DD) | Decoerência em tempo ocioso | Planejada | — |
| 6 | Cancelamento probabilístico de erros (PEC) | Portas | Planejada | — |
| 7 | Combinações das anteriores | Várias | Planejada | — |

As técnicas 4 e 5 existem como opções de execução do serviço da IBM. Ficaram **desativadas** nas opções registradas da rodada 3, de modo que os resultados da calibração de leitura não as incluem.

## Em poucas linhas

**1. Construção do circuito.** O mesmo estado pode ser preparado por sequências diferentes de portas. Em um processador onde só alguns pares de qubits são vizinhos, uma sequência que exige interação entre qubits distantes obriga o compilador a inserir operações extras. Escolher uma sequência que segue as conexões físicas reduz as portas executadas. Medimos essa redução e seu efeito.

**2. Mitigação de leitura.** Prepara-se cada resultado possível, mede-se como o equipamento o registra e monta-se uma matriz **A**, em que cada coluna mostra as frequências observadas para uma preparação. Depois resolve-se **A q = p**, em que **p** são as frequências observadas e **q** a estimativa corrigida. Com *n* qubits são necessárias 2ⁿ calibrações. Isso limita o método a poucos qubits. Bravyi et al. (2021) descrevem modelos que reduzem esse custo. Aplicamos a matriz completa, com 5 qubits e 32 calibrações.

**3. Extrapolação a ruído zero.** Executa-se o circuito com níveis de ruído crescentes, por exemplo repetindo pares de portas que se anulam no caso ideal. Ajusta-se uma curva ao indicador em função do nível de ruído e prolonga-se até ruído zero (Temme, Bravyi e Gambetta, 2017; Giurgica-Tiron et al., 2020). O resultado depende do tipo de curva escolhido e costuma ter incerteza maior.

**4. Twirling de Pauli.** Insere-se aleatoriamente portas de Pauli antes e depois das portas de dois qubits, de forma que o circuito ideal não mude. O ruído passa a se comportar como uma mistura de erros de Pauli (Wallman e Emerson, 2016). Costuma ser preparação para outras técnicas, como a PEC.

**5. Desacoplamento dinâmico.** Insere-se sequências de pulsos nos períodos em que um qubit espera, para reduzir o efeito do ambiente (Viola, Knill e Lloyd, 1999).

**6. Cancelamento probabilístico de erros.** Aprende-se um modelo do ruído das portas, e cada circuito é executado com variações sorteadas cuja combinação cancela, em média, o ruído (van den Berg et al., 2023). Permite estimativas sem o viés típico da ZNE, mas exige caracterizar o ruído e mais amostras.

## Como acrescentar uma técnica

1. Inclua uma linha na tabela acima com a fonte de ruído atacada e a situação `Planejada`.
2. Copie [experimentos/_modelo](../experimentos/_modelo/README.md) para uma pasta numerada nova.
3. Preencha pergunta, circuito de teste, controle, custo em medidas e critério de sucesso **antes** de executar.
4. Depois de executar, guarde as contagens em `dados/` e mude a situação para `Medida na IBM` ou `Simulada`.
5. Acrescente a referência em [referencias.md](referencias.md).

[Fundamentos](README.md) · [Ruído](ruido.md) · [Indicadores](indicadores.md)
