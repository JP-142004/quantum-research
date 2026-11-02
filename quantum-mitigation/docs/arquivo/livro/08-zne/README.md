# 08. Extrapolação a ruído zero

[← Anterior](../07-simulacao-local/README.md) · [Índice do livro](../../../../README.md) · [Próximo →](../09-reproducao/README.md)

## A ideia de ZNE

ZNE significa *zero-noise extrapolation*, ou extrapolação a ruído zero. Produzimos estimativas com diferentes níveis de ruído, ajustamos uma função e estimamos seu valor no limite de ruído zero. O projeto usa um piloto local com dobramento unitário. A técnica e suas escolhas de escala e extrapolação são discutidas por [Giurgica-Tiron e colaboradores](https://arxiv.org/abs/2005.10921).

## Como aumentar operações sem mudar o alvo ideal

Chamando a preparação de U, acrescentamos pares de blocos inverso/original, cuja composição ideal é identidade. O código executa U e, em seguida, repete U† e U. Usamos fatores nominais 1, 3 e 5. As medições não fazem parte desse dobramento; as H finais para medir X também ficam fora dele.

| Fator nominal | Blocos de preparação | CX compiladas |
| ---: | --- | ---: |
| 1 | U | 4 |
| 3 | U, U†, U | 12 |
| 5 | U, U†, U, U†, U | 20 |

As barreiras impedem a simplificação através das fronteiras dos blocos na compilação usada. Os testes conferem a distribuição ideal e a contagem de CX após compilar. Se o compilador apagasse os pares inversos, não teríamos ampliado as operações como planejado.

Fator 3 não significa que medimos uma intensidade física de ruído exatamente três vezes maior. É um rótulo de construção, cuja relação com o ruído depende das portas e do modelo.

## Protocolo executado no PC

Cada bloco contém 32 calibrações, seis circuitos GHZ (três fatores × duas bases) e quatro controles: 42 circuitos. Foram três blocos de 1.000 shots por circuito, ou 126.000 shots simulados. Todos usaram o cenário de leitura + portas do capítulo anterior.

Primeiro mitigamos a leitura em cada fator. Depois ajustamos uma reta por mínimos quadrados ordinários nos pontos de fator 1, 3 e 5. Para valores $y_1,y_3,y_5$, o intercepto calculado pelo código é

$$\hat y_0=\frac{13}{12}y_1+\frac13y_3-\frac5{12}y_5.$$

O coeficiente negativo mostra por que a extrapolação pode ampliar flutuações. Não recortamos o resultado para o intervalo físico. Em cada réplica bootstrap, a calibração é compartilhada entre fatores e as contagens de cada circuito são reamostradas separadamente. Assim calculamos também a diferença entre ZNE e fator 1 com sua covariância.

## Referência sem flutuação de shots

| Base | Fator 1 | Fator 3 | Fator 5 | Intercepto linear 1,3,5 | Intercepto linear só 1,3 |
| --- | ---: | ---: | ---: | ---: | ---: |
| Z | 0,946261 | 0,848950 | 0,763687 | 0,989897 | 0,994917 |
| X | 0,922368 | 0,784717 | 0,667608 | 0,982634 | 0,991194 |

Esses valores vêm do modelo exato após remover a leitura. Mesmo sem flutuação estatística, a reta não recupera exatamente 1: existe viés de aproximação. Mudar a faixa de fatores muda a extrapolação. O objetivo dessa comparação é expor essa sensibilidade, não escolher retrospectivamente a opção que chega mais perto do ideal.

## Resultados amostrados e limites

No bloco 1, por exemplo, PZ após mitigação de leitura no fator 1 foi 0,9639 ± 0,0188; o ZNE linear foi 1,0072 ± 0,0226. O valor acima de 1 é uma estimativa não restringida com flutuação, não uma probabilidade física maior que 100%. Todos os blocos, inclusive os menos favoráveis, estão no [relatório](../../../../dados/simulados/validacao_2026_11_01/relatorio.md).

Uma parábola em três pontos interpola os três pontos e não deixa graus de liberdade para avaliar o ajuste residual; não seria, por si só, validação de um modelo melhor. O piloto usa a reta pré-definida. Não implementamos busca automática de ajustes favoráveis, nem demonstramos ZNE em hardware.

**O que está pronto:** construção, verificação ideal, simulação e análise do piloto. **O que falta:** avaliar seu protocolo em um backend real, após validar os controles e as condições de execução. O [plano experimental](../../../plano_experimentos.md) separa essas etapas.

---

[← Anterior](../07-simulacao-local/README.md) · [Índice do livro](../../../../README.md) · [Próximo →](../09-reproducao/README.md)
