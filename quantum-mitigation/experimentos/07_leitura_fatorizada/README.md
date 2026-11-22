# Experimento 7 · Uma tabela por qubit substitui a matriz completa de leitura?

**Estado:** planejado. **Nenhum cálculo foi feito ainda.** Este arquivo registra as regras **antes** de olhar o resultado, como nos outros experimentos. As decisões marcadas com ⚠ precisam de aprovação do autor e dos orientadores.

**Onde e quando:** análise local, sem acesso à IBM. Usa as contagens já gravadas no [experimento 4](../04_calibracao_leitura/README.md) (`ibm_fez`, sessões de 8, 9 e 10 de novembro de 2026, 1.000 medidas por circuito). Não há dados novos.

## Resposta curta

*A escrever depois da análise.*

## Pergunta

No experimento 4, a calibração de leitura usou uma matriz de 32 × 32, medida com os 32 estados de `00000` a `11111` ([leitura](../../fundamentos/tecnicas/leitura.md)). Essa matriz não serve para muitos qubits: com 20 qubits seriam mais de um milhão de calibrações.

Um modelo mais simples usa uma tabela de 2 × 2 **por qubit** e supõe que um qubit não atrapalha a leitura do vizinho. **Quanto a simplificação do modelo e o custo da calibração alteram os valores ajustados de PZ e CX do GHZ?**

Esta pergunta não explica por que o PZ ajustado ficou em 0,953. Os três métodos usam preparações de calibração em comum e podem ter o mesmo viés. A origem desse resto continua sendo uma investigação separada.

## Como será feito

**Três métodos**, todos aplicados às mesmas contagens do GHZ conectado de 5 qubits (Z e X) de cada sessão:

| Método | Tabelas | Calibrações usadas | O que testa |
| --- | --- | --- | --- |
| Completo | 1 de 32 × 32 | as 32 | A referência (o que o experimento 4 já fez) |
| Fatorizado (a) | 5 de 2 × 2, com as marginais das 32 calibrações | as 32 | Só a simplificação do modelo |
| Fatorizado (b) | 5 de 2 × 2, com só `00000` e `11111` | 2 | A simplificação mais o corte de custo |

**Comparações.** Principais: (a) contra o completo, que isola o efeito da simplificação do modelo (mesmos dados de calibração), e (b) contra o completo, que avalia o pacote "modelo simplificado + calibração barata". Secundária: (a) contra (b), que mostra a sensibilidade à quantidade de dados: em (a), cada condição de um qubit reúne 16.000 medidas (16 estados × 1.000), e em (b), 1.000. Em (b), o contexto dos outros qubits é sempre "todos em 0" ou "todos em 1", e isso pode não representar bem o GHZ se a resposta de um qubit depender dos vizinhos. Por isso (b) é apresentado como teste de redução de custo, com a diferença de precisão informada junto (a largura do intervalo em cada método).

- **Indicadores:** PZ (base Z) e CX (base X) do GHZ conectado, cada sessão separada ([indicadores](../../fundamentos/indicadores.md)).
- **Incerteza:** bootstrap compartilhado. Em cada réplica, a calibração e o GHZ são reamostrados **uma vez** e a mesma réplica entra nos três ajustes. Assim a diferença entre métodos tem a incerteza certa, e não a soma das incertezas separadas.
- **Valores negativos:** os ajustados podem passar de 1 ou ficar abaixo de 0 em alguma probabilidade (quasiprobabilidades). Não recortamos nem renormalizamos, como no experimento 4. Registramos a menor quasiprobabilidade e o condicionamento de cada matriz. Réplicas que falharem são contadas e informadas, nunca descartadas em silêncio.
- **Ordem dos bits:** a conversão entre qubit físico e bit da resposta usa `leitura.permutacao`, como no experimento 4. Em 5 qubits, aplicar as 5 tabelas uma a uma deve dar o mesmo que o produto explícito das 5 (teste automático).
- **Custo:** nenhuma medida nova na IBM.

