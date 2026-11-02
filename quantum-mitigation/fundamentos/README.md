# Fundamentos

A teoria necessária para ler os experimentos, em ordem de leitura. Nenhum arquivo supõe conhecimento prévio.

| Ordem | Arquivo | O que explica |
| --- | --- | --- |
| 1 | [conceitos.md](conceitos.md) | Qubit, porta, circuito, shot, backend, simulador. |
| 2 | [ruido.md](ruido.md) | De onde vem a diferença entre o resultado ideal e o medido. |
| 3 | [indicadores.md](indicadores.md) | Como dar uma nota ao resultado, o erro padrão e o bootstrap, com as contas. |
| 4 | [circuitos/ghz.md](circuitos/ghz.md) | O circuito de referência (GHZ) e os indicadores PZ e CX. |
| 5 | [tecnicas/README.md](tecnicas/README.md) | As técnicas de mitigação: a ideia, a conta com números e os limites. |
| 6 | [referencias.md](referencias.md) | Os trabalhos em que cada técnica se apoia. |

## Regra desta pasta

Cada **circuito** do código (`mitigacao/circuitos/<nome>.py`) tem uma explicação em `circuitos/<nome>.md`. Cada **técnica** (`mitigacao/tecnicas/<nome>.py`) tem uma explicação em `tecnicas/<nome>.md`. Assim, quem lê o código sabe onde está a teoria, e quem lê a teoria sabe onde está o código.

Um arquivo que passa de cerca de 150 linhas é dividido.

[Visão geral](../README.md)
