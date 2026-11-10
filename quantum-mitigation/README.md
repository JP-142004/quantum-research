# Mitigação de ruído em circuitos quânticos

Os computadores quânticos atuais cometem erros: o resultado de um circuito se afasta do resultado ideal por causa do **ruído**. Este projeto estuda **técnicas de mitigação**, que estimam o resultado correto sem consertar o equipamento, e mede quanto cada uma aproxima o resultado do ideal e a que custo.

É a frente de **mitigação** de uma pesquisa de iniciação científica (PIBIC). A frente de modelagem de ruído está em [quantum-modeling](../quantum-modeling/README.md).

## Estado atual

Esta é a **segunda versão**, reconstruída do zero para ser mais simples e para crescer. A primeira versão ficou guardada na marca `mitigation-antiga` do Git. Todos os seis experimentos **já foram executados e analisados**: os quatro da IBM (`ibm_fez`), em 3 sessões nos dias 8, 9 e 10 de novembro de 2026, e os dois de simulação.

O circuito de teste é o **estado GHZ**, porque sua resposta ideal é conhecida. Seguem-se seis experimentos, quatro em computadores da IBM e dois em simulação, com três técnicas: circuito com menos portas, calibração de leitura e extrapolação a ruído zero. Depois entram outras técnicas (twirling, desacoplamento dinâmico, PEC) e outros circuitos.

## Por onde começar

1. [fundamentos](fundamentos/README.md): a teoria, explicada do zero.
2. [experimentos](experimentos/README.md): o plano dos seis experimentos, na ordem em que as perguntas surgem.

## Pastas

| Pasta | Conteúdo |
| --- | --- |
| [fundamentos](fundamentos/README.md) | Conceitos, ruído, indicadores, o circuito GHZ, as técnicas (com as contas) e as referências. |
| [experimentos](experimentos/README.md) | Um experimento por pasta: relatório, receita, dados e resultados. |
| `mitigacao` | O código, escrito uma vez: `circuitos/`, `tecnicas/`, `execucao/` (simulador e IBM, com a mesma interface), indicadores, estatística e registro das sessões. |
| `rodar.py` | O único comando: `python rodar.py 03 --verificar`, `--enviar`, `--coletar`, `--listar` ou `--analisar`. |
| `tests` | Testes automáticos. Percorrem todos os circuitos registrados. |
| `requirements.txt` | As versões dos pacotes Python. |

## Como o repositório cresce

Cada coisa nova entra em **um lugar só**:

| Para acrescentar… | Você escreve… |
| --- | --- |
| um **circuito** | `mitigacao/circuitos/<nome>.py` (com a lista `EXEMPLOS`, que os testes percorrem sozinhos) e `fundamentos/circuitos/<nome>.md` |
| uma **técnica** | `mitigacao/tecnicas/<nome>.py` e `fundamentos/tecnicas/<nome>.md` |
| um **experimento** | uma pasta nova em `experimentos/`, copiada do molde |
| um **computador** | nada: é um parâmetro do envio |

## Aviso

Enviar circuitos à IBM gasta o tempo do plano de quem envia. Nenhum envio acontece sem decisão explícita do autor, com o orçamento de medidas combinado antes.