### Verificações além do PZ e do CX

PZ e CX resumem muita coisa em dois números, e dois modelos podem coincidir neles sem serem equivalentes.

1. **Previsão da calibração.** As 1.000 medidas de cada circuito de calibração são divididas ao acaso em duas metades (semente fixa, escolhida antes de calcular). Cada método é montado com a primeira metade e avaliado na segunda: compara-se a distribuição que ele prevê, para cada um dos 32 estados, com a medida. A métrica é a distância de variação total média, fixada agora.
2. **Controles independentes.** Os 4 controles do experimento 4 (`00000` e `11111` em Z; `+++++` e `++++-` em X) seguem como avaliação separada.

### Critério de equivalência, definido antes de calcular

Para cada sessão e cada indicador, olhamos a diferença **fatorizado menos completo**, com o intervalo de 95% do bootstrap compartilhado.

| Resultado | Quando |
| --- | --- |
| **Equivalente** | O intervalo de 95% inteiro está dentro da margem. |
| **Diferente** | O intervalo de 95% inteiro está fora da margem, de um lado só. |
| **Inconclusivo** | O intervalo cruza a margem. |

- ⚠ **Margem proposta: ±0,02** para PZ e para CX. Falta a justificativa científica: por que 0,02 preserva as conclusões do projeto? Para comparação, o resíduo do PZ ajustado é de cerca de 0,047 (1 − 0,953), então 0,02 é cerca de 43% dele. Pode ser melhor usar margens diferentes em PZ e CX.
- Este critério (intervalo de 95% dentro da margem) é mais exigente que o TOST de 90%, e não deve ser chamado de TOST sem especificar o procedimento.
- Cada sessão aparece separada. A conclusão geral só vale se o resultado for o mesmo nas 3.

## Resultado

*Tabelas geradas dos dados, a preencher depois da análise.*

<!-- TABELA:metodos -->
*Por sessão: observado, ajustado completo, ajustado (a) e ajustado (b), com incerteza.*
<!-- /TABELA:metodos -->

<!-- TABELA:diferencas -->
*Diferença em relação ao completo, intervalo de 95%, decisão, condicionamento e menor quasiprobabilidade.*
<!-- /TABELA:diferencas -->

## Conclusão

*A escrever depois da análise. O que cada resultado permitirá dizer:*

- **Equivalente:** "Nestas 3 sessões e dentro da margem, trocar a matriz completa pelo modelo fatorizado não alterou materialmente PZ e CX ajustados."
- **Diferente:** "Os indicadores são sensíveis ao modelo ou ao protocolo de calibração." Dizer que a causa é correlação de leitura entre qubits exigiria examinar os padrões conjuntos das contagens.
- **Inconclusivo:** dizer que estes dados não permitem decidir.

**Limites já conhecidos.**
- Um computador e três dias seguidos.
- O modelo fatorizado supõe independência entre qubits. Concordar com o completo em 5 qubits não prova que vale em tamanhos maiores.
- Os métodos compartilham as preparações de calibração. Concordância entre eles não elimina um viés comum, por exemplo de erros de preparação absorvidos na calibração.
- Os quatro controles cobrem poucos estados e não validam todas as distribuições.

## Próximo passo

*Depende do resultado. Se os modelos forem equivalentes, a análise com um modelo por qubit abre caminho para tamanhos maiores. A investigação da origem do resíduo de 0,953 é uma pergunta separada.*

## Arquivos

| Arquivo | Para que serve |
| --- | --- |
| `analisar.py` | O programa que lê as contagens do experimento 4 e compara os três métodos. *(a escrever)* |
| `resultados/` | Tabelas, `resultados.json` e figura, geradas dos dados. Podem ser refeitas. *(a gerar)* |

Este experimento **não tem pasta `dados/` própria** e não envia nada à IBM: lê `../04_calibracao_leitura/dados/`, que não se edita.

[Experimentos](../README.md)
