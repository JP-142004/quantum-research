# Experimento 8, parte B · Na IBM, em 10 e 20 qubits, a calibração por qubit leva os indicadores perto do ideal?

**Estado:** **só plano. Nada foi enviado à IBM.** O envio exige a aprovação do Luiz para aquele envio específico, depois de ele conferir o saldo de tempo do plano. Os critérios abaixo serão completados **antes** do envio, depois de ver o resultado da [parte A](../a_simulador/README.md).

## Resposta curta

*A escrever depois da execução.*

## Pergunta

Em 20 qubits a matriz completa de calibração não existe (seriam 2²⁰ calibrações). A calibração por qubit é o que cabe. Com ela, o GHZ conectado de 10 e de 20 qubits fica perto do ideal? E a hipótese de que cada qubit lê sem influência dos vizinhos aguenta?

## Como será feito (plano)

- **Computador:** `ibm_fez`, como nos experimentos 1 a 4. **3 sessões em dias diferentes**, como no 4.
- **Em cada sessão e para n = 10 e n = 20:** GHZ conectado em Z e em X; **4 calibrações**: `00…0`, `11…1`, `0101…` e `1010…`; 4 controles independentes (zeros e uns em Z; todos em `+` e todos em `+` com o qubit 0 em `−`, em X). 10 circuitos por tamanho, 20 por sessão, 20.000 medidas por sessão.
- **Por que 4 calibrações:** `00…0` e `11…1` dão a tabela 2 × 2 de cada qubit. `0101…` e `1010…` dão a tabela do mesmo qubit com os vizinhos em outro estado. Se a tabela mudar muito entre os dois grupos, a leitura de um qubit depende dos vizinhos, e a hipótese do modelo por qubit não vale.
- **Resultados que serão olhados:** (1) a tabela de cada qubit nos dois grupos de calibração, com a diferença e o intervalo de 95%; (2) PZ e CX do GHZ, observados e ajustados; (3) os controles depois do ajuste.
- **Limite já conhecido:** em 20 qubits não há a matriz completa como referência. A conferência é só pelos controles e pela comparação entre os dois grupos de calibração, que é mais fraca que a do experimento 7.
- **Antes de qualquer envio:** `python rodar.py 08b --verificar --online` para conferir que o GHZ, as calibrações e os controles de cada tamanho usam os **mesmos qubits físicos** e quantas portas de dois qubits cada circuito tem. A verificação local já confere que todos os circuitos dão o resultado ideal declarado.
- **Critérios de sucesso e margem:** *a definir antes do envio.*

## Resultado, Conclusão e Próximo passo

*Não há dados.*

## Arquivos

| Arquivo | Para que serve |
| --- | --- |
| `experimento.py` | A receita, pronta para `python rodar.py 08b --verificar` (local, não envia). |

**Execução:** IBM (`ibm_fez`). **Nada é enviado sem `--enviar` e sem a confirmação do Luiz.**

[Experimento 8](../README.md) · [Experimentos](../../README.md)
