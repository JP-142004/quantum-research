# Piloto local de extrapolação a ruído zero

[Percurso da pesquisa](../../../README.md) · [Dados da execução](../validacao_2026_11_01/relatorio.md)

Depois de ajustar a leitura, ainda vemos o efeito das portas. Neste piloto ampliamos a preparação com pares de operações inversas. Em condições ideais, cada par se cancela. No simulador ruidoso, as portas extras aumentam a exposição ao canal despolarizante escolhido. Os fatores 1, 3 e 5 correspondem a 4, 12 e 20 portas CX após compilação. A mudança de base e a medição ficam fora do dobramento.

![Referências do simulador em três fatores e interceptos lineares](../../../figuras/zne_fatores.png)

Os pontos dos fatores 1, 3 e 5 são referências sem flutuação de shots, após descontar a leitura. A linha é a reta ajustada aos três pontos. O símbolo no fator zero representa o valor previsto por essa reta. Para PZ, o intercepto é (13 × 0,946261 + 4 × 0,848950 − 5 × 0,763687)/12 ≈ **0,9899**. Para a correlação X, a mesma conta com 0,922368, 0,784717 e 0,667608 dá **0,9826**. Ambos ficam mais próximos do ideal, 1. A diferença que resta mostra a limitação de aproximar a resposta por uma reta.

Com 1.000 shots por circuito, há flutuação adicional. Por exemplo, no primeiro bloco o PZ estimado no fator 1 foi 0,9639 ± 0,0188, e a extrapolação deu 1,0072 ± 0,0226. O ajuste estatístico pode ultrapassar 1. Os 42 circuitos por bloco incluem calibração, seis circuitos GHZ e quatro controles. Em três blocos, são **126.000 shots locais**. Os fatores indicam quantas operações inserimos; sua relação com o ruído em um equipamento físico ainda precisaria ser medida.

[Implementação do dobramento e do intercepto](../../../scripts/protocolo_local.py) · [Referências numéricas e sementes](../validacao_2026_11_01/manifesto.json) · [Resultados do primeiro bloco](../validacao_2026_11_01/zne_leitura_e_portas_bloco_01_analise.json)
