# Experimento N · Título como uma pergunta

> Copie esta pasta para `NN_nome_curto` e apague as instruções entre colchetes. Escreva para quem não conhece os termos: explique ou aponte para [fundamentos](../../fundamentos/README.md).

**Onde e quando:** [IBM ou simulador]; computador; dias das sessões; **shots por circuito:** [preencher].

## Resposta curta

[Duas frases com a resposta. Escreva por último.]

## Pergunta

[O que queremos descobrir? Qual resultado anterior levou a esta pergunta? Qual fonte de ruído está em questão ([ruído](../../fundamentos/ruido.md))?]

## Como foi feito

- **Circuito e tamanhos:** [qual, com que qubits; veja `fundamentos/circuitos/`]
- **Resultado ideal e indicador:** [fórmula e valor ideal; veja [indicadores](../../fundamentos/indicadores.md)]
- **Técnica avaliada:** [qual; veja `fundamentos/tecnicas/`]
- **Referência e controle:** [com o que comparamos, e que controle de resposta conhecida detecta falhas]
- **Custo:** [circuitos × shots = medidas; portas de dois qubits]
- **Critério de sucesso, definido antes de executar:** [o que contará como melhora]

## Resultado

[Uma conta real, do dado bruto ao indicador, com os números intermediários. Tabelas e figuras vêm de `resultados/`, geradas dos dados. Legenda curta que diz o que cada ponto ou barra mostra. Cada sessão separada.]

## Conclusão

[O que dá para afirmar. O que os dados não mostram. Limites: computador, dias, número de sessões, hipóteses do modelo.]

## Próximo passo

[A pergunta que esta conclusão deixa em aberto, com link para o experimento seguinte.]

## Arquivos

| Arquivo | Para que serve |
| --- | --- |
| `experimento.py` | A receita: circuito, tamanhos, técnicas, onde roda e quantas sessões. |
| `dados/AAAA-MM-DD_computador/` | Uma pasta por sessão: ficha, contagens e circuitos. **Não se edita.** |
| `resultados/` | Tabelas e figuras geradas dos dados. Podem ser refeitas. |

**Execução:** [diga se o experimento envia jobs à IBM.]

[Experimentos](../README.md)
