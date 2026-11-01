# Mitigação de ruído em circuitos GHZ

Este diretório reúne os arquivos dos experimentos anteriores. A pergunta que orienta o trabalho é: quanto dos desvios observados pode ser reduzido pela construção do circuito e pelo ajuste dos resultados de leitura?

## Onde encontrar cada etapa

| Pasta em `experimentos/` | Objetivo |
| --- | --- |
| `01_ghz_escala/` | Observar os resultados do GHZ original de 5 a 50 qubits. |
| `02_controles/` | Medir estados conhecidos: todos zeros, todos uns e qubits separados ou juntos. |
| `03_ghz_conectado/` | Comparar o GHZ original com uma construção que segue as conexões físicas; medir nas bases Z e X. Inclui o código conectado de 50 qubits. |
| `04_mitigacao_leitura/` | Calibrar os 32 estados de cinco qubits e ajustar os indicadores do GHZ. |

`dados/brutos/` contém as contagens disponíveis. `dados/processados/` contém tabelas calculadas a partir delas. [O guia dos experimentos](docs/experimentos.md) explica a sequência e as métricas. [O registro da importação](docs/organizacao.md) documenta a origem dos arquivos e os ajustes realizados.

## Usar os scripts

No terminal, a partir da raiz do repositório:

```powershell
python -m pip install -r quantum-mitigation/requirements.txt
python quantum-mitigation/scripts/resumir_resultados.py
```

O segundo comando apenas analisa arquivos locais, sem acessar a IBM. Ele recria as tabelas em `dados/processados/`.

Os scripts em `experimentos/` enviam circuitos ao hardware quando executados. Antes de rodá-los, confira backend, qubits, shots e credenciais salvas na sua máquina. Alguns scripts históricos selecionam Kingston; outros selecionam Fez ou usam `least_busy`. Os nomes e a disponibilidade dos backends devem ser conferidos antes de uma nova rodada.

As versões usadas nas rodadas históricas não estavam registradas. As dependências estão listadas sem fixar versões; o código conserva `SamplerV2`, que apresentou aviso de descontinuação nas execuções anteriores. Esta organização não representa uma atualização da API.

Não coloque tokens no código ou no Git. Novas saídas dos scripts de mitigação e GHZ conectado de 50 qubits são gravadas em suas respectivas pastas de dados brutos.
