# Figuras das três rodadas reais

[Visão geral](../README.md) · [Relatório comparativo](../docs/comparacao_rodadas.md)

| Figura | O que mostra |
| --- | --- |
| [comparacao_rodadas.png](comparacao_rodadas.png) / [SVG](comparacao_rodadas.svg) | PZ/CX brutos e ajustados, barras de ±1 erro padrão, linha ideal em 1 |
| [ganho_rodadas.png](ganho_rodadas.png) / [SVG](ganho_rodadas.svg) | Ajustado − bruto, com intervalo percentil de 95% pareado |

As duas figuras são geradas por [comparar_rodadas.py](../scripts/comparar_rodadas.py) a partir dos três JSONs reais. PNG é conveniente para visualizar e inserir em slides; SVG preserva formas vetoriais para redimensionar.

O eixo vertical do gráfico de comparação é ampliado e não começa em zero; isso está indicado na figura. As barras dos dois gráficos têm significados diferentes. Uma legenda deve informar origem, indicador e definição da barra de erro. A aproximação ao ideal não deve ser apresentada como fidelidade completa ou eliminação dos erros físicos.

## Gráfico do piloto local

[zne_fatores.png](zne_fatores.png) mostra as referências exatas do modelo simulado nos fatores 1, 3 e 5 e os interceptos extrapolados no fator zero. Sua origem e a conta estão no [experimento 6](../experimentos/06_zne_simulado/README.md). As duas figuras anteriores usam resultados reais.
