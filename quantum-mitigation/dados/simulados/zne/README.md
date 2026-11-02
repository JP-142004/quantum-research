# 6. Por que colocar mais operações em um circuito com ruído?

Queríamos investigar o erro que permanece após ajustar a leitura. Para isso criamos três versões do GHZ conectado. As versões maiores têm operações extras que, em condições ideais, se desfazem entre si. Todas deveriam dar a mesma resposta. No modelo escolhido, porém, cada porta CX acrescenta ruído. Podemos então observar quanto o resultado muda quando aumentamos deliberadamente essa exposição.

| Versão | Portas CX | PZ na referência do modelo após descontar a leitura |
| --- | ---: | ---: |
| Fator 1 | 4 | 0,946261 |
| Fator 3 | 12 | 0,848950 |
| Fator 5 | 20 | 0,763687 |

Ajustamos uma reta a esses três pontos e a prolongamos até o fator zero. O intercepto vale (13 × 0,946261 + 4 × 0,848950 − 5 × 0,763687)/12 ≈ **0,9899**. Esse ponto zero é uma previsão baseada nas três versões. É daí que vem o nome **extrapolação a ruído zero (ZNE)**.

![Indicadores simulados nos três fatores e previsão no fator zero](../../../figuras/zne_fatores.png)

As linhas representam as retas ajustadas, e os losangos no fator zero são previsões. Para a correlação X, a mesma conta dá **0,9826**. Mesmo conhecendo os valores sem flutuação de shots, a reta deixa uma diferença em relação ao ideal 1. A curva verdadeira do modelo não é exatamente uma reta.

## E quando usamos apenas mil medidas?

Em cada bloco, foram 32 calibrações, seis circuitos GHZ (três fatores medidos em Z e X) e quatro controles. Com três blocos, são 42 × 1.000 × 3 = **126.000 shots simulados**. No primeiro bloco, o PZ ajustado do fator 1 foi 0,9639 ± 0,0188. A extrapolação deu 1,0072 ± 0,0226. A estimativa pode ultrapassar 1 porque vem de uma reta ajustada a dados com incerteza. Conservamos esse valor para que o efeito da extrapolação seja visível.

O piloto foi realizado no PC. Seu resultado descreve o modelo testado. Uma execução em hardware faz parte das possibilidades futuras. [Código do dobramento e do ajuste](../../../scripts/protocolo_local.py) · [Dados do primeiro bloco](../validacao_2026_11_01/zne_leitura_e_portas_bloco_01_analise.json) · [Relatório completo](../validacao_2026_11_01/relatorio.md)
