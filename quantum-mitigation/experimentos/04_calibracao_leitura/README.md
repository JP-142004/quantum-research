# Experimento 4 · A calibração de leitura aproxima os indicadores do ideal?

**Estado:** planejado, ainda não executado nesta versão. Resultado, Conclusão e Próximo passo serão escritos depois da primeira sessão.

**Onde e quando:** IBM, `ibm_fez` (confirmado na hora do envio), 3 sessões em 3 dias, qubits 0 a 4. Cada circuito é repetido 1.000 vezes.

## Pergunta

Se medirmos como o equipamento registra estados conhecidos, podemos usar isso para estimar melhor PZ e CX do GHZ? A técnica está explicada, com um exemplo de um qubit, em [leitura](../../fundamentos/tecnicas/leitura.md).

## Como será feito

Cada sessão tem 38 circuitos de cinco qubits:

| Circuitos | O que são | Para quê |
| ---: | --- | --- |
| 32 | Cada sequência de `00000` a `11111`. | Montar a matriz de calibração A. |
| 2 | GHZ conectado, medido em Z e em X. | Calcular PZ e CX. |
| 4 | **Controles independentes** (amostras novas, não reaproveitam a calibração): `00000` e `11111` em Z, e os estados `+++++` e `++++-` em X, com resposta `00000` e `00001`. | Conferir se a correção acerta o que ela não viu. |

- **Custo:** 38 circuitos × 1.000 = 38.000 medidas por sessão, 114.000 nas 3 sessões.
- **Critério (proposta, definida antes de rodar):** a calibração só conta como "ajudou" se o valor **ajustado ficar mais perto de 1 que o bruto nas 3 sessões**, tanto em PZ quanto em CX, com o intervalo de 95% do ganho acima de zero. Os controles independentes decidem se a melhora vem mesmo da leitura: desvios persistentes, do mesmo sinal, em sessões diferentes, pedem investigação antes de atribuir a melhora à leitura.
- **Limites já conhecidos:** a calibração não corrige o erro das portas e também absorve parte do erro de preparação.

## Arquivos

| Arquivo | Para que serve |
| --- | --- |
| `experimento.py` | A receita. |
| `dados/AAAA-MM-DD_computador/` | Uma pasta por sessão. **Não se edita.** *(ainda não existem)* |
| `resultados/` | Tabelas e figuras geradas dos dados. *(ainda não existem)* |

**Execução:** `python rodar.py 04 --enviar` **envia jobs à IBM**, depois de você digitar a confirmação.

[Experimentos](../README.md)
