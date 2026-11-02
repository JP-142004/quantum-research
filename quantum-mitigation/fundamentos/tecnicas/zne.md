# Extrapolação a ruído zero (ZNE)

**Ideia.** Não dá para desligar o ruído, mas dá para aumentá-lo de forma controlada e ver como o resultado piora. Prolongando essa tendência para trás, estima-se o valor com ruído zero.

**Como aumentar o ruído.** Seja U o bloco de portas que prepara o estado. Executamos U, depois o seu inverso U⁻¹ (que desfaz U) e depois U de novo: U · U⁻¹ · U. No caso ideal isso dá o mesmo estado que U sozinho, mas há três vezes mais portas e, portanto, mais ruído. Repetindo o par U⁻¹ · U mais uma vez, chegamos a cinco vezes. Chamamos de **fator de ruído** 1, 3 e 5 essas três versões. No GHZ conectado de 5 qubits, elas têm 4, 12 e 20 portas CX.

## Conta com números

Valores exatos de um modelo simulado, sem flutuação de shots (de uma execução anterior do projeto). PZ nos fatores 1, 3 e 5 vale 0,9463, 0,8490 e 0,7637. Ajustamos uma reta por mínimos quadrados:

- Com pontos igualmente espaçados, a inclinação é (0,7637 − 0,9463) / (5 − 1) = **−0,04565** por unidade de fator.
- A média de PZ é 0,8530 e a média dos fatores é 3. No fator 0: 0,8530 + 3 × 0,04565 ≈ **0,990**.

## Limites

- A queda real do indicador não é perfeitamente linear, então a reta deixa um erro sistemático (**viés**).
- O resultado depende da curva escolhida, e a incerteza aumenta.
- O valor no fator 0 é uma **previsão**, não uma medida: nenhum circuito com zero portas é executado.

Referências: Temme, Bravyi e Gambetta (2017); Giurgica-Tiron et al. (2020).

[Técnicas](README.md)
