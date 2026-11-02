# Resultados derivados dos dados reais

[Dados](../README.md) · [Estatística e leitura dos resultados](../../docs/livro/06-estatistica/README.md)

| Arquivo | Abrangência | Gerador |
| --- | --- | --- |
| [resumo_escala.csv](resumo_escala.csv) | Dez tamanhos GHZ, zeros/uns/outros e PZ | `resumir_resultados.py` |
| [resumo_mitigacao.csv](resumo_mitigacao.csv) | Apenas os dois JSONs históricos; valores centrais e diagnósticos | `resumir_resultados.py` |
| [comparacao_rodadas.json](comparacao_rodadas.json) | As três rodadas, EP, ganhos, intervalos, sementes e hashes | `comparar_rodadas.py` |

O CSV histórico com duas rodadas não está quebrado nem é a comparação completa. Para as três, use o JSON e o [relatório consolidado](../../docs/comparacao_rodadas.md). Não altere o CSV para aparentar uma quarta rodada inexistente.

No JSON, `bruto` e `ajustado` são estimativas; `se_*` são erros padrão; `ic95_ganho_percentil` contém limites dos percentis bootstrap; `reducao_desvio_ideal` é uma proporção, não um percentual já multiplicado por 100. A unidade de PZ e CX é adimensional.

Esses arquivos podem ser sobrescritos pelos geradores. Para uma análise nova, registre o código e parâmetros usados e preserve os brutos. Consulte o [roteiro de reprodução](../../docs/livro/09-reproducao/README.md).

## Comparação antes e depois do ajuste

![Valores brutos e ajustados de PZ e CX nas três rodadas](../../figuras/comparacao_rodadas.png)

Em cada rodada no eixo horizontal, os dois pontos mostram o indicador bruto e o ajustado. A linha em 1 marca o valor ideal. Na rodada 3, PZ sobe de 0,895 para 0,9648. As barras mostram **um erro padrão** e o eixo vertical está ampliado. No painel X, leia o número como correlação, não como porcentagem de medidas corretas.

![Diferenças ajustado menos bruto por rodada e intervalos percentis de 95%](../../figuras/ganho_rodadas.png)

Aqui a referência é **zero**, que significa ausência de mudança após o ajuste. O ponto da rodada 3 para PZ vale 0,9648 − 0,895 ≈ 0,0698. A barra representa o intervalo de 95% para essa diferença, calculada usando a mesma amostra para bruto e ajustado. Esse é um intervalo diferente das barras do gráfico anterior. [Resultados que alimentam os dois gráficos](comparacao_rodadas.json)
