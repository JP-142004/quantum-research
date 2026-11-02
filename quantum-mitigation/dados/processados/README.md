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
