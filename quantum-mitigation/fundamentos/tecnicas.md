# Técnicas de mitigação

**Mitigação não é correção de erros.** A correção de erros protege os qubits durante a computação e exige qubits adicionais. A mitigação, segundo van den Berg et al. (2023), só busca estimativas corretas de valores esperados, tratando o equipamento como ele é. Este projeto estuda mitigação.

| # | Técnica | Fonte de ruído que ataca | Situação | Experimento |
| --- | --- | --- | --- | --- |
| 1 | Construção do circuito com menos portas | Portas, decoerência | Medida na IBM | [3](../experimentos/03_ghz_conectado/README.md) |
| 2 | Calibração de leitura | Leitura | Medida na IBM, 3 rodadas | [4](../experimentos/04_mitigacao_leitura/README.md) |
| 3 | Extrapolação a ruído zero (ZNE) | Portas | Simulada | [6](../experimentos/06_zne_simulado/README.md) |
| 4 | Twirling de Pauli | Ruído coerente | Planejada | — |
| 5 | Desacoplamento dinâmico | Decoerência | Planejada | — |
| 6 | Cancelamento probabilístico de erros (PEC) | Portas | Planejada | — |

Os termos "leitura", "portas" e "decoerência" estão explicados em [ruido.md](ruido.md).

## 1. Construção com menos portas

**Ideia.** O mesmo estado pode ser preparado por sequências diferentes de portas. Se uma sequência exige CX entre qubits que não são vizinhos, o compilador insere portas extras. Escolher a sequência que segue as conexões físicas reduz as portas executadas.

**Por que ajuda.** Se cada CX tivesse 1% de chance de erro (valor só ilustrativo), a chance de nenhuma dar erro em 13 portas seria 0,99¹³ ≈ 0,88, e em 4 portas, 0,99⁴ ≈ 0,96. Menos portas, menos chances de erro.

**O que medimos.** Nas contas do experimento 3, o GHZ original ficou com 13 portas de dois qubits e o conectado com 4. O GHZ conectado liga os qubits em árvore, a partir do qubit 2: 2→1, 2→3, 1→0, 3→4.

**Limite.** Reduz o erro das portas, mas não o elimina.

## 2. Calibração de leitura

**Ideia.** A leitura às vezes registra o bit errado. Se medirmos como o equipamento registra cada preparação conhecida, podemos desfazer essa distorção nas contagens do circuito que nos interessa.

**Exemplo com um qubit** (números ilustrativos, não são dados reais). Preparamos 0 e o leitor registra 0 em 90% das vezes. Preparamos 1 e o leitor registra 0 em 20% das vezes. Organizamos isso numa matriz **A**, em que cada coluna é uma preparação e cada linha, o que foi registrado:

| | preparado 0 | preparado 1 |
| --- | ---: | ---: |
| registrou 0 | 0,90 | 0,20 |
| registrou 1 | 0,10 | 0,80 |

No circuito, observamos **p** = (0,55 ; 0,45) (55% de zeros). A estimativa corrigida **q** é a que, passada pela matriz, reproduz o observado: **A q = p**, ou seja, **q = A⁻¹ p**. Aqui o determinante de A é 0,90×0,80 − 0,20×0,10 = 0,70, e

q₀ = (0,80×0,55 − 0,20×0,45) / 0,70 = 0,35 / 0,70 = **0,50**, e q₁ = 0,50.

Conferência: 0,90×0,50 + 0,20×0,50 = 0,55. ✓

**No projeto.** Com 5 qubits há 2⁵ = 32 preparações possíveis (de `00000` a `11111`), então **A** é 32 × 32 e cada rodada tem 32 circuitos de calibração. Com n qubits seriam 2ⁿ, o que limita este método a poucos qubits; Bravyi et al. (2021) descrevem modelos que reduzem esse custo.

**Limites.** A calibração também absorve parte do erro de preparação, porque os estados de calibração são preparados por portas. Ela não desfaz o erro das portas do circuito. A inversão pode dar componentes ligeiramente negativas (quasiprobabilidades) e indicadores acima de 1; não as recortamos porque isso introduziria viés ([indicadores.md](indicadores.md)). O erro padrão do resultado ajustado é maior que o do bruto.

## 3. Extrapolação a ruído zero (ZNE)

**Ideia.** Não dá para desligar o ruído, mas dá para aumentá-lo de forma controlada e ver como o resultado piora. Prolongando essa tendência para trás, estima-se o valor com ruído zero.

**Como aumentar o ruído.** Seja U o bloco de portas que prepara o GHZ. Executamos U, depois o seu inverso U⁻¹ (que desfaz U) e depois U de novo: U · U⁻¹ · U. No caso ideal isso dá o mesmo estado que U sozinho, mas há três vezes mais portas e, portanto, mais ruído. Repetindo o par U⁻¹ · U mais uma vez, chegamos a cinco vezes. Chamamos de **fator de ruído** 1, 3 e 5 essas três versões. No GHZ conectado, elas têm 4, 12 e 20 portas CX.

**Conta com os números do experimento 6** (valores exatos do modelo, sem flutuação de shots). PZ nos fatores 1, 3 e 5 vale 0,9463, 0,8490 e 0,7637. Ajustamos uma reta por mínimos quadrados:

- Com pontos igualmente espaçados, a inclinação é (0,7637 − 0,9463) / (5 − 1) = **−0,04565** por unidade de fator.
- A média de PZ é 0,8530 e a média dos fatores é 3. No fator 0: 0,8530 + 3 × 0,04565 ≈ **0,990**. O script, que usa os valores sem arredondar, dá 0,9899.

**Limites.** A queda real do indicador não é perfeitamente linear, então a reta deixa um erro sistemático (**viés**): aqui, 1 − 0,9899 = 0,0101. O resultado depende da curva escolhida, e a incerteza aumenta ([experimento 6](../experimentos/06_zne_simulado/README.md)). Referências: Temme, Bravyi e Gambetta (2017); Giurgica-Tiron et al. (2020).

## Técnicas planejadas

Ainda não testadas neste projeto. As duas primeiras existem como opções de execução do serviço da IBM e ficaram **desativadas** nas rodadas medidas.

- **Twirling de Pauli.** Insere portas de Pauli aleatórias antes e depois de cada CX, de modo que o circuito ideal não muda. O ruído passa a se comportar como uma mistura de erros simples, mais fácil de mitigar (Wallman e Emerson, 2016).
- **Desacoplamento dinâmico.** Insere sequências de pulsos nos períodos em que um qubit espera, para reduzir o efeito do ambiente (Viola, Knill e Lloyd, 1999).
- **Cancelamento probabilístico de erros (PEC).** Aprende-se um modelo do ruído das portas, e o circuito é executado com variações sorteadas cuja combinação cancela o ruído em média. Evita o viés da ZNE, mas exige caracterizar o ruído e mais amostras (van den Berg et al., 2023).

[Fundamentos](README.md) · [Ruído](ruido.md) · [Indicadores](indicadores.md) · [Referências](referencias.md)
