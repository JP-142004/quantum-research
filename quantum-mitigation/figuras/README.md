# Figuras

Todas as imagens do repositório ficam aqui. O número no começo do nome é o do experimento a que a figura pertence. Cada figura aparece no relatório do respectivo experimento.

| Figura | Experimento | O que mostra | Origem |
| --- | --- | --- | --- |
| [01_escala_observada.png](01_escala_observada.png) | [1](../experimentos/01_ghz_escala/README.md) | Fração de medidas todas 0 ou todas 1 (PZ) para GHZ de 5 a 50 qubits. | CSV da série histórica. |
| [02_controles_reais.png](02_controles_reais.png) | [2](../experimentos/02_controles/README.md) | Acerto de cada controle (estado simples) em cada backend, em %. | JSON recuperado da IBM. |
| [03_construcoes_reais.png](03_construcoes_reais.png) | [3](../experimentos/03_ghz_conectado/README.md) | PZ e CX brutos das construções original e conectada. | JSON recuperado da IBM. |
| [04_contagens_rodada3.png](04_contagens_rodada3.png) | [4](../experimentos/04_mitigacao_leitura/README.md) | Contagens em Z da rodada 3. | Contagens da IBM. |
| [04_comparacao_rodadas.png](04_comparacao_rodadas.png) · [svg](04_comparacao_rodadas.svg) | [4](../experimentos/04_mitigacao_leitura/README.md) | PZ e CX brutos e ajustados nas três rodadas, com ±1 erro padrão. O eixo vertical não começa em zero. | `scripts/comparar_rodadas.py` |
| [04_ganho_rodadas.png](04_ganho_rodadas.png) · [svg](04_ganho_rodadas.svg) | [4](../experimentos/04_mitigacao_leitura/README.md) | Ajustado menos bruto em cada rodada, com intervalo de 95%. | `scripts/comparar_rodadas.py` |
| [05_simulacao_ideal.png](05_simulacao_ideal.png) | [5](../experimentos/05_validacao_simulada/README.md) | Indicadores dos três blocos simulados sem ruído. | `scripts/visualizar_dados.py` |
| [05_simulacao_leitura.png](05_simulacao_leitura.png) | [5](../experimentos/05_validacao_simulada/README.md) | Idem, com erro só na leitura. | `scripts/visualizar_dados.py` |
| [05_simulacao_leitura_e_portas.png](05_simulacao_leitura_e_portas.png) | [5](../experimentos/05_validacao_simulada/README.md) | Idem, com erro na leitura e nas portas. | `scripts/visualizar_dados.py` |
| [05_controles_simulados.png](05_controles_simulados.png) | [5](../experimentos/05_validacao_simulada/README.md) | Desvio dos quatro controles em relação ao alvo, nos doze blocos. | `scripts/visualizar_dados.py` |
| [06_zne_blocos.png](06_zne_blocos.png) | [6](../experimentos/06_zne_simulado/README.md) | Indicadores nos fatores 1, 3 e 5 e valor extrapolado, nos três blocos. | `scripts/visualizar_dados.py` |
| [06_zne_fatores.png](06_zne_fatores.png) | [6](../experimentos/06_zne_simulado/README.md) | Referência exata do modelo nos fatores 1, 3 e 5 e a reta extrapolada. | Cálculo exato do modelo. |

PNG serve para ler e inserir em slides; SVG é vetorial e redimensiona sem perder qualidade. As figuras 01 a 04 usam dados da IBM; 05 e 06 são simulação.

[Visão geral](../README.md)
