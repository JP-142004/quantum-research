# Circuito de referência e indicadores

## O estado GHZ

Para cinco qubits, o estado GHZ ideal é

(|00000⟩ + |11111⟩) / √2.

Medido na base Z, ele produz apenas `00000` ou `11111`, cada um em cerca de metade dos shots. Escolhemos o GHZ como primeiro circuito de teste por duas razões: sua resposta ideal é conhecida em duas bases de medição, e seu tamanho pode crescer sem mudar a estrutura do circuito. Outros circuitos serão incluídos depois. Para cada um será preciso definir o resultado ideal e o indicador de desempenho (ver o fim deste arquivo).

## Indicador em Z: PZ

**PZ** é a fração dos shots que deram todos zeros ou todos uns.

PZ = (contagem de `00000` + contagem de `11111`) / total de shots.

Valor ideal: 1.

*Exemplo real (rodada 3, IBM Fez):* 454 shots deram `00000`, 441 deram `11111` e 105 deram outras sequências. PZ = (454 + 441) / 1.000 = **0,895**.

## Indicador em X: CX

PZ não basta. Uma mistura clássica, que sorteia `00000` ou `11111` sem coerência quântica, também teria PZ igual a 1. Para distinguir os dois casos, giramos cada qubit para a base X antes de medir.

Nessa base, o GHZ ideal só produz sequências com **número par** de bits 1. A **correlação em X**, **CX**, é

CX = (fração de sequências com número par de 1) − (fração com número ímpar).

Valor ideal: 1. Uma mistura clássica daria 0.

*Exemplo real (rodada 3):* 903 sequências pares e 97 ímpares. CX = (903 − 97) / 1.000 = **0,806**. Atenção: **0,806 não significa 80,6% de acertos.** É uma diferença entre duas frações.

## O que PZ e CX não dizem

Os dois indicadores verificam propriedades do GHZ, mas não determinam sua **fidelidade** completa. Um estado pode ter PZ e CX próximos de 1 e ainda diferir do GHZ em outras propriedades. Por isso os resultados são descritos como "aproximação dos indicadores do ideal", e não como "estado corrigido".

## Valor bruto, ajustado e simulado

| Palavra | Significado |
| --- | --- |
| **Bruto** ou **observado** | Calculado direto das contagens que o equipamento devolveu. |
| **Ajustado** ou **estimado** | Calculado nas mesmas contagens, depois de aplicar uma técnica (por exemplo, a matriz de calibração). Não existe uma nova execução com mais acertos. |
| **Referência do modelo** | Valor exato calculado no simulador, sem flutuação de shots. Só existe quando nós escolhemos o ruído. |

## Incerteza: bootstrap

Com 1.000 shots, outra execução daria contagens ligeiramente diferentes. Para estimar quanto, usamos o *bootstrap*:

1. Pegamos as frequências observadas como se fossem a verdade.
2. Sorteamos novas contagens com essas frequências (amostragem multinomial). Na mitigação de leitura, sorteamos as contagens da calibração e as do GHZ.
3. Refazemos toda a conta, inclusive o ajuste, e guardamos o indicador.
4. Repetimos 5.000 vezes por rodada.

O **erro padrão (EP)** é o desvio padrão dos 5.000 valores. O **intervalo de 95%** vai do percentil 2,5 ao 97,5.

Para o **ganho** (ajustado menos bruto) usamos, em cada réplica, as mesmas contagens do GHZ para os dois valores. Assim a incerteza do ganho respeita o fato de que os dois vêm das mesmas medidas.

**Limite do método.** O bootstrap só contém a variação de amostragem dentro de uma rodada. Não inclui deriva do equipamento entre dias nem erros sistemáticos desconhecidos.

## Quasiprobabilidades

Inverter a matriz de calibração pode produzir componentes ligeiramente negativas ou indicadores acima de 1. Essas componentes são chamadas quasiprobabilidades. Não as recortamos, porque o recorte introduziria um viés. A menor componente negativa de cada rodada está registrada em [comparacao_rodadas.json](../dados/processados/comparacao_rodadas.json).

## Como incluir um circuito novo

Antes de executar, registre na pasta do experimento:

1. o **resultado ideal** do circuito;
2. o **indicador** que mede o desvio, com sua fórmula e seu valor ideal;
3. como o indicador **distingue** o estado desejado de uma mistura clássica, se for o caso;
4. o custo em portas de dois qubits e em shots.

[Fundamentos](README.md) · [Ruído](ruido.md) · [Técnicas](tecnicas.md)
