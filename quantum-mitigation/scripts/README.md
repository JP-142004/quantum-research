# Scripts

Programas de análise, validação e geração de tabelas e figuras. Todos rodam no PC, **exceto `recuperar_job.py`**, que consulta a IBM (sem enviar nenhum job novo). Os programas que enviam circuitos à IBM estão nas pastas dos [experimentos](../experimentos/README.md), não aqui.

[Visão geral](../README.md)

## Análise dos dados reais

| Script | O que faz | Lê | Grava |
| --- | --- | --- | --- |
| `resumir_resultados.py` | Calcula PZ de cada tamanho do experimento 1 e o resumo das duas primeiras rodadas. | Texto de escala e dois JSONs históricos | `resumo_escala.csv`, `resumo_mitigacao.csv` |
| `comparar_rodadas.py` | Ajuste de leitura, bootstrap e comparação das três rodadas do experimento 4. | Três JSONs das rodadas | JSON comparativo, `docs/comparacao_rodadas.md` e figuras 04 |

## Simulação e validação (experimentos 5 e 6)

| Script | O que faz |
| --- | --- |
| `protocolo_local.py` | Biblioteca: define circuitos, ruído e cálculos. Não inicia nada ao ser importada. |
| `validar_protocolo_local.py` | Executa os blocos simulados e salva contagens, análises e circuitos. Exige `--execucao` com um nome novo; recusa uma pasta já existente. |
| `verificar_registro_local.py` | Audita uma execução concluída: hashes, totais de shots, QPY e coerência com o modelo exato. Grava `verificacao.json`. |

## Tabelas, figuras e links

| Script | O que faz |
| --- | --- |
| `gerar_tabelas.py` | Preenche as tabelas marcadas com `TABELA:nome` nos READMEs, a partir dos dados. Com `--verificar`, só confere. |
| `visualizar_dados.py` | Recria as figuras 02, 03, 05 e 06 em [figuras](../figuras/README.md) a partir dos JSONs. |
| `verificar_links.py` | Confere os links relativos e as âncoras dos arquivos Markdown. |
| `recuperar_job.py` | Histórico: consulta o job `dbaa20fi0auc7391ncu0` e imprime as contagens. **Acessa a IBM** (também ao ser importado); não é usado pelos testes. |

## Como rodar

```powershell
python scripts/gerar_tabelas.py
python scripts/verificar_links.py
```

Use [requirements-analise.txt](../requirements-analise.txt) para análise e gráficos e [requirements-simulacao.txt](../requirements-simulacao.txt) para a simulação e os testes. O [requirements.txt](../requirements.txt) é a lista histórica que inclui o Runtime da IBM; não é necessário para os programas locais. `comparar_rodadas.py` aceita `--base` e `--bootstrap` (mínimo e padrão: 5.000).

## Preservação dos dados

Relatórios e tabelas derivados podem ser refeitos. O executor local recusa uma pasta já existente e, se falhar no meio, conserva os arquivos parciais; o auditor exige o estado `concluida`. Não renomeie nem complete à mão um manifesto incompleto para tratá-lo como válido.

**Quebras de linha e o auditor.** Os hashes do manifesto foram calculados com quebras de linha CRLF. Em uma cópia com LF (Linux, macOS ou checkout sem conversão), `verificar_registro_local.py` acusa "Arquivo alterado" apesar de o conteúdo ser o mesmo: os 26 hashes conferem quando as quebras dos JSON são convertidas para CRLF. Não indica corrupção, e os hashes do manifesto não devem ser "corrigidos".
