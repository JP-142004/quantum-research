# Dados simulados

Resultados de simulações no PC (Qiskit Aer), com ruído sintético escolhido por nós. Como o ruído é conhecido, dá para comparar o que a técnica estima com o valor exato do modelo. Os valores **não** valem para o hardware da IBM.

[Dados](../README.md)

Tudo da execução `validacao_2026_11_01` fica na mesma pasta, porque os scripts e a auditoria usam esses caminhos. Cada circuito foi simulado com 1.000 medidas.

| Arquivo | O que tem |
| --- | --- |
| `manifesto.json` | Origem, modelo de ruído, sementes, versões, referências exatas e hashes dos arquivos. |
| `verificacao.json` | Resultado da auditoria de integridade e consistência. |
| `relatorio.md` | Todos os valores desta execução. |
| `comparacao.qpy` | 40 circuitos compilados da comparação de construções. |
| `zne.qpy` | 42 circuitos compilados do ZNE. |
| `comparacao_<cenário>_bloco_<NN>_contagens.json` | Contagens de um bloco da comparação. Cenários: `ideal`, `leitura`, `leitura_e_portas`. Blocos: 01 a 03. |
| `comparacao_<cenário>_bloco_<NN>_analise.json` | Indicadores brutos e ajustados, ganhos e intervalos do mesmo bloco. |
| `zne_leitura_e_portas_bloco_<NN>_contagens.json` e `_analise.json` | O mesmo para os três blocos de ZNE (fatores 1, 3 e 5 e extrapolação). |

Os quatro controles (zeros, uns, paridade positiva e negativa) estão dentro dos arquivos `_analise.json` de cada bloco.

| Experimento | Arquivos | Figuras |
| --- | --- | --- |
| [5. Validação simulada](../../experimentos/05_validacao_simulada/README.md) | `comparacao_*` | [ideal](../../figuras/05_simulacao_ideal.png), [leitura](../../figuras/05_simulacao_leitura.png), [leitura e portas](../../figuras/05_simulacao_leitura_e_portas.png), [controles](../../figuras/05_controles_simulados.png) |
| [6. ZNE simulada](../../experimentos/06_zne_simulado/README.md) | `zne_*` | [blocos](../../figuras/06_zne_blocos.png), [fatores](../../figuras/06_zne_fatores.png) |
