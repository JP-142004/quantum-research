# Mitigação de ruído em circuitos quânticos

Os computadores quânticos atuais cometem erros: o resultado de um circuito se afasta do resultado ideal por causa do **ruído**. Este projeto estuda **técnicas de mitigação**, que estimam o resultado correto sem consertar o equipamento, e mede quanto cada uma aproxima o resultado do ideal e a que custo.

É a frente de **mitigação** de uma pesquisa de iniciação científica (PIBIC). A frente de modelagem de ruído está em [quantum-modeling](../quantum-modeling/README.md).

## Estado atual

Por enquanto o circuito de teste é o **estado GHZ**, porque sua resposta ideal é conhecida. Foram feitos seis experimentos, quatro em computadores da IBM e dois em simulação, com três técnicas: circuito com menos portas, calibração de leitura e extrapolação a ruído zero. O trabalho vai ser expandido com outras técnicas (twirling, desacoplamento dinâmico, PEC) e outros circuitos.

## Por onde começar

1. [fundamentos](fundamentos/README.md): a teoria, explicada do zero.
2. [experimentos](experimentos/README.md): um mini relatório por experimento, na ordem em que foram feitos, com pergunta, método, resultado, conclusão e próximo passo.
3. [docs](docs/README.md): o relatório em formato de artigo e o planejamento do que vem a seguir.

## Pastas

| Pasta | Conteúdo |
| --- | --- |
| [fundamentos](fundamentos/README.md) | Conceitos, ruído, indicadores, técnicas (com as contas) e referências. |
| [experimentos](experimentos/README.md) | Metodologia, resultados e conclusão de cada experimento, mais o código. |
| [dados](dados/README.md) | Contagens da IBM, resultados processados e simulados, sem análise. |
| [figuras](figuras/README.md) | Todos os gráficos do repositório. |
| [docs](docs/README.md) | Relatório, planejamento e relatórios de apoio. |
| [scripts](scripts/README.md) | Análise, simulação, validação e geração de tabelas e figuras. |
| [tests](tests/README.md) | Testes automatizados. |

## Aviso

Os programas das pastas de experimento 1 a 4 **enviam jobs à IBM** quando executados. Para estudar os resultados não é preciso executá-los: os dados já estão salvos.
