# Instruções para o Claude Code neste projeto

Projeto de PIBIC do Luiz (Engenharia de Computação, PUCPR): **mitigação de ruído em circuitos quânticos**, começando pelo estado GHZ. Este repositório é a **referência** do artigo, não o artigo. Esta é a **versão 2**, reconstruída do zero; a versão 1 está na marca `mitigation-antiga` do Git.

## Estrutura e a regra dos 3 lugares

- `README.md`: capa curta, como num repositório normal de GitHub.
- `fundamentos/`: a teoria, explicada do zero. Cada circuito e cada técnica do código têm um arquivo de explicação com o mesmo nome.
- `mitigacao/`: o código, escrito uma vez. `circuitos/`, `tecnicas/`, `execucao/` (IBM e simulador com a mesma interface) e as contas.
- `experimentos/NN_nome/`: relatório, `experimento.py` (a receita), `dados/AAAA-MM-DD_computador/` (uma pasta por sessão, **nunca editada**) e `resultados/` (gerado dos dados).
- `tests/`: testes automáticos.

Cada coisa nova entra em um lugar só: um circuito é `mitigacao/circuitos/<nome>.py` mais `fundamentos/circuitos/<nome>.md`; uma técnica é `mitigacao/tecnicas/<nome>.py` mais `fundamentos/tecnicas/<nome>.md`; um experimento é uma pasta copiada de `experimentos/_molde`. **Não crie frameworks**: cada encaixe tem poucas funções, arquivos de código com até cerca de 150 linhas, sem linguagem de configuração.

## Responsabilidades e escopo

- O Luiz cuida de **mitigação** (esta pasta). A **modelagem** é do João Paulo (`../quantum-modeling`). Não escreva "fizemos" sobre a modelagem.
- **Altere apenas `quantum-mitigation/`.** Não mexa no README da raiz nem em `quantum-modeling`.
- Trabalhe na branch `mitigation-v2`. Nunca na `main`.

## Git

- Faça commits locais, um por etapa, com mensagem em português que diga o que mudou e por quê.
- **Push só quando o Luiz pedir**, e só para `mitigation-v2`, sem `--force`:
  `git -c credential.https://github.com.username=Luizafonsobsilva push origin refs/heads/mitigation-v2:refs/heads/mitigation-v2`
- **Nunca peça, leia nem grave tokens ou senhas**, em arquivo ou no chat.

## IBM Quantum: regras de segurança

- **Nunca envie jobs sem o Luiz aprovar aquele envio específico.** Antes de cada um, mostre circuitos, número de medidas e computador, e peça que ele confira o saldo de tempo do plano dele. O número de medidas não é o tempo de uso da IBM.
- Os programas de envio têm três modos (`--verificar`, `--enviar`, `--coletar`). Nada é enviado sem `--enviar`, e uma sessão já registrada não é reenviada.
- Opções fixas em todo envio: desacoplamento dinâmico desligado, twirling desligado, `init_qubits` ligado, compilação nível 1, semente 42 e 1.000 shots.
- Consultar jobs já feitos para recuperar resultados é permitido quando o Luiz pedir.

## Dados: não alterar

- Não edite nada em `experimentos/*/dados/`. É o registro original, e cada sessão nasce com a sua **ficha completa** (job, computador, dia e hora, qubits, opções, versões, circuitos), gravada automaticamente. Tabelas e figuras de `resultados/` podem ser refeitas.
- Os dados da versão 1 não ficam nesta branch. Estão na marca `mitigation-antiga`.

## Como escrever (preferências do Luiz)

- **Simples e didático.** Resposta curta no topo de cada relatório, uma pergunta por etapa, uma conta real com os números, e a interpretação. Sem historinhas nem analogias longas. Não presuma que o leitor conhece ruído ou técnicas: explique ou aponte para `fundamentos/`.
- **Resultados em imagens**, com legendas curtas que digam o que cada ponto ou barra mostra. Explique cada arquivo de uma pasta em uma linha.
- **Sem repetir avisos.** Diga cada limite no lugar onde ele importa. Evite o tom genérico de texto gerado por IA.
- Cada número de tabela vem dos dados, gerado por código, nunca digitado à mão.
- Sempre distinga **observado**, **ajustado (estimado)** e **simulado**. Informe computador e dia.
- Não diga que há "fidelidade" nem que o erro das portas foi eliminado. Não atribua causa que os dados não mostram.
- Só cite referências que você conseguiu abrir. Não invente citações.

## Fluxo de qualquer mudança

1. Edite.
2. Rode os testes, a partir da raiz do repositório: `venv/Scripts/python -m unittest discover -s quantum-mitigation/tests`. O ambiente (`venv/`, Python 3.12) se cria com `requirements.txt`; o `venv/` não vai para o Git.
3. Confira que `experimentos/*/dados/` não mudou (`git status`).
4. Commit local. Push só se o Luiz pedir.

Comandos do projeto (a partir de `quantum-mitigation/`): `python rodar.py NN --verificar` (local, não envia), `--enviar`, `--coletar --sessao NOME`, `--listar`. Nunca rode `--enviar` em um experimento da IBM sem a aprovação do Luiz.

Um circuito novo precisa declarar `EXEMPLOS` (lista de `(n, variante)`) no módulo dele: os testes o percorrem sozinhos. Arquivos de código ficam com até cerca de 150 linhas.

## Estado em 2 de novembro de 2026

- **Fases 1 e 2 prontas:** esqueleto, `fundamentos/`, plano dos experimentos, e o código em `mitigacao/` com `rodar.py` e 52 testes. Ainda não há dados nem análise (`analisar`), que entram na Fase 3 junto com os experimentos 5 e 6.
- Plano combinado: experimentos 1 a 4 em **3 sessões na IBM, em 3 dias**, no mesmo computador; experimentos 5 e 6 no simulador. O experimento 3 compara original e conectado em 5, 10 e 20 qubits.
- Fases seguintes, cada uma com aprovação do Luiz: 3) análise e experimentos 5 e 6 no simulador; 4) sessão 1 na IBM; 5) sessões 2 e 3; 6) relatórios finais.
- Os critérios de sucesso de `experimentos/README.md` são uma proposta e precisam ser confirmados antes da primeira sessão.

Em caso de dúvida sobre escopo, dados ou envio à IBM, **pergunte ao Luiz antes de agir**.
