# 02. Qubits, portas e o estado GHZ

[← Anterior](../01-visao-geral/README.md) · [Índice do livro](../../../README.md) · [Próximo →](../03-circuitos-medidas/README.md)

## Do bit ao qubit

Um bit clássico assume 0 ou 1. Um estado puro de um qubit pode ser escrito como

$$|\psi\rangle = \alpha|0\rangle + \beta|1\rangle,\qquad |\alpha|^2+|\beta|^2=1.$$

As amplitudes $\alpha$ e $\beta$ podem ser complexas. Ao medir na base Z, as probabilidades de 0 e 1 são seus módulos ao quadrado. O sinal e a fase relativa não aparecem diretamente nessas duas probabilidades, mas afetam medidas em outras bases. É por isso que uma superposição não pode ser reduzida a uma lista de probabilidades clássicas em uma única base.

Uma medição produz uma sequência de bits, não uma impressão das amplitudes. Para estimar probabilidades, repetimos a preparação e a medição. Cada repetição é um **shot**. Mil shots podem dar 493 zeros e 507 uns mesmo quando as probabilidades exatas são 50% e 50%.

## As portas usadas

| Porta | Ação relevante | Uso no projeto |
| --- | --- | --- |
| X | Troca $\lvert 0\rangle$ e $\lvert 1\rangle$ | Preparar estados de calibração |
| H, Hadamard | Leva $\lvert 0\rangle$ a $(\lvert 0\rangle+\lvert 1\rangle)/\sqrt2$ | Iniciar GHZ e mudar a base de medida |
| Z | Troca o sinal da componente $\lvert 1\rangle$ | Preparar o controle $\lvert −\rangle$ |
| CX, CNOT | Inverte o alvo se o controle é 1, atuando linearmente na superposição | Espalhar a correlação do GHZ |
| Medição | Produz um resultado clássico | Obter as contagens |

No GHZ de dois qubits, começamos com $|00\rangle$. Uma H no primeiro qubit cria uma superposição; uma CX entre ele e o segundo transforma os dois ramos em $|00\rangle$ e $|11\rangle$. O mesmo princípio se estende a mais qubits.

## O estado GHZ

Para $n$ qubits, o alvo é

$$|GHZ_+\rangle=\frac{|0\rangle^{\otimes n}+|1\rangle^{\otimes n}}{\sqrt2}.$$

Em cinco qubits, os únicos resultados ideais em Z são `00000` e `11111`, cada um com probabilidade 1/2. O estado é emaranhado: não pode ser escrito como produto de estados independentes de cada qubit. Isso não permite transmitir mensagens instantaneamente entre eles.

Compare duas preparações: uma superposição GHZ e uma mistura clássica que escolhe todos zeros ou todos uns ao acaso. Em Z, ambas têm a mesma distribuição. Em X, o GHZ positivo apresenta correlação coletiva igual a 1, enquanto essa mistura clássica apresenta correlação 0. Essa é a razão concreta para observar mais de uma base.

O projeto usa GHZ como circuito de referência. Uma apresentação mais ampla do estado e da caracterização por observáveis está no [tutorial da IBM sobre GHZ e tomografia](https://quantum.cloud.ibm.com/docs/en/tutorials/shadow-tomography). Não implementamos a tomografia desse tutorial.

## Estados puros, misturas e matriz densidade

Um vetor de estado representa estados puros. Para descrever misturas e canais de ruído de forma geral, usamos a matriz densidade $\rho$. Para um estado puro, $\rho=|\psi\rangle\langle\psi|$. As entradas diagonais dão probabilidades em Z; entradas fora da diagonal contêm informação de coerência nessa base.

Com cinco qubits, um vetor de estado tem 32 amplitudes e uma matriz densidade tem 32 × 32 entradas. Isso é pequeno para o PC usado. O tamanho cresce exponencialmente: não podemos extrapolar a facilidade dessa simulação para circuitos genéricos de cinquenta qubits.

## Fidelidade não é o mesmo que PZ

Para um alvo puro GHZ, a fidelidade é $F=\langle GHZ_+|\rho|GHZ_+\rangle$. Ela depende de populações e de coerências específicas. PZ e CX, que estudaremos no próximo capítulo, são indicadores úteis, mas não determinam a fidelidade completa de um estado arbitrário. A mistura clássica do exemplo tem PZ = 1, mas fidelidade 1/2 com o GHZ positivo.

**Exemplo para conferir:** se um aparelho escolhe `00000` ou `11111` com probabilidades iguais sem preparar coerência, PZ sozinho não distingue esse procedimento do GHZ ideal.

---

[← Anterior](../01-visao-geral/README.md) · [Índice do livro](../../../README.md) · [Próximo →](../03-circuitos-medidas/README.md)
