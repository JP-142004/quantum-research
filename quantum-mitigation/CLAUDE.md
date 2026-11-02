# Instruções para o Claude Code neste projeto

Projeto de PIBIC do Luiz (Engenharia de Computação, PUCPR): **mitigação de ruído em circuitos quânticos**, começando pelo estado GHZ. Este repositório é a **referência** do artigo, não o artigo. Cada pasta tem uma função:

- `README.md` (root): introdução curta, como num repositório normal de GitHub. Sem resultados, tabelas nem regras longas.
- `fundamentos/`: toda a teoria, explicada do zero (conceitos, ruído, indicadores, técnicas com as contas, referências).
- `experimentos/`: um mini relatório por experimento, na ordem em que foram feitos, com o código ao lado. Molde fixo (seção "Molde de um experimento" de `experimentos/README.md`): Pergunta, Como foi feito, Resultado, Conclusão, Próximo passo, Arquivos.
- `dados/`: só mostra os dados e a origem de cada arquivo, sem análise.
- `figuras/`: todas as imagens do repositório, com o número do experimento no nome.
- `docs/`: `relatorio.md` (formato de artigo), `planejamento.md` e relatórios de apoio.
- `scripts/` e `tests/`: análise, validação e testes, cada arquivo explicado.

Leia o README, depois `experimentos/README.md`.

## Responsabilidades e escopo

- O Luiz cuida de **mitigação** (esta pasta). A **modelagem** é do João Paulo (`../quantum-modeling`). Não escreva "fizemos" sobre a modelagem.
- **Altere apenas `quantum-mitigation/`.** Não mexa no README da raiz nem em `quantum-modeling`.
- Trabalhe na branch `mitigation`. Nunca na `main`.

## Git

- Faça commits locais, um por etapa, com mensagem em português que diga o que mudou e por quê.
- **Push só quando o Luiz pedir**, e só para `mitigation`, sem `--force`:
  `git -c credential.https://github.com.username=Luizafonsobsilva push origin refs/heads/mitigation:refs/heads/mitigation`
- **Nunca peça, leia nem grave tokens ou senhas**, em arquivo ou no chat.

## IBM Quantum: regras de segurança

- **Não envie jobs.** Os programas de `experimentos/01` a `04` enviam circuitos à IBM quando executados. Não os execute nem os importe.
- Consultar jobs antigos para recuperar resultados é permitido quando o Luiz pedir. **Novos envios exigem uma decisão específica dele**, com orçamento de medidas combinado antes.
- O job `dbjnndgnceqs73akbkh0` (rodada 3) já terminou. Nunca o reenvie.

## Dados: não alterar

- Não edite nada em `dados/brutos`, `dados/simulados` nem os arquivos `.qpy`. São o registro original. Tabelas e figuras derivadas podem ser recriadas por script.
- O auditor `scripts/verificar_registro_local.py` acusa "Arquivo alterado" em checkouts com quebras de linha LF. É um problema conhecido de CRLF, explicado em `scripts/README.md`. Não "corrija" os hashes do manifesto.

## Como escrever (preferências do Luiz)

- **Simples e didático.** Uma pergunta por etapa, uma conta real com os números, e a interpretação. Sem historinhas nem analogias longas. Pouca hierarquia. Poucos caminhos concorrentes de leitura.
- **Resultados em imagens** (arquivos em `figuras/`), com legendas curtas que digam o que cada ponto ou barra mostra. Explique cada arquivo de uma pasta em uma linha.
- **Sem repetir avisos.** Diga cada limite no lugar onde ele importa. Evite o tom genérico de texto gerado por IA.
- Cada número de tabela vem dos dados (`scripts/gerar_tabelas.py`), nunca digitado à mão.
- Sempre distinga **observado**, **ajustado (estimado)** e **simulado**. Informe backend e data.
- Não diga que há "fidelidade" nem que o erro das portas foi eliminado. Não atribua causa que os dados não mostram.
- Só cite referências que você conseguiu abrir. Não invente citações.

## Fluxo de qualquer mudança (a partir desta pasta)

1. Edite os textos.
2. `python scripts/gerar_tabelas.py` (preenche as tabelas marcadas com `TABELA:nome`).
3. `python scripts/verificar_links.py` (links e âncoras).
4. `python -m unittest discover -s tests` (testes; os de simulação precisam de `requirements-simulacao.txt`).
5. Confira que `dados/` não mudou (`git status`).
6. Commit local. Push só se o Luiz pedir.

## Como acrescentar um experimento ou técnica

Copie o molde de `experimentos/README.md`, defina pergunta, indicador, controle e critério de sucesso **antes** de executar, guarde as contagens em `dados/` com o mesmo número, e atualize as tabelas de `experimentos/README.md`, `fundamentos/tecnicas.md` e `dados/README.md`.

## Estado em 2 de novembro de 2026

- Repositório reorganizado em 2 de novembro de 2026: root curto, um mini relatório por experimento, imagens em `figuras/`, dados sem análise. O texto em formato de artigo está em `docs/relatorio.md`; falta preencher **autoria, orientação e instituição** no cabeçalho dele.
- Experimentos 1 a 4 medidos na IBM. Experimentos 5 e 6 simulados no PC.
- A proposta de 120.000 medidas na IBM (`docs/planejamento.md`) **aguarda decisão do Luiz**. Nada dela foi executado.
- Ainda falta um leitor que não conhece o trabalho ler só o root, `fundamentos/` e um experimento e dizer o que não entendeu.

Em caso de dúvida sobre escopo, dados ou envio à IBM, **pergunte ao Luiz antes de agir**.
