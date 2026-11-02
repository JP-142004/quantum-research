# Experimento 1 · Como o erro cresce de 5 a 50 qubits?

**Estado:** planejado, ainda não executado nesta versão. Resultado, Conclusão e Próximo passo serão escritos depois da primeira sessão.

**Onde e quando:** IBM, `ibm_fez` (confirmado na hora do envio), 3 sessões em 3 dias. Cada circuito é repetido 1.000 vezes.

## Pergunta

Um GHZ ideal só produz `00…0` ou `11…1` ([GHZ](../../fundamentos/circuitos/ghz.md)). Que fração das medidas cai nesses dois resultados quando o número de qubits aumenta? É o ponto de partida: mede o erro **antes** de qualquer técnica de mitigação.

## Como será feito

- **Circuito:** GHZ original (H e uma CX do qubit de menor número para todos os outros), medido em Z.
- **Tamanhos:** de 5 a 50 qubits, de 5 em 5 (10 circuitos). Com 5 qubits, os qubits físicos 0 a 4, os mesmos dos outros experimentos. Com mais, a busca parte do qubit 2 e junta qubits vizinhos.
- **Indicador:** **PZ**, a fração das medidas que deram todos zeros ou todos uns. Vale 1 no caso ideal ([indicadores](../../fundamentos/indicadores.md)).
- **Custo:** 10 circuitos × 1.000 = 10.000 medidas por sessão, 30.000 nas 3 sessões.
- **Critério:** não há hipótese a testar. Mostramos o PZ de cada tamanho em cada sessão, lado a lado, com o erro padrão só pela amostragem.

## Arquivos

| Arquivo | Para que serve |
| --- | --- |
| `experimento.py` | A receita: circuito, tamanhos, computador e número de sessões. |
| `dados/AAAA-MM-DD_computador/` | Uma pasta por sessão, criada pelo envio. **Não se edita.** *(ainda não existem)* |
| `resultados/` | Tabelas e figuras geradas dos dados. *(ainda não existem)* |

**Execução:** `python rodar.py 01 --enviar` **envia jobs à IBM**, depois de você digitar a confirmação.

[Experimentos](../README.md)
