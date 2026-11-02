# Scripts de análise e validação

[Índice do livro](../README.md) · [Comandos de reprodução](../docs/livro/09-reproducao/README.md) · [Funções e dados](../docs/livro/10-codigo-dados/README.md)

| Arquivo | Entrada | Saída/efeito | Acesso IBM |
| --- | --- | --- | --- |
| [resumir_resultados.py](resumir_resultados.py) | Texto GHZ de escala e dois JSONs históricos | Sobrescreve `resumo_escala.csv` e `resumo_mitigacao.csv` | Não |
| [comparar_rodadas.py](comparar_rodadas.py) | Três JSONs reais | Recria JSON comparativo, relatório e figuras PNG/SVG | Não |
| [protocolo_local.py](protocolo_local.py) | Parâmetros internos, circuitos e contagens | Biblioteca de construção, simulação exata e análise; não inicia lote ao importar | Não |
| [validar_protocolo_local.py](validar_protocolo_local.py) | Nome novo em `--execucao` | Cria diretório de resultados simulados, QPY, JSONs e relatório | Não |
| [verificar_registro_local.py](verificar_registro_local.py) | Caminho de execução concluída | Verifica dados e grava `verificacao.json` | Não |
| [recuperar_job.py](recuperar_job.py) | ID histórico fixo no código | Consulta `dbaa20fi0auc7391ncu0` e imprime contagens | Sim; não submete novo job |

## Parâmetros e ambientes

`comparar_rodadas.py` aceita `--base` para a pasta de mitigação e `--bootstrap`, com mínimo e padrão de 5.000. `validar_protocolo_local.py` exige `--execucao`; shots, blocos e bootstrap estão fixos no código atual. `verificar_registro_local.py` recebe um caminho posicional.

Use [requirements-analise.txt](../requirements-analise.txt) para comparação/gráficos e [requirements-simulacao.txt](../requirements-simulacao.txt) para Aer/testes. O [requirements.txt](../requirements.txt) é a lista histórica que inclui Runtime; não é necessário para os novos programas locais.

## Preservação

Relatórios e tabelas derivados podem ser recriados. O executor local recusa uma pasta já existente; se falhar no meio, conserva arquivos parciais e o estado inicial do manifesto. O auditor exige `concluida`. Não se deve renomear ou completar manualmente um manifesto incompleto para tratá-lo como execução válida.

O script de recuperação é histórico e acessa o serviço no corpo do arquivo, inclusive quando importado. Ele não é usado pelos testes locais. O ID nele não é o da rodada 3 de mitigação.
