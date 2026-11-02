# Indicadores e incerteza

Um **indicador** é uma nota que diz quão perto do ideal está o resultado. Todo experimento define o seu indicador **antes** de executar.

## Indicadores gerais (valem para qualquer circuito)

| Indicador | Definição | Ideal |
| --- | --- | --- |
| **Probabilidade de sucesso** | Fração dos shots que caíram em resultados que o circuito ideal pode produzir. | 1 |
| **Distância até o ideal** | Metade da soma, sobre todas as sequências, de \|fração observada − fração ideal\|. | 0 |

*Exemplo (5 qubits, um GHZ medido em Z, de uma execução anterior do projeto).* O ideal é 50% `00000` e 50% `11111`. Foram observados 477 `00000`, 445 `11111` e 78 de outras sequências, em 1.000 shots.

- Probabilidade de sucesso = (477 + 445) / 1.000 = **0,922**.
- Distância até o ideal = ½ × (|0,477 − 0,5| + |0,445 − 0,5| + 0,078) = ½ × (0,023 + 0,055 + 0,078) = **0,078**.

## Indicadores específicos de um circuito

Cada circuito define os seus em `circuitos/<nome>.md`. O GHZ, por exemplo, tem **PZ** e **CX** ([circuitos/ghz.md](circuitos/ghz.md)). Para incluir um circuito novo, registre antes de executar:

1. o **resultado ideal** do circuito;
2. o **indicador** que mede o desvio, com sua fórmula e seu valor ideal;
3. como o indicador **distingue** o estado desejado de uma mistura clássica, se for o caso;
4. o custo em portas de dois qubits e em shots.

## Erro padrão só pela amostragem

Com n shots, o indicador flutua de uma execução para outra mesmo sem ruído extra. Para dois indicadores simples usamos as fórmulas:

- Uma fração p (probabilidade de sucesso, PZ): erro padrão = √(p (1 − p) / n). Com p = 0,895 e n = 1.000: √(0,895 × 0,105 / 1000) ≈ 0,0097.
- Uma correlação C (como o CX): erro padrão = √((1 − C²) / n). Com C = 0,806 e n = 1.000: √((1 − 0,650) / 1000) ≈ 0,0187.

Para saber se duas medidas diferem de verdade, divide-se a diferença pelo erro padrão da diferença (a raiz da soma dos quadrados dos dois erros padrão). Diferenças de poucos erros padrão podem ser só flutuação.

## Bootstrap: a incerteza quando há várias contas encadeadas

Quando o indicador sai de várias contas (como a calibração de leitura), a fórmula acima não basta. Usamos o *bootstrap*:

1. Pegamos as frequências observadas como se fossem a verdade.
2. Sorteamos novas contagens com essas frequências (amostragem multinomial). Na mitigação de leitura, sorteamos as contagens da calibração e as do circuito.
3. Refazemos toda a conta, inclusive o ajuste, e guardamos o indicador.
4. Repetimos 5.000 vezes.

O **erro padrão (EP)** é o desvio padrão dos 5.000 valores. O **intervalo de 95%** vai do percentil 2,5 ao 97,5.

Para o **ganho** (ajustado menos bruto) usamos, em cada réplica, as mesmas contagens do circuito para os dois valores. Assim a incerteza do ganho respeita o fato de que os dois vêm das mesmas medidas.

**Limite do método.** O bootstrap só contém a variação de amostragem dentro de uma sessão. Não inclui a mudança do equipamento entre dias nem erros sistemáticos desconhecidos. É por isso que repetimos os experimentos em sessões diferentes.

## Quasiprobabilidades

Inverter a matriz de calibração pode produzir componentes ligeiramente negativas ou indicadores acima de 1. Essas componentes são chamadas quasiprobabilidades. Não as recortamos, porque o recorte introduziria um viés. A menor componente negativa de cada sessão é registrada junto com os resultados.

[Fundamentos](README.md) · [Ruído](ruido.md) · [GHZ](circuitos/ghz.md)
