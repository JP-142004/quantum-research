# Mitigação de ruído em circuitos quânticos: visão geral

Este repositório é a **referência** do artigo sobre mitigação de ruído: guarda os dados, os programas, as contas e os resultados em que o texto se apoia. O artigo é escrito à parte (rascunho em [docs/rascunho_artigo.md](docs/rascunho_artigo.md)) e cita este material. A modelagem de ruído é uma frente separada, de João Paulo, em [quantum-modeling](../quantum-modeling/README.md).

## A pergunta

Quanto cada técnica de mitigação aproxima os resultados de um circuito quântico do valor ideal, e a que custo? Começamos pelo estado GHZ de cinco qubits, porque conhecemos a resposta ideal. Medimos dois indicadores, **PZ** e **CX**, que valem 1 no caso ideal ([definições e contas](fundamentos/indicadores.md)).

## O que já foi feito

| # | Experimento | Onde | O que mostra |
| --- | --- | --- | --- |
| 1 | [Escala do GHZ, 5 a 50 qubits](experimentos/01_ghz_escala/README.md) | IBM | Como PZ cai quando o circuito cresce. |
| 2 | [Controles de estados conhecidos](experimentos/02_controles/README.md) | IBM | Se qubits isolados acertam estados simples. |
| 3 | [Construção com menos portas](experimentos/03_ghz_conectado/README.md) | IBM | Efeito de reduzir as portas de dois qubits (13 para 4). |
| 4 | [Calibração de leitura, 3 rodadas](experimentos/04_mitigacao_leitura/README.md) | IBM | Quanto o ajuste de leitura aproxima PZ e CX do ideal. |
| 5 | [Validação simulada](experimentos/05_validacao_simulada/README.md) | PC | O que a calibração recupera quando o erro é conhecido. |
| 6 | [ZNE simulada](experimentos/06_zne_simulado/README.md) | PC | Extrapolação a ruído zero, com viés e incerteza. |

Cada pasta de experimento traz pergunta, método, conta, resultado e limites. Backend e data de cada execução ficam no README do experimento.

**O que se sabe até aqui.** As condições dos experimentos diferem, então a tabela não é um ranking.

<!-- TABELA:sintese -->
| Técnica | Onde | Variação nos indicadores | Custo |
| --- | --- | --- | --- |
| Construção com menos portas | IBM Fez, valores brutos | PZ +0,055; CX +0,208 | 9 portas CX a menos (13 → 4); nenhum shot extra |
| Calibração de leitura | IBM Fez, 3 rodadas | PZ +0,070 a +0,072; CX +0,148 a +0,164 | 32 circuitos de calibração por rodada; erro padrão maior |
| Extrapolação a ruído zero | Simulação, referência exata | PZ 0,9463 → 0,9899 (fator 1 → extrapolado) | 3 versões do circuito, até 20 CX; erro padrão maior; viés da reta |
<!-- /TABELA:sintese -->

## O que vem a seguir

Nada abaixo foi executado em hardware. O protocolo está em [docs/plano_experimentos.md](docs/plano_experimentos.md).

1. O protocolo do experimento 5 na IBM (120.000 medidas). Depende de decisão do Luiz.
2. Piloto de ZNE na IBM (126.000 medidas).
3. Mais qubits, comparando um modelo de leitura escalável com a matriz completa em cinco qubits.
4. Twirling, desacoplamento dinâmico e PEC no GHZ ([técnicas](fundamentos/tecnicas.md)).
5. Outros circuitos, depois de caracterizar as técnicas no GHZ.
6. Preencher autoria, orientação e instituição do artigo e pedir a um leitor externo que diga o que não entendeu.

Para acrescentar uma etapa, copie [experimentos/_modelo](experimentos/_modelo/README.md), defina pergunta, indicador, controle e critério de sucesso antes de executar, guarde as contagens em `dados/` e atualize as tabelas de [experimentos](experimentos/README.md) e de [técnicas](fundamentos/tecnicas.md).

## Onde está cada coisa

| Pasta | Conteúdo |
| --- | --- |
| [fundamentos](fundamentos/README.md) | Ruído, técnicas, indicadores e referências. |
| [experimentos](experimentos/README.md) | Um README por experimento e os programas históricos. |
| [dados](dados/README.md) | Contagens da IBM (brutos), resultados processados e simulados. |
| [figuras](figuras/README.md) | Gráficos usados no texto. |
| [scripts](scripts/README.md) | Análise e geração das tabelas. |
| [tests](tests/README.md) | Testes de tabelas, links e números citados. |
| [docs](docs/README.md) | Rascunho do artigo, plano, relatórios de apoio e [arquivo](docs/arquivo/README.md) de documentos anteriores. |

## Regras do repositório

- As tabelas vêm dos dados (`python scripts/gerar_tabelas.py`), nunca digitadas à mão. Os links se conferem com `python scripts/verificar_links.py`.
- Todo resultado é identificado como **observado** (IBM), **ajustado** (estimado a partir do observado) ou **simulado**.
- Os programas dos experimentos 1 a 4 **enviam jobs à IBM** quando executados. Comandos seguros: [scripts/README.md](scripts/README.md). Novos envios exigem decisão específica e orçamento de medidas combinado antes.
- `dados/brutos` e `dados/simulados` são o registro original e não se editam.
