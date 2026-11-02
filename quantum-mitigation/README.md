# Mitigação de ruído em circuitos GHZ

Este é o ponto de entrada para entender a frente de mitigação do PIBIC. O projeto compara construções de circuitos GHZ, calibra a leitura e avalia os indicadores com incertezas. O livro abaixo parte dos conceitos básicos e chega ao código, aos resultados e à reprodução.

**Estado documentado em 2 de novembro de 2026:** três rodadas reais de mitigação no IBM Fez (102.000 shots), análise consolidada e validação local com piloto ZNE (486.000 shots simulados). O protocolo novo ainda não foi executado no hardware. Os resultados até `8ff5086` foram publicados na branch `mitigation`.

## Livro do projeto

Leia na ordem se estiver chegando agora. Cada capítulo tem navegação para o anterior, o próximo e este índice.

| Capítulo | O que você vai entender |
| --- | --- |
| [01. A pesquisa e o mapa do repositório](docs/livro/01-visao-geral/README.md) | Pergunta de pesquisa, estrutura e diferença entre medida, simulação e proposta. |
| [02. Qubits, portas e o estado GHZ](docs/livro/02-fundamentos/README.md) | Qubits, amplitudes, portas, emaranhamento, GHZ e fidelidade. |
| [03. Construção, compilação e medidas em Z e X](docs/livro/03-circuitos-medidas/README.md) | Construções original/conectada, roteamento, PZ, CX e ordem dos bits. |
| [04. Ruído e mitigação de leitura](docs/livro/04-mitigacao-leitura/README.md) | Matriz de calibração, exemplo numérico, inversão e quasiprobabilidades. |
| [05. Experimentos e resultados reais](docs/livro/05-experimentos-reais/README.md) | Origem dos arquivos, escala de 5 a 50 qubits e três rodadas IBM. |
| [06. Incertezas, bootstrap e interpretação](docs/livro/06-estatistica/README.md) | Erros padrão, bootstrap pareado, intervalos e limites das conclusões. |
| [07. Validação no computador local](docs/livro/07-simulacao-local/README.md) | Modelo de ruído, protocolos, controles, referências exatas e testes. |
| [08. Extrapolação a ruído zero](docs/livro/08-zne/README.md) | Dobrar circuitos, extrapolar, comparar incerteza e reconhecer viés. |
| [09. Como instalar, executar e conferir](docs/livro/09-reproducao/README.md) | Ambientes Python, comandos locais, auditoria e solução de problemas. |
| [10. Guia do código e dicionário de dados](docs/livro/10-codigo-dados/README.md) | Responsabilidade das funções, campos JSON, QPY e rastreabilidade. |
| [11. Histórico, conclusões e próximos passos](docs/livro/11-historico-limites/README.md) | O que foi feito, publicado, demonstrado e o que ainda está pendente. |
| [12. Glossário, perguntas frequentes e referências](docs/livro/12-glossario-fontes/README.md) | Vocabulário, dúvidas comuns e referências primárias. |

## Percursos de leitura

- **Primeiro contato:** capítulos 1–5, depois o resumo para o orientador.
- **Entender os números:** capítulos 3, 4 e 6, acompanhados do relatório comparativo.
- **Reproduzir no PC:** capítulos 7–10; os comandos locais não exigem conta IBM.
- **Planejar a próxima coleta:** capítulos 5, 11 e o plano experimental.

## Relatórios e registros

| Documento | Função |
| --- | --- |
| [Resumo para o orientador](docs/resumo_orientador.md) | Síntese para discussão científica |
| [Comparação das três rodadas](docs/comparacao_rodadas.md) | Resultados reais, incertezas e gráficos |
| [Relatório da validação local](dados/simulados/validacao_2026_11_01/relatorio.md) | Resultados dos modelos sintéticos e do ZNE local |
| [Plano experimental](docs/plano_experimentos.md) | Protocolos futuros e critérios de análise |
| [Registro de trabalho](docs/registro_trabalho.md) | Histórico de organização, implementação e publicação |
| [Organização da importação](docs/organizacao.md) | Proveniência dos arquivos históricos |
| [Inventário de importação](docs/inventario_importacao.json) | Relação origem/destino e hashes |

## Navegação por pasta

[Experimentos](experimentos/README.md) · [Scripts](scripts/README.md) · [Dados](dados/README.md) · [Figuras](figuras/README.md) · [Testes](tests/README.md) · [Documentos](docs/README.md) · [Modelagem](../quantum-modeling/README.md) · [Raiz do repositório](../README.md)

## Ler e executar são ações diferentes

Os programas históricos em `experimentos` podem enviar circuitos à IBM quando executados ou importados. Os scripts novos de análise e simulação são locais. Comece pelo capítulo 9 para reproduzir; não execute todos os arquivos Python em sequência. O job `dbjnndgnceqs73akbkh0` já terminou e seus dados estão salvos.

O livro foi conferido contra código e registros, mas não preenche lacunas de metadados históricos por suposição. Resultados reais, simulados e relatos sem contagens são identificados separadamente.
