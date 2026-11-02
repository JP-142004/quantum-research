# Simulações locais

[Dados](../README.md) · [Método de simulação](../../docs/livro/07-simulacao-local/README.md) · [ZNE](../../docs/livro/08-zne/README.md)

## Execução disponível

[validacao_2026_11_01](validacao_2026_11_01/relatorio.md) contém nove blocos de comparação de construções e três blocos de ZNE. Total: 486.000 shots simulados. Nenhum deles foi executado na QPU da IBM.

| Arquivos | Papel |
| --- | --- |
| [manifesto.json](validacao_2026_11_01/manifesto.json) | Parâmetros, versões, referências exatas, sementes e hashes |
| [comparacao.qpy](validacao_2026_11_01/comparacao.qpy) | 40 circuitos compilados da comparação |
| [zne.qpy](validacao_2026_11_01/zne.qpy) | 42 circuitos compilados do piloto |
| `*_contagens.json` | Contagens de cada protocolo/cenário/bloco |
| `*_analise.json` | Estimativas, erros, intervalos e contrastes por bloco |
| [relatorio.md](validacao_2026_11_01/relatorio.md) | Apresentação dos resultados e limites |
| [verificacao.json](validacao_2026_11_01/verificacao.json) | Resultado da auditoria |

Cada nome como `comparacao_leitura_bloco_01_contagens.json` informa protocolo, cenário, bloco e tipo de conteúdo. A ordenação embaralhada é registrada em cada arquivo de contagens; os QPY seguem a ordem do catálogo do manifesto.

Os erros do modelo são escolhidos, não extraídos de uma calibração atual da IBM. Os blocos variam a amostragem com modelo fixo. Para reproduzir, use outro nome em `--execucao`; o executor não sobrescreve um diretório existente.

O manifesto cobre por hash 24 JSONs e dois QPY, não todos os documentos da pasta. A auditoria verifica essa lista e a coerência numérica. Veja o [dicionário de dados](../../docs/livro/10-codigo-dados/README.md) para os limites desse mecanismo.

## O teste de recuperação de um erro conhecido

Em cada bloco executamos 32 calibrações, o GHZ original e o conectado em duas bases, e quatro controles independentes. Cada circuito recebeu 1.000 shots. A comparação teve três blocos em cada um dos três cenários: 40 × 1.000 × 3 × 3 = **360.000 shots simulados**.

| Cenário | O que pudemos verificar |
| --- | --- |
| Ideal | As duas construções têm PZ e correlação X iguais a 1. Os controles de paridade dão os sinais esperados, inclusive −1 para o controle negativo. |
| Apenas leitura | Antes da leitura os indicadores valem 1. Depois do canal conhecido, as referências exatas são PZ = 0,836604 e correlação X = 0,695688. A inversão da matriz exata recupera o valor anterior à leitura. Com shots finitos há dispersão. |
| Leitura e portas | O modelo acrescenta despolarização após cada porta CX. Antes da leitura, o original já tem PZ = 0,840887 e correlação X = 0,769022. No conectado são 0,946261 e 0,922368. Corrigir a leitura recupera essas distribuições de referência no cálculo exato; os desvios produzidos pelas portas permanecem. |

O [protocolo](../../scripts/protocolo_local.py) associa a calibração aos bits físicos realmente medidos após o roteamento. O [executor](../../scripts/validar_protocolo_local.py) guarda contagens sorteadas e referências sem flutuação de shots. Isso permite conferir cada estimativa do [relatório](validacao_2026_11_01/relatorio.md) contra um alvo conhecido. As sementes variam entre blocos, enquanto o modelo permanece fixo. A etapa seguinte usou outros 126.000 shots no [piloto de ZNE](zne/README.md).
