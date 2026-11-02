# ZNE · extrapolação a ruído zero

Simulamos três versões do mesmo circuito com 4, 12 e 20 portas CX. No modelo, a população em Z caiu de **0,946** para **0,849** e **0,764** conforme aumentamos o número de portas.

![Pontos dos três circuitos simulados e previsão no fator zero](../../../figuras/zne_fatores.png)

Os pontos nos fatores 1, 3 e 5 correspondem aos três circuitos. O losango no fator zero é a previsão da reta. Para Z, essa previsão foi **0,990**, próxima do valor ideal 1.

[Relatório com os cálculos e as incertezas](../validacao_2026_11_01/relatorio.md)

## Resultados amostrados por bloco

| Bloco | PZ extrapolado | CX extrapolado |
| --- | --- | --- |
| [01](../validacao_2026_11_01/zne_leitura_e_portas_bloco_01_analise.json) | 1,0072 | 0,9532 |
| [02](../validacao_2026_11_01/zne_leitura_e_portas_bloco_02_analise.json) | 0,9135 | 1,0582 |
| [03](../validacao_2026_11_01/zne_leitura_e_portas_bloco_03_analise.json) | 1,0065 | 0,9283 |
