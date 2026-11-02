# Dados: origem antes de interpretação

[Índice do livro](../README.md) · [Dicionário dos arquivos](../docs/livro/10-codigo-dados/README.md)

Imagine procurar o número 0,9648 da terceira rodada. Comece nos dados **brutos** para ver as 454 e 441 medidas dos dois extremos. Passe aos **processados** para ver o ajuste calculado a partir delas. Abra os **simulados** quando quiser saber o que o método recupera em um teste com resposta conhecida. Assim você consegue seguir a origem de um número sem abrir todos os JSONs.

| Pasta | Origem e uso |
| --- | --- |
| [brutos](brutos/README.md) | Contagens experimentais reais preservadas e metadados disponíveis |
| [processados](processados/README.md) | Tabelas e análises derivadas dos registros reais |
| [simulados](simulados/README.md) | Contagens e análises geradas no PC com modelos definidos |

Os 102.000 shots das três rodadas reais e os 486.000 shots simulados são conjuntos diferentes. Não os agregue em uma única amostra experimental. A série histórica de escala e a linha de base da modelagem também têm seus próprios registros.

Frequências brutas são inteiros não negativos. Indicadores ajustados são estimativas e podem sair do intervalo físico; consulte os erros e o método. Para rastrear uma figura, siga o JSON processado até seu arquivo bruto e job ou manifesto.
