# Conceitos básicos

Tudo o que é preciso saber para acompanhar os experimentos, sem supor conhecimento prévio de computação quântica.

## Qubit, porta e circuito

- **Bit** é 0 ou 1. Um **qubit** também dá 0 ou 1 quando medido, mas antes da medida pode estar numa **superposição**: um estado que não é nem 0 nem 1, e que dá cada resultado com certa probabilidade.
- **Porta** é uma operação sobre qubits. Usamos três:
  - **X** troca 0 por 1.
  - **H** coloca um qubit que está em 0 numa superposição: ao medir, dá 0 ou 1 com 50% de chance cada.
  - **CX** age sobre dois qubits, o *controle* e o *alvo*: inverte o alvo se o controle for 1. É a porta que liga um qubit ao outro.
- **Circuito** é uma sequência de portas seguida de medida. A **profundidade** é o número de camadas de portas, uma medida aproximada do tempo que o circuito leva.

## Medir e repetir

Cada execução do circuito devolve uma sequência de bits, por exemplo `00101`, e o resultado é aleatório. Por isso o circuito é repetido muitas vezes. Cada repetição é um **shot**, e as **contagens** dizem quantas vezes cada sequência apareceu. Neste projeto usamos 1.000 shots por circuito.

Na sequência de bits, o bit da **direita** é o qubit 0.

## Bases de medição: Z e X

Medir **em Z** é a medida normal, que lê 0 ou 1. Medir **em X** significa aplicar H em cada qubit antes de medir. Algumas propriedades de um estado só aparecem em uma das bases, por isso medimos nas duas ([circuitos/ghz.md](circuitos/ghz.md) mostra um exemplo).

## O computador real

- **Backend** é o computador quântico escolhido, por exemplo `ibm_fez` ou `ibm_kingston`. **Job** é uma execução enviada ao serviço da IBM, com um identificador próprio.
- No processador, só alguns pares de qubits estão ligados fisicamente. A **compilação** adapta o circuito às portas e às ligações do equipamento e pode **inserir portas extras** para conectar qubits distantes. Por isso o circuito executado tem mais portas que o desenhado.
- Nos circuitos compilados para o Fez, a porta de dois qubits aparece com o nome `cz`: o CX do desenho vira CZ mais rotações. Nos textos, "porta de dois qubits" vale para as duas.
- Cada porta, sobretudo a de dois qubits, e cada medida têm uma pequena chance de erro. A soma desses erros é o **ruído** ([ruido.md](ruido.md)).

## Simulador

É um programa no PC que calcula o resultado do circuito. Como podemos **escolher o ruído**, sabemos a resposta certa e podemos testar se uma técnica a recupera. Os valores de uma simulação não valem para o equipamento real.

## As três palavras dos resultados

| Palavra | Significado |
| --- | --- |
| **Observado** (ou bruto) | Calculado direto das contagens que o equipamento devolveu. |
| **Ajustado** (ou estimado) | Calculado nas mesmas contagens, depois de aplicar uma técnica. Não houve uma nova execução com mais acertos. |
| **Simulado** | Vem de um simulador, com ruído escolhido por nós. |

[Fundamentos](README.md) · [Ruído](ruido.md)
