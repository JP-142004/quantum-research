# Circuito de referência: o estado GHZ

## O estado

Para cinco qubits, o estado GHZ ideal é

(|00000⟩ + |11111⟩) / √2.

Medido na base Z, ele produz apenas `00000` ou `11111`, cada um em cerca de metade dos shots. Escolhemos o GHZ como primeiro circuito de teste por duas razões: sua resposta ideal é conhecida em duas bases de medição, e seu tamanho pode crescer sem mudar a estrutura do circuito.

## Como se monta

H no qubit de origem e uma CX dele para cada outro qubit ([conceitos](../conceitos.md)). Há duas **variantes**, com o mesmo resultado ideal:

| Variante | Como liga os qubits | Efeito depois de compilar |
| --- | --- | --- |
| **original** | O qubit 0 manda para todos os outros. | Se o computador não liga o qubit 0 a todos, o compilador acrescenta trocas de lugar (SWAP) e portas extras. |
| **conectada** | Cada qubit passa para um vizinho, em árvore a partir de um qubit raiz, seguindo as ligações do computador. | Nenhuma porta extra. |

## Indicador em Z: PZ

**PZ** é a fração dos shots que deram todos zeros ou todos uns. Vale 1 no caso ideal, e é a probabilidade de sucesso deste circuito em Z.

PZ = (contagem de `00000` + contagem de `11111`) / total de shots.

*Exemplo (de uma execução anterior do projeto).* 454 shots deram `00000`, 441 deram `11111` e 105 deram outras sequências. PZ = (454 + 441) / 1.000 = **0,895**.

## Indicador em X: CX

PZ não basta. Uma mistura clássica, que sorteia `00000` ou `11111` sem coerência quântica, também teria PZ igual a 1. Para distinguir os dois casos, giramos cada qubit para a base X antes de medir.

Nessa base, o GHZ ideal só produz sequências com **número par** de bits 1. A **correlação em X**, **CX**, é

CX = (fração de sequências com número par de 1) − (fração com número ímpar).

Vale 1 no caso ideal. Uma mistura clássica daria 0.

*Exemplo (mesma execução).* 903 sequências pares e 97 ímpares. CX = (903 − 97) / 1.000 = **0,806**. Atenção: **0,806 não significa 80,6% de acertos.** É uma diferença entre duas frações.

## O que PZ e CX não dizem

Os dois indicadores verificam propriedades do GHZ, mas não determinam sua **fidelidade** completa. Um estado pode ter PZ e CX próximos de 1 e ainda diferir do GHZ em outras propriedades. Por isso os resultados são descritos como "aproximação dos indicadores do ideal", e não como "estado corrigido".

[Fundamentos](../README.md) · [Indicadores](../indicadores.md)
