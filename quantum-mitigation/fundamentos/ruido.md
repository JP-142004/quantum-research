# Fontes de ruído

Os termos básicos (qubit, porta, shot) estão em [conceitos.md](conceitos.md). Um computador quântico devolve sequências de bits. Cada sequência é um **shot**. Repetindo o circuito muitas vezes, contamos quantas vezes cada sequência apareceu. O **ruído** é tudo o que faz essas contagens diferirem das previstas para o circuito ideal.

## Exemplo

Preparamos `00000` e o equipamento devolve `00001`. Essa única sequência não diz onde o desvio surgiu. Há três possibilidades:

1. o qubit **já não começou em 0** (erro de preparação);
2. uma **operação** do circuito alterou o qubit (erro de porta ou decoerência);
3. o qubit estava em 0 e a **medição** registrou 1 (erro de leitura).

Técnicas diferentes atacam fontes diferentes. Por isso o projeto separa as fontes antes de comparar as técnicas.

## Fontes consideradas

| Fonte | Quando atua | Como se manifesta | Técnicas que a atacam |
| --- | --- | --- | --- |
| **Preparação** | Antes do circuito | Qubit inicia fora de `0`. | A calibração de leitura incorpora parte desse efeito. |
| **Portas** | Durante o circuito | Cada porta, sobretudo de dois qubits, altera ligeiramente o estado. Mais portas, mais desvio. | Circuito com menos portas, ZNE, PEC, twirling. |
| **Decoerência** | Enquanto o qubit espera ou opera | O estado se degrada com o tempo. Circuitos mais profundos sofrem mais. | Circuito mais curto, desacoplamento dinâmico. |
| **Leitura** | Na medição | O equipamento registra 0 como 1, ou 1 como 0, com certa probabilidade. | Calibração de leitura. |
| **Amostragem** | Na contagem | Com poucos shots, a fração observada flutua mesmo sem ruído no equipamento. | Mais shots; bootstrap para estimar a incerteza. |

A última linha não é ruído do equipamento. É uma incerteza estatística ([indicadores.md](indicadores.md) mostra a conta).

## Duas propriedades que importam para a escolha da técnica

**Ruído estocástico e ruído coerente.** O ruído estocástico se comporta como uma mistura de resultados errados. O coerente é uma rotação sistemática, que pode se somar de forma construtiva ao longo do circuito. Wallman e Emerson (2016) mostram que sortear portas de um qubit ao compilar converte ruído coerente em estocástico. Essa conversão é o *twirling*.

**Os parâmetros do equipamento mudam com o tempo.** Uma calibração feita em um dia pode não valer em outro. Por isso cada sessão de mitigação de leitura usa a calibração medida na própria sessão, e repetimos os experimentos em dias diferentes.

## O que um ajuste de leitura não resolve

Se uma porta já alterou o qubit para `1` e a leitura registrou `1` corretamente, a leitura não errou. Esse erro ocorreu antes, e corrigir a leitura não o desfaz. É por isso que o projeto simula cenários em que só a leitura tem erro e cenários em que leitura e portas têm erro (experimento 5).

[Fundamentos](README.md) · [Indicadores](indicadores.md)
