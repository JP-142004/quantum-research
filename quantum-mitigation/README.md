# Mitigação de ruído em circuitos quânticos

Esta pesquisa investiga como identificar os efeitos do ruído em circuitos quânticos e avaliar técnicas para reduzi-los. Começamos com circuitos GHZ porque conhecemos os resultados esperados em condições ideais. Isso nos permitiu observar desvios, mudar a construção dos circuitos e testar a calibração da leitura. A pesquisa será ampliada para outros circuitos e técnicas. Cada nova etapa será documentada junto de seus dados, resultados e limitações.

## O que chamamos de ruído?

Imagine preparar cinco qubits em zero e ler `00001`. A preparação pode ter deixado um qubit em um estado diferente do previsto. Uma porta, a operação que transforma os qubits, pode ter aplicado uma rotação ligeiramente errada. Durante uma espera, um qubit excitado pode perder energia, ou uma superposição pode perder a relação de fase entre suas componentes. Por fim, o detector pode registrar um bit incorretamente. Uma única leitura mostra o resultado final. Para distinguir as causas, precisamos de controles com respostas conhecidas e de comparações em que mudamos uma condição por vez.

Mesmo um circuito ideal pode dar resultados diferentes a cada repetição, chamada *shot*. No GHZ ideal, todos zeros e todos uns têm a mesma probabilidade na base Z. Obter 493 de um tipo e 507 do outro em mil tentativas é compatível com esse sorteio. Já obter sequências intermediárias nessa base é um desvio em relação ao alvo ideal. Mitigar significa reduzir o efeito desses desvios sobre o resultado que queremos estimar. Neste projeto, mudamos tanto o circuito que o equipamento executa quanto o cálculo feito a partir das contagens.

## Percurso experimental

| Pergunta | Registro disponível |
| --- | --- |
| [1. O que muda com o tamanho?](experimentos/01_ghz_escala/README.md) | Série histórica de hardware, com contagens de 5 a 50 qubits. |
| [2. O que acontece com estados simples?](experimentos/02_controles/README.md) | Programas históricos preservados; faltam as contagens separadas desses controles. |
| [3. Podemos usar menos portas?](experimentos/03_ghz_conectado/README.md) | Comparação histórica relatada no Fez; a comparação local também tem dados simulados. |
| [4. Quanto muda o indicador após calibrar a leitura?](experimentos/04_mitigacao_leitura/README.md) | Três rodadas concluídas no Fez, com 102.000 shots reais e resultados recalculáveis. |
| [5. O que a técnica recupera quando conhecemos o erro?](dados/simulados/README.md) | Comparação local em três cenários, 360.000 shots simulados. |
| [6. O que acontece ao extrapolar para ruído zero?](dados/simulados/zne/README.md) | Piloto local, 126.000 shots simulados. |
| [Próxima etapa em hardware](docs/plano_experimentos.md) | Comparação planejada com controles independentes, 120.000 medidas propostas. |

## Continuidade da pesquisa

Para cada novo circuito ou técnica, crie uma pasta com README e acrescente uma linha ao percurso. Registre a **pergunta**, o **circuito de teste** e seu resultado ideal, o **tipo de ruído** investigado, o **controle**, a **origem dos dados**, o **cálculo**, o **resultado com incerteza** e as **limitações**. Uma comparação com outro circuito pode ser acrescentada mesmo que seu indicador de interesse seja diferente de PZ ou CX.

| Técnica | O que investigar | Situação nesta pesquisa |
| --- | --- | --- |
| Extrapolação a ruído zero (ZNE) | Variar a exposição ao ruído e estimar o indicador no limite de ruído zero. A escolha do ajuste altera o resultado. | Piloto simulado concluído. [Método de dobramento](https://arxiv.org/abs/2005.10921) |
| Pauli twirling | Sortear operações de Pauli compensadas que preservam o circuito ideal e mudam como erros coerentes se acumulam na média. Requer várias versões do circuito. | Possibilidade futura. |
| Desacoplamento dinâmico | Inserir pulsos durante esperas para reduzir efeitos de certas perturbações. A duração das esperas e os erros dos pulsos influenciam o benefício. | Possibilidade futura. |
| Cancelamento probabilístico de erros (PEC) | Combinar amostras com pesos positivos e negativos com base em um modelo de ruído. A variância pode exigir muitos shots. | Possibilidade futura. |

Para comparar os mecanismos dessas técnicas, veja o [guia da IBM](https://quantum.cloud.ibm.com/docs/en/guides/error-mitigation-and-suppression-techniques) e o [trabalho de Temme e colaboradores](https://arxiv.org/abs/1612.02058). A escolha do próximo circuito e da próxima técnica permanece aberta.

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
