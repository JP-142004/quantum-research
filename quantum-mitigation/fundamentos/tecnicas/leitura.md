# Calibração de leitura

**Ideia.** A leitura às vezes registra o bit errado. Se medirmos como o equipamento registra cada preparação conhecida, podemos desfazer essa distorção nas contagens do circuito que nos interessa.

## Exemplo com um qubit

Os números são ilustrativos, não são dados reais. Preparamos 0 e o leitor registra 0 em 90% das vezes. Preparamos 1 e o leitor registra 0 em 20% das vezes. Organizamos isso numa matriz **A**, em que cada coluna é uma preparação e cada linha, o que foi registrado:

| | preparado 0 | preparado 1 |
| --- | ---: | ---: |
| registrou 0 | 0,90 | 0,20 |
| registrou 1 | 0,10 | 0,80 |

No circuito, observamos **p** = (0,55 ; 0,45), ou seja, 55% de zeros. A estimativa corrigida **q** é a que, passada pela matriz, reproduz o observado: **A q = p**, ou seja, **q = A⁻¹ p**. O determinante de A é 0,90 × 0,80 − 0,20 × 0,10 = 0,70, e

q₀ = (0,80 × 0,55 − 0,20 × 0,45) / 0,70 = 0,35 / 0,70 = **0,50**, e q₁ = 0,50.

Conferência: 0,90 × 0,50 + 0,20 × 0,50 = 0,55. ✓

## Com cinco qubits

Há 2⁵ = 32 preparações possíveis (de `00000` a `11111`), então **A** é 32 × 32 e cada sessão tem 32 circuitos de calibração. A conta é a mesma: **q = A⁻¹ p**.

## O que acontece com mais qubits

Com n qubits são necessárias 2ⁿ calibrações, e a matriz cresce como 2ⁿ × 2ⁿ. Isso limita este modelo, chamado `completo`, a uns 10 qubits. O projeto prevê um segundo modelo, `fatorizado`, em que cada qubit tem a sua matriz 2 × 2 (o custo cresce com n, e não com 2ⁿ). Ele só vale se a leitura de um qubit não influencia a dos outros. Bravyi et al. (2021) descrevem modelos assim. **Ainda não está implementado.**

## Limites

- A calibração também absorve parte do erro de preparação, porque os estados de calibração são preparados por portas.
- Ela **não** desfaz o erro das portas do circuito.
- A inversão pode dar componentes ligeiramente negativas (quasiprobabilidades) e indicadores acima de 1; não as recortamos ([indicadores.md](../indicadores.md)).
- O erro padrão do resultado ajustado é maior que o do bruto.

[Técnicas](README.md)
