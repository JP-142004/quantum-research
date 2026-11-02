# Experimento 3 · Montar o GHZ com menos passos melhora o resultado?

**Estado:** planejado, ainda não executado nesta versão. Resultado, Conclusão e Próximo passo serão escritos depois da primeira sessão.

**Onde e quando:** IBM, `ibm_fez` (confirmado na hora do envio), 3 sessões em 3 dias. Cada circuito é repetido 1.000 vezes.

## Pergunta

O computador só liga diretamente alguns pares de qubits. Quando o circuito pede uma porta entre dois qubits que não são vizinhos, o compilador acrescenta trocas de lugar (SWAP) e portas extras, e cada porta de dois qubits tem chance de erro ([ruído](../../fundamentos/ruido.md)). Dá para montar o mesmo GHZ seguindo as ligações do computador, sem passos extras, e isso melhora o resultado? ([construção](../../fundamentos/tecnicas/construcao.md))

## Como será feito

- **Circuitos:** o GHZ **original** (o qubit de menor número liga a todos) e o **conectado** (árvore que segue as ligações, a partir do qubit 2), nos **mesmos qubits**, no mesmo job.
- **Tamanhos:** 5, 10 e 20 qubits. Com 5, os qubits 0 a 4.
- **Medidas:** em Z (indicador PZ) e em X (indicador CX), sem correção de leitura ([indicadores](../../fundamentos/circuitos/ghz.md)).
- **Compilação:** a conectada é compilada **sem trocas de qubits**. Se o compilador precisar trocar algum, o envio é recusado.
- **Custo:** 3 tamanhos × 2 construções × 2 bases = 12 circuitos × 1.000 = 12.000 medidas por sessão, 36.000 nas 3 sessões.
- **Critério (proposta, definida antes de rodar):** a conectada só conta como melhor se a diferença tiver o **mesmo sinal nas 3 sessões**, em cada tamanho. Caso contrário, o resultado é "inconclusivo". Cada sessão aparece separada.

## Arquivos

| Arquivo | Para que serve |
| --- | --- |
| `experimento.py` | A receita. |
| `dados/AAAA-MM-DD_computador/` | Uma pasta por sessão. **Não se edita.** *(ainda não existem)* |
| `resultados/` | Tabelas e figuras geradas dos dados. *(ainda não existem)* |

**Execução:** `python rodar.py 03 --enviar` **envia jobs à IBM**, depois de você digitar a confirmação.

[Experimentos](../README.md)
