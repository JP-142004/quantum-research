# 02 — Controles com estados conhecidos

[Experimentos](../README.md) · [Circuitos e medidas](../../docs/livro/03-circuitos-medidas/README.md)

Os controles perguntam se já aparecem desvios quando não tentamos preparar um GHZ. Eles ajudam a formular hipóteses sobre preparação e leitura, mas não isolam perfeitamente as fontes de erro.

| Script | O que faz | Backend escrito no código |
| --- | --- | --- |
| [todos_zeros.py](todos_zeros.py) | Mede cinco qubits inicializados em zero, no layout 0–4 | `ibm_kingston` |
| [todos_uns.py](todos_uns.py) | Aplica X nos cinco qubits e mede, no layout 0–4 | `ibm_kingston` |
| [qubits_individuais.py](qubits_individuais.py) | Prepara 0 e 1 separadamente nos qubits físicos 0 e 1; quatro circuitos | `ibm_fez` |
| [comparar_zeros.py](comparar_zeros.py) | Compara qubit 0 sozinho, qubit 1 sozinho e cinco qubits juntos; três circuitos | `ibm_fez` |

Cada circuito usa 1.000 shots. Os scripts mostram contagens e frações que diferem do estado esperado. O teste de uns inclui portas X; o de zeros também depende de inicialização. Diferenças entre backend ou horário impedem atribuir uma mudança exclusivamente ao agrupamento dos qubits.

## Evidência disponível

Os programas foram preservados, mas não havia arquivos separados de contagens desses controles na pasta importada. Não reconstruímos resultados ausentes. Os controles do protocolo local novo possuem seus próprios dados em `dados/simulados`; eles não substituem essas medições históricas.

**Execução:** os quatro arquivos acessam a IBM e submetem circuitos. Para conhecer os controles novos sem hardware, leia o [capítulo de simulação](../../docs/livro/07-simulacao-local/README.md).
