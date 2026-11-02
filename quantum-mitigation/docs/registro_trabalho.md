# Registro de trabalho — PIBIC

## 1 de novembro de 2026

### Histórico e preservação

A cópia de trabalho é `C:/Users/luizb/Desktop/PIBIC quantica/quantum-research`, branch `mitigation`. Foram incorporados por fast-forward os commits `d798852`, `958a680` e `daa2b2f` da outra cópia local. As alterações anteriormente preparadas no Desktop eram idênticas ao primeiro commit; seu backup permanece no stash identificado como `Backup Desktop antes de incorporar mitigation 2026-11-01`.

O job real `dbjnndgnceqs73akbkh0` já estava concluído. Seus resultados foram utilizados sem nova consulta ou submissão. Naquela etapa de organização ainda não havia sido feito push. Posteriormente, após autorização, os seis commits até `8ff5086` foram publicados na branch `mitigation`, sem alterar `main`.

### Comparação dos dados reais

Commit local `e2fea3b` — consolida três rodadas, gráficos, análise com 5.000 réplicas bootstrap por rodada, resumo para o orientador e plano experimental. Foram preservados os dados brutos e os resultados históricos. Ver [comparação](comparacao_rodadas.md), [resumo](resumo_orientador.md) e [plano](plano_experimentos.md).

### Implementação local

Commit local `1e21d5a` — implementa os circuitos originais e conectados, calibração de 32 estados, quatro controles independentes, compilação em mapa sintético, inversão com correção do mapa físico/clássico e bootstrap compartilhado. Inclui piloto de ZNE com dobramento global de fatores 1, 3 e 5. Nenhum desses scripts importa o cliente IBM Runtime, lê credenciais ou oferece comando de submissão.

Seis testes automatizados passaram: distribuições ideais e roteamento dos 40/42 circuitos, controle negativo, canal de leitura assimétrico e mapeamento, convenção do Aer para leitura, rejeição de dados inválidos/matriz singular e extrapolação linear/identidade.

### Execução registrada

O PC possui Intel Core Ultra 9 275HX, aproximadamente 32 GB de RAM e RTX 5070 Ti Laptop. A simulação usa CPU, com no máximo quatro threads; a GPU não foi necessária. Bibliotecas já instaladas: Python 3.12.10, NumPy 2.5.4, Qiskit 2.6.0 e Qiskit Aer 0.17.2. As dependências estão fixadas em `requirements-simulacao.txt`.

Execução `validacao_2026_11_01`: três blocos em cada cenário ideal, leitura e leitura + portas, mais três blocos de ZNE local. Cada circuito recebe 1.000 shots simulados; cada bloco usa 2.000 réplicas bootstrap. O total é 486.000 shots simulados, sem consumo de QPU da IBM.

O [relatório local completo](../dados/simulados/validacao_2026_11_01/relatorio.md) apresenta os valores brutos/ajustados, diferenças entre construções, controles e extrapolação. O [manifesto](../dados/simulados/validacao_2026_11_01/manifesto.json) registra parâmetros, sementes, versões, tempos, referências exatas e hashes. Os QPY preservam os circuitos compilados; contagens e análises ficam separadas por bloco. A [auditoria](../dados/simulados/validacao_2026_11_01/verificacao.json) confere os hashes, os QPY, os totais e a coerência com o modelo exato.

O programa recusa sobrescrever uma execução existente. Uma nova simulação deve usar outro nome em `--execucao`. Os dados simulados ficam exclusivamente em `dados/simulados/`, separados de `dados/brutos/`, que contém resultados reais.

### Limites e trabalho que depende de hardware

Os erros e a conectividade usados são sintéticos. As repetições variam a semente de amostragem; não reproduzem deriva real do dispositivo. A validação confirma a implementação no modelo, não prevê numericamente os próximos resultados da IBM. O protocolo de hardware ainda precisa de compilação e conferência contra um backend real disponível, com propriedades e opções atuais.

A próxima decisão é discutir com o orientador o protocolo de comparação com controles (120.000 medidas reais propostas). O piloto ZNE local serve de preparação metodológica; não autoriza nem agenda automaticamente ZNE no hardware. Nenhum experimento real novo foi executado.

### Reproduzir a auditoria

```powershell
python quantum-mitigation/scripts/verificar_registro_local.py quantum-mitigation/dados/simulados/validacao_2026_11_01
```

O resultado da auditoria usa um limite amplo de seis erros padrão para detectar inconsistências numéricas; isso não é teste confirmatório nem estudo da cobertura dos intervalos. As instruções completas de instalação e simulação estão no relatório local.


## 2 de novembro de 2026 — documentação em capítulos

A frente de mitigação recebeu um [índice em formato de livro](../README.md), com 12 capítulos sobre fundamentos, circuitos, leitura, experimentos, estatística, simulação, ZNE, reprodução, código, histórico e referências. READMEs de pasta explicam os scripts e seus efeitos, a origem dos dados, os testes e as figuras. O README da modelagem agora distingue o código existente das pastas reservadas.

Os textos foram conferidos contra scripts e registros, sem alterar contagens, circuitos, resultados numéricos ou o protocolo experimental. A revisão contextualizou a ausência de ZNE na importação histórica e a publicação posterior no GitHub. Os relatórios gerados permanecem como registros das análises que os produziram.

A revisão principal foi registrada no commit `d4f7869`. A verificação documental conferiu 39 arquivos Markdown e 291 links internos, além da consistência estrutural das tabelas e dos blocos de código. As fórmulas nas tabelas foram ajustadas para não quebrar suas colunas no Markdown. A comparação com `8ff5086` confirmou que scripts, requirements, JSONs, CSVs, QPY e figuras permaneceram intactos. Não foi necessário reexecutar experimentos ou simulações para essa mudança documental.
