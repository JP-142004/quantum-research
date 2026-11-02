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
