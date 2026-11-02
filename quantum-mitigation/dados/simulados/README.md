# Dados simulados

Resultados de simulações no PC (Qiskit Aer), com ruído sintético escolhido por nós. Como o ruído é conhecido, dá para comparar o que a técnica estima com o valor exato do modelo. Os valores **não** valem para o hardware da IBM.

[Dados](../README.md)

Existe uma única execução, `validacao_2026_11_01` (1º de novembro de 2026), e todos os arquivos ficam na mesma pasta porque o manifesto, o auditor e os scripts usam esses caminhos. Cada circuito foi simulado com 1.000 medidas.

## Achar um resultado

Cada **bloco** é uma repetição independente: tem sementes próprias e a sua própria calibração de leitura. Cada célula abre os dados (contagens) e os indicadores calculados (análise) daquele bloco.

| Cenário | Experimento | Bloco 1 | Bloco 2 | Bloco 3 |
| --- | --- | --- | --- | --- |
| Ideal (sem ruído) | [5](../../experimentos/05_validacao_simulada/README.md) | [contagens](validacao_2026_11_01/comparacao_ideal_bloco_01_contagens.json) · [análise](validacao_2026_11_01/comparacao_ideal_bloco_01_analise.json) | [contagens](validacao_2026_11_01/comparacao_ideal_bloco_02_contagens.json) · [análise](validacao_2026_11_01/comparacao_ideal_bloco_02_analise.json) | [contagens](validacao_2026_11_01/comparacao_ideal_bloco_03_contagens.json) · [análise](validacao_2026_11_01/comparacao_ideal_bloco_03_analise.json) |
| Só erro de leitura | [5](../../experimentos/05_validacao_simulada/README.md) | [contagens](validacao_2026_11_01/comparacao_leitura_bloco_01_contagens.json) · [análise](validacao_2026_11_01/comparacao_leitura_bloco_01_analise.json) | [contagens](validacao_2026_11_01/comparacao_leitura_bloco_02_contagens.json) · [análise](validacao_2026_11_01/comparacao_leitura_bloco_02_analise.json) | [contagens](validacao_2026_11_01/comparacao_leitura_bloco_03_contagens.json) · [análise](validacao_2026_11_01/comparacao_leitura_bloco_03_analise.json) |
| Leitura e portas | [5](../../experimentos/05_validacao_simulada/README.md) | [contagens](validacao_2026_11_01/comparacao_leitura_e_portas_bloco_01_contagens.json) · [análise](validacao_2026_11_01/comparacao_leitura_e_portas_bloco_01_analise.json) | [contagens](validacao_2026_11_01/comparacao_leitura_e_portas_bloco_02_contagens.json) · [análise](validacao_2026_11_01/comparacao_leitura_e_portas_bloco_02_analise.json) | [contagens](validacao_2026_11_01/comparacao_leitura_e_portas_bloco_03_contagens.json) · [análise](validacao_2026_11_01/comparacao_leitura_e_portas_bloco_03_analise.json) |
| ZNE (leitura e portas, fatores 1, 3 e 5) | [6](../../experimentos/06_zne_simulado/README.md) | [contagens](validacao_2026_11_01/zne_leitura_e_portas_bloco_01_contagens.json) · [análise](validacao_2026_11_01/zne_leitura_e_portas_bloco_01_analise.json) | [contagens](validacao_2026_11_01/zne_leitura_e_portas_bloco_02_contagens.json) · [análise](validacao_2026_11_01/zne_leitura_e_portas_bloco_02_analise.json) | [contagens](validacao_2026_11_01/zne_leitura_e_portas_bloco_03_contagens.json) · [análise](validacao_2026_11_01/zne_leitura_e_portas_bloco_03_analise.json) |

Figuras: [ideal](../../figuras/05_simulacao_ideal.png), [leitura](../../figuras/05_simulacao_leitura.png), [leitura e portas](../../figuras/05_simulacao_leitura_e_portas.png), [controles](../../figuras/05_controles_simulados.png) (experimento 5); [blocos de ZNE](../../figuras/06_zne_blocos.png) e [fatores](../../figuras/06_zne_fatores.png) (experimento 6).

## Como ler o nome de um arquivo

`comparacao_leitura_e_portas_bloco_02_analise.json` se divide em quatro partes:

| Parte | Significado |
| --- | --- |
| `comparacao` ou `zne` | Qual experimento: `comparacao` é o 5 (GHZ original contra conectado); `zne` é o 6. |
| `ideal`, `leitura`, `leitura_e_portas` | O cenário de ruído simulado. O ZNE só foi feito em `leitura_e_portas`. |
| `bloco_01` a `bloco_03` | A repetição. Cada bloco tem a sua calibração. |
| `_contagens` ou `_analise` | `_contagens`: quantas vezes cada sequência de bits apareceu em cada circuito. `_analise`: indicadores brutos e ajustados, erros padrão, ganhos e intervalos, calculados dessas contagens. |

Os quatro **controles** (todos zeros, todos uns, paridade positiva e negativa) não têm arquivo próprio: estão dentro de cada `_analise`. Um bloco de comparação tem 40 circuitos (32 de calibração, 4 GHZ e 4 controles) e um bloco de ZNE tem 42 (32 de calibração, 6 GHZ e 4 controles).

## Registro da execução

Estes cinco arquivos descrevem a execução inteira, não um bloco.

| Arquivo | O que tem |
| --- | --- |
| `manifesto.json` | Origem, modelo de ruído, sementes, versões, referências exatas do modelo e o hash de cada arquivo. |
| `verificacao.json` | Resultado da auditoria de integridade e consistência (`scripts/verificar_registro_local.py`). |
| `relatorio.md` | Todos os valores desta execução, em texto. |
| `comparacao.qpy` | 40 circuitos compilados da comparação, para o experimento 5. |
| `zne.qpy` | 42 circuitos compilados do ZNE, para o experimento 6. |

Pasta da execução: [validacao_2026_11_01](validacao_2026_11_01/relatorio.md).
