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

## Novas rodadas de mitigação

O script `experimentos/04_mitigacao_leitura/repetir_mitigacao.py` separa envio e coleta. A rodada 3 continua as duas rodadas históricas, mantendo Fez, qubits físicos 0 a 4, 1.000 shots e 34 circuitos por rodada. O objetivo é avaliar a repetibilidade da melhora nos indicadores Z e X.

```powershell
# Verificação ideal local, sem acesso à IBM:
python quantum-mitigation/experimentos/04_mitigacao_leitura/repetir_mitigacao.py --verificar
# Envia uma única rodada nova:
python quantum-mitigation/experimentos/04_mitigacao_leitura/repetir_mitigacao.py --rodada 3 --enviar
# Consulta o mesmo job e salva o resultado quando concluído:
python quantum-mitigation/experimentos/04_mitigacao_leitura/repetir_mitigacao.py --rodada 3 --coletar
```

Os IDs, versões, circuitos compilados em QPY, contagens e análise ficam em `dados/brutos/04_mitigacao_leitura/repeticoes/`. A análise calcula os mesmos indicadores e seus erros de amostragem por bootstrap. O embaralhamento usa uma semente diferente em cada rodada; isso não garante a ordem física das execuções. As opções de DD e twirling permanecem desativadas. Há um limite de execução de 120 segundos por job; esse limite não é uma estimativa do tempo de fila.

O envio recusa sobrescrever uma rodada registrada. A coleta consulta o estado e retorna sem bloquear enquanto o job não terminou. Cada rodada adicional deve usar outro número. O resumo histórico em CSV continua restrito aos dois JSONs originais.

## Comparação consolidada das três rodadas

A análise offline das três execuções concluídas está disponível em:

- [Comparação, incertezas e diagnósticos](docs/comparacao_rodadas.md).
- [Resumo para o orientador](docs/resumo_orientador.md).
- [Plano dos próximos experimentos](docs/plano_experimentos.md).
- [Resultados processados e hashes de origem](dados/processados/comparacao_rodadas.json).
- Gráficos em `figuras/`, nos formatos PNG e SVG.

O script `scripts/comparar_rodadas.py` usa apenas dados locais e 5.000 réplicas bootstrap por rodada. As instruções para reproduzir a análise em ambiente separado estão no relatório. O CSV histórico de duas rodadas foi preservado; a comparação completa está no novo JSON e nas tabelas do relatório. Nenhum experimento novo foi enviado para produzir esses arquivos.

## Validação local concluída

O protocolo de comparação e o piloto de ZNE foram validados no PC, com modelos sintéticos de leitura e de ruído nas portas. Foram simulados 12 blocos, totalizando 486.000 shots; nenhum job novo foi enviado à IBM.

- [Registro de trabalho e commits locais](docs/registro_trabalho.md).
- [Relatório completo da simulação](dados/simulados/validacao_2026_11_01/relatorio.md).
- [Manifesto, sementes, versões e referências exatas](dados/simulados/validacao_2026_11_01/manifesto.json).
- [Auditoria dos dados e circuitos](dados/simulados/validacao_2026_11_01/verificacao.json).

Os scripts `scripts/protocolo_local.py`, `scripts/validar_protocolo_local.py` e `scripts/verificar_registro_local.py` são exclusivamente locais. As dependências estão em `requirements-simulacao.txt`, e os testes em `tests/`. O relatório contém os comandos de reprodução. Resultados sintéticos ficam em `dados/simulados/`, separados dos resultados reais em `dados/brutos/`.
