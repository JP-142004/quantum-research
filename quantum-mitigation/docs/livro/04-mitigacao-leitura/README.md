# 04. Ruído e mitigação de leitura

[← Anterior](../03-circuitos-medidas/README.md) · [Índice do livro](../../../README.md) · [Próximo →](../05-experimentos-reais/README.md)

## Onde aparecem os desvios

Erros podem surgir na preparação, nas portas, durante a espera e na leitura. Também existe flutuação estatística por usar um número finito de shots. Mitigação de leitura trata um modelo específico dessa cadeia; não substitui correção quântica de erros, nem reconstrói automaticamente toda a dinâmica que ocorreu antes da medida.

No modelo clássico de leitura, uma sequência verdadeira $j$ pode ser registrada como $i$. Definimos $A_{ij}=P(i\mid j)$, com resultados observados nas linhas e estados preparados nas colunas. Cada coluna soma 1. Essa matriz de atribuição é apresentada no [tutorial de mitigação de leitura da IBM](https://quantum.cloud.ibm.com/docs/en/tutorials/readout-error-mitigation-sampler). O projeto usa a inversão completa para cinco qubits; não usa o algoritmo M3 do tutorial.

## Exemplo de um qubit

Suponha P(1|0) = 0,10 e P(0|1) = 0,20:

$$A=\begin{pmatrix}0,90&0,20\\0,10&0,80\end{pmatrix}.$$

Se a distribuição anterior à leitura for $q=(0,5;0,5)$, a distribuição observada será $p=Aq=(0,55;0,45)$. Resolver $Aq=p$ recupera 0,5 e 0,5 nesse exemplo exato. Com contagens finitas, tanto A quanto p são estimados e a resposta tem incerteza.

## Como fazemos em cinco qubits

1. Preparamos cada uma das 32 sequências possíveis.
2. Medimos 1.000 shots por sequência.
3. Dividimos as contagens de cada preparação pelo total e montamos a coluna correspondente de A.
4. Medimos o GHZ em Z e X e construímos as distribuições observadas.
5. Resolvemos os sistemas lineares com `numpy.linalg.solve`.
6. Calculamos PZ e CX com as distribuições ajustadas.

A matriz tem dimensão 32 × 32. O custo completo cresce como $2^n$ preparações e $4^n$ entradas; não se deve aplicar essa construção diretamente a cinquenta qubits.

## Matriz completa e modelo independente

Nos dados reais, a matriz completa estimada pode representar padrões conjuntos de confusão; não impomos que o erro seja independente em cada qubit. Na simulação, geramos propositalmente um canal independente por qubit para conhecer a resposta de referência. Mesmo nesse caso, o estimador continua usando uma matriz completa obtida de contagens finitas.

A API `ReadoutError` do Aer recebe, no exemplo de um qubit, probabilidades condicionadas por **linha**. A matriz A usada na inversão está condicionada por **coluna**. O código trata essas convenções explicitamente; um teste determinístico assimétrico verifica que a orientação não foi invertida. Ver a [referência de ReadoutError](https://qiskit.github.io/qiskit-aer/stubs/qiskit_aer.noise.ReadoutError.html).

## Quasiprobabilidades e estabilidade

Ao inverter uma matriz estimada de uma amostra finita, algumas componentes de q podem ficar negativas. Isso não significa que o detector observou uma frequência negativa. É uma propriedade do estimador linear. O projeto preserva esses valores e informa o menor valor em cada base. Recortar negativos e renormalizar produziria outro estimador, com outro viés.

O número de condição avalia a sensibilidade numérica da inversão. Nas três rodadas reais ele fica perto de 1,2. O código interrompe análises quando a condição excede 100 em caminhos que usam essa verificação; esse é um critério operacional, não uma prova da validade física do modelo. Normalização, resíduo da solução e condição respondem a perguntas diferentes.

## O que a correção não resolve

Se as portas já degradaram o estado antes da leitura, recuperar a distribuição anterior à leitura não recupera o estado ideal. Além disso, preparar as 32 calibrações exige inicialização e portas X. Seus erros podem ser absorvidos pela matriz estimada. Uma calibração antiga pode não descrever a leitura de outro momento.

Por isso, apresentamos os resultados brutos junto com os ajustados, os diagnósticos e a incerteza. O [capítulo de estatística](../06-estatistica/README.md) mostra como essa incerteza é propagada.

---

[← Anterior](../03-circuitos-medidas/README.md) · [Índice do livro](../../../README.md) · [Próximo →](../05-experimentos-reais/README.md)
