# 12. Glossário, perguntas frequentes e referências

[← Anterior](../11-historico-limites/README.md) · [Índice do livro](../../../../README.md)

## Glossário

| Termo | Significado neste projeto |
| --- | --- |
| Backend | Equipamento ou serviço de execução selecionado |
| Bootstrap | Reamostragem estatística usada para estimar dispersão de estimadores |
| Calibração | Circuitos de estados conhecidos usados para estimar a matriz de leitura |
| Circuito lógico | Sequência de operações desejada, antes da adaptação ao hardware |
| Circuito compilado | Versão adaptada a portas, conexões e layout |
| Contagens | Quantas vezes cada bitstring apareceu |
| CX, porta | CNOT entre controle e alvo |
| CX, indicador | Correlação coletiva em X; nos textos também escrita $C_X$ |
| DD | Desacoplamento dinâmico; permaneceu desativado nas opções registradas da rodada 3 |
| Erro padrão, EP | Dispersão estimada de um estimador em amostras repetidas |
| GHZ | Estado multipartite usado como referência no projeto |
| H | Porta Hadamard |
| Hash | Identificador calculado dos bytes de um arquivo, usado para conferir mudanças |
| Job | Execução submetida a um serviço; seu ID identifica o registro |
| Layout | Correspondência entre qubits lógicos e físicos |
| Matriz densidade | Representação de estados puros ou mistos |
| PZ | População nos estados todos zeros e todos uns em Z |
| QPY | Formato de serialização dos circuitos do Qiskit |
| Quasiprobabilidade | Componente de um estimador que pode ser negativa após ajuste |
| QPU | Processador quântico |
| Roteamento | Adaptação das interações às conexões físicas |
| Seed/semente | Parâmetro para reproduzir escolhas pseudoaleatórias |
| Shot | Uma preparação seguida das medidas do circuito |
| SWAP | Operação que troca estados entre dois qubits |
| Twirling | Aleatorização usada em certas técnicas de tratamento de ruído; desativada nas opções registradas da rodada 3 |
| ZNE | Extrapolação de estimativas para ruído zero |

## Perguntas frequentes

**O computador pessoal tem qubits?** O trabalho local usa bits clássicos para calcular o comportamento de um modelo quântico. O hardware quântico real foi o da IBM nos jobs registrados.

**1.000 shots significam 1.000 qubits?** Não. Um circuito de cinco qubits pode ser repetido 1.000 vezes. Na rodada real, cada um dos 34 circuitos foi repetido 1.000 vezes.

**O ajuste muda os dados originais?** Não. Calcula estimativas derivadas. As contagens continuam sendo inteiros não negativos.

**Por que apareceu 1,03 ou uma componente negativa?** O estimador linear e a extrapolação não são restringidos ao espaço físico de probabilidades. A incerteza e o viés do modelo precisam acompanhar esses números.

**Se o valor corrigido fica perto de 1, o GHZ está perfeito?** Não. Há custo estatístico, hipótese de calibração e informação de estado que esses dois indicadores não determinam.

**Os três blocos simulados representam três calibrações reais da IBM?** Não. São amostras diferentes de um modelo fixo, com sementes diferentes.

**O repositório já faz correção quântica de erros?** Não implementa códigos de correção com qubits lógicos protegidos. Estuda construção de circuitos e mitigação por estimadores.

**Podemos simular 50 qubits porque cinco foi rápido?** Não em geral. Alguns estados e métodos estruturados permitem casos grandes; o custo depende do circuito e do ruído. A modelagem histórica usa MPS para os maiores GHZ, e isso não constitui garantia para circuitos arbitrários.

**Qual arquivo devo ler primeiro para uma reunião?** O [resumo para o orientador](../../resumo_orientador.md), depois o [relatório das três rodadas](../../../comparacao_rodadas.md). Para justificar método, use os capítulos 3, 4 e 6.

## Fontes e como foram usadas

Os números experimentais deste livro vêm dos arquivos locais identificados nos capítulos. As referências abaixo fundamentam conceitos e convenções; não são a origem das contagens do projeto. Consultadas em 2 de novembro de 2026. A documentação online pode corresponder a versões posteriores às registradas nos manifestos.

| Fonte primária | Uso na leitura |
| --- | --- |
| [IBM: GHZ e tomografia](https://quantum.cloud.ibm.com/docs/en/tutorials/shadow-tomography) | Estado GHZ e diferença entre observáveis e caracterização do estado |
| [IBM: ordenação de bits](https://quantum.cloud.ibm.com/docs/en/guides/bit-ordering) | Índices, representação textual e diagramas |
| [IBM: mitigação de leitura](https://quantum.cloud.ibm.com/docs/en/tutorials/readout-error-mitigation-sampler) | Canal clássico de atribuição; nosso cálculo usa matriz completa, não M3 |
| [AerSimulator](https://qiskit.github.io/qiskit-aer/stubs/qiskit_aer.AerSimulator.html) | Simulador e métodos de evolução |
| [Aer: ReadoutError](https://qiskit.github.io/qiskit-aer/stubs/qiskit_aer.noise.ReadoutError.html) | Convenção de probabilidades do canal de leitura |
| [Aer: depolarizing_error](https://qiskit.github.io/qiskit-aer/stubs/qiskit_aer.noise.depolarizing_error.html) | Definição do parâmetro de despolarização |
| [Temme, Bravyi e Gambetta, 2017](https://arxiv.org/abs/1612.02058) | Formulação de mitigação e extrapolação a ruído zero |
| [Giurgica-Tiron et al., 2020/2021](https://arxiv.org/abs/2005.10921) | Dobramento unitário e escolhas de extrapolação |

As contas de exemplos didáticos são ilustrativas e estão separadas das tabelas de resultados. Não citamos uma referência externa como validação de uma afirmação que depende de medidas locais ausentes.

---

[← Anterior](../11-historico-limites/README.md) · [Índice do livro](../../../../README.md)
