# Experimento 2 · O computador acerta o que é fácil?

**Estado:** planejado, ainda não executado nesta versão. Resultado, Conclusão e Próximo passo serão escritos depois da primeira sessão.

**Onde e quando:** IBM, `ibm_fez` (confirmado na hora do envio), 3 sessões em 3 dias. Cada circuito é repetido 1.000 vezes.

## Pergunta

Se eu peço ao computador um resultado que já conheço, ele devolve esse resultado? Por exemplo: "deixe os 5 qubits em 0 e me diga o que você vê". A resposta certa é `00000`, sempre. Um pedido assim, com resposta conhecida, é um **controle**. Aqui não há GHZ: só pedir e ler.

O teste mistura dois passos, **preparar** o qubit e **ler** o resultado, e não diz qual dos dois falhou.

## Como será feito

12 circuitos:

| Pedido | Circuitos |
| --- | --- |
| Cinco qubits em 0 | `00000`, nos qubits 0 a 4. |
| Cinco qubits em 1 | `11111` (porta X nos cinco), nos qubits 0 a 4. |
| Um qubit por vez | Cada qubit de 0 a 4, sozinho, pedido em 0 e em 1 (10 circuitos). |

- **Indicador:** quantas vezes, em 1.000, o computador respondeu o que pedimos.
- **Custo:** 12 circuitos × 1.000 = 12.000 medidas por sessão, 36.000 nas 3 sessões.
- **Critério:** não há hipótese a testar. Mostramos cada sessão separada, para ver se um qubit muda de um dia para o outro. Não atribuímos causa que os dados não mostram.

## Arquivos

| Arquivo | Para que serve |
| --- | --- |
| `experimento.py` | A receita. |
| `dados/AAAA-MM-DD_computador/` | Uma pasta por sessão. **Não se edita.** *(ainda não existem)* |
| `resultados/` | Tabelas e figuras geradas dos dados. *(ainda não existem)* |

**Execução:** `python rodar.py 02 --enviar` **envia jobs à IBM**, depois de você digitar a confirmação.

[Experimentos](../README.md)
