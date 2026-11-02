# Experimentos

Cada experimento tem uma pasta numerada e um README com a mesma estrutura: pergunta, método, dados, conta, resultado, limites e arquivos. A ordem é a ordem em que as perguntas surgiram.

| # | Experimento | Pergunta | Onde rodou | Situação |
| --- | --- | --- | --- | --- |
| 1 | [Escala do GHZ](01_ghz_escala/README.md) | Como o desvio cresce com o número de qubits? | IBM | Medido |
| 2 | [Controles](02_controles/README.md) | O desvio aparece já em estados simples? | IBM | Medido |
| 3 | [Construção do circuito](03_ghz_conectado/README.md) | Menos portas reduzem o desvio? | IBM | Medido |
| 4 | [Calibração de leitura](04_mitigacao_leitura/README.md) | Quanto a correção da leitura aproxima os indicadores do ideal? | IBM (Fez), 3 rodadas | Medido |
| 5 | [Validação simulada](05_validacao_simulada/README.md) | O que a calibração recupera quando conhecemos a causa do erro? | PC | Simulado |
| 6 | [ZNE simulada](06_zne_simulado/README.md) | A extrapolação a ruído zero reduz o erro das portas? | PC | Simulado |

Os resultados numéricos estão em [dados](../dados/README.md), separados em brutos (contagens da IBM), processados (indicadores calculados) e simulados. As técnicas estão listadas em [fundamentos/tecnicas.md](../fundamentos/tecnicas.md), com a situação de cada uma.

## Atenção ao executar

Os programas Python das pastas 1 a 4 **enviam jobs à IBM** quando executados. Para estudar os resultados não é necessário executá-los: os dados já estão salvos. Os comandos que apenas leem dados, sem acessar a IBM, estão em [scripts/README.md](../scripts/README.md).

## Como acrescentar um experimento

1. Copie a pasta [_modelo](_modelo/README.md) para a próxima numeração, por exemplo `07_nome_curto`.
2. Escreva pergunta, indicador, controle, custo em shots e critério de sucesso **antes** de executar.
3. Guarde contagens em `dados/brutos/07_nome_curto` ou `dados/simulados/`. Calcule os indicadores por script, nunca à mão.
4. Para tabelas, use os marcadores de [gerar_tabelas.py](../scripts/gerar_tabelas.py). Assim o número do texto sempre vem do dado.
5. Acrescente uma linha na tabela acima e em [tecnicas.md](../fundamentos/tecnicas.md), e uma linha em [dados/README.md](../dados/README.md) se houver um novo tipo de dado.

[Visão geral](../README.md)
