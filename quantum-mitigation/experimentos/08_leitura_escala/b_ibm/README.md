# Experimento 8, parte B · Na IBM, em 10 e 20 qubits, a calibração por qubit leva os indicadores perto do ideal?

**Estado em 22 de novembro de 2026:** plano, receita, verificação de independência e teste prévio com dados existentes. **Nada foi enviado à IBM.** O envio exige a aprovação do Luiz para aquele envio específico, depois de ele conferir o saldo de tempo do plano. Faltam: confirmar os critérios abaixo e escrever o código de análise dos dados da IBM, os dois **antes** do envio.

## Resposta curta

*A escrever depois da execução.*

## Pergunta

Em 20 qubits a matriz completa de calibração não existe (seriam 2²⁰ calibrações). A calibração por qubit é o que cabe. Com ela, o GHZ conectado de 10 e de 20 qubits fica perto do ideal? E a hipótese de que cada qubit lê sem influência dos vizinhos aguenta?

## Como será feito (plano)

- **Computador:** `ibm_fez`, como nos experimentos 1 a 4. **3 sessões em dias diferentes**, como no 4.
- **Em cada sessão e para n = 10 e n = 20:** GHZ conectado em Z e em X; **4 calibrações**: `00…0`, `11…1`, `0101…` e `1010…`; 4 controles independentes (zeros e uns em Z; todos em `+` e todos em `+` com o qubit 0 em `−`, em X). 10 circuitos por tamanho, 20 por sessão, 20.000 medidas por sessão.
- **Por que 4 calibrações:** `00…0` e `11…1` dão a tabela 2 × 2 de cada qubit. `0101…` e `1010…` dão a tabela do mesmo qubit com os vizinhos em outro estado: se a tabela mudar entre os dois grupos, a leitura de um qubit depende do estado dos vizinhos.
- **Duas formas de os qubits não serem independentes, duas verificações.** (1) *Dependência do estado dos vizinhos*: compara as tabelas dos dois grupos de calibração. (2) *Erros que acontecem juntos*, mesmo sem depender do estado (como na parte A): compara, em `00…0` e em `11…1`, a variância do número de erros por medida com a soma das variâncias de cada qubit (código em `mitigacao/leitura_independencia.py`). **A verificação (1) não enxerga a (2)**: na parte A, o erro conjunto muda os dois grupos do mesmo jeito. Por isso a (2) existe.
- **Resultados que serão olhados:** (1) a verificação de erros conjuntos; (2) a tabela de cada qubit nos dois grupos de calibração, com a diferença e o intervalo de 95%; (3) PZ e CX do GHZ, observados e ajustados; (4) os controles depois do ajuste.
- **Limite já conhecido:** em 20 qubits não há a matriz completa como referência. A conferência é só pelos controles e pelas verificações de independência, que é mais fraca que a do experimento 7. A verificação (1) ainda não foi testada em simulador: o simulador não tem erro que dependa do estado dos vizinhos.
- **Antes de qualquer envio:** `python rodar.py 08b --verificar --online` para conferir que o GHZ, as calibrações e os controles de cada tamanho usam os **mesmos qubits físicos** e quantas portas de dois qubits cada circuito tem. A verificação local já confere que todos os circuitos dão o resultado ideal declarado.

### Proposta de critérios (a confirmar pelo Luiz antes do envio)

| O quê | Regra proposta |
| --- | --- |
| Erros conjuntos, por tamanho e sessão | **Não rejeitada** se o p-valor for > 0,01 em `00…0` e em `11…1`; **rejeitada** se for ≤ 0,001 em qualquer um; entre os dois, **inconclusivo** (olhar os pares). Com 12 verificações no total, 1 delas em 100 cai abaixo de 0,01 por acaso. |
| Dependência dos vizinhos | A diferença entre as tabelas dos dois grupos, por qubit, dentro de ±0,02 com 95% de confiança (a margem provisória do experimento 7, ainda sem justificativa). |
| GHZ ajustado | O mesmo critério do experimento 4: nas 3 sessões, mais perto de 1 que o observado, com o intervalo de 95% do ganho acima de zero. |
| Controles | Cada controle ajustado a no máximo 2 erros padrão de 1, como no experimento 4. |

Se a independência for rejeitada, o ajuste por qubit não vale para aquele tamanho e o relatório diz isso, mesmo que o GHZ melhore.

## Teste prévio da verificação de independência (sem IBM)

Tabela gerada por `piloto.py` com dados que já existem: as sessões da parte A (onde sabemos que o cenário `leitura_correlacionada` tem erro conjunto) e as do [experimento 4](../../04_calibracao_leitura/README.md) (IBM, 5 qubits). **T** é o excesso de variância; a coluna seguinte é o T que se esperaria com os qubits embaralhados (sem ligação entre eles); o p-valor vem de 1.000 embaralhamentos (o menor possível é 0,001). A última coluna é o par de qubits com mais erros juntos.

<!-- TABELA:piloto -->
| Origem | Sessão · estado | Taxa de erro por qubit | T | T com qubits embaralhados | p-valor | Par com mais erros juntos |
| --- | --- | ---: | ---: | --- | ---: | --- |
| A · simulador, 10 qubits | leitura_bloco_01 · zeros | 0,029 | 0,015 | 0,000 ± 0,012 | 0,130 | 5–7: 4 (esperado 1,3) |
| A · simulador, 10 qubits | leitura_bloco_01 · uns | 0,040 | -0,009 | 0,000 ± 0,016 | 0,741 | 3–7: 5 (esperado 1,9) |
| A · simulador, 10 qubits | leitura_bloco_02 · zeros | 0,030 | 0,034 | 0,000 ± 0,012 | 0,011 | 2–6: 5 (esperado 1,1) |
| A · simulador, 10 qubits | leitura_bloco_02 · uns | 0,038 | -0,004 | -0,000 ± 0,015 | 0,605 | 3–9: 5 (esperado 2,5) |
| A · simulador, 10 qubits | leitura_bloco_03 · zeros | 0,030 | 0,015 | 0,000 ± 0,012 | 0,134 | 0–6: 5 (esperado 2,3) |
| A · simulador, 10 qubits | leitura_bloco_03 · uns | 0,039 | -0,004 | -0,001 ± 0,016 | 0,608 | 4–9: 8 (esperado 3,4) |
| A · simulador, 10 qubits | leitura_correlacionada_bloco_01 · zeros | 0,058 | 0,294 | 0,001 ± 0,023 | 0,001 | 8–9: 34 (esperado 2,3) |
| A · simulador, 10 qubits | leitura_correlacionada_bloco_01 · uns | 0,064 | 0,209 | 0,001 ± 0,024 | 0,001 | 8–9: 38 (esperado 7,4) |
| A · simulador, 10 qubits | leitura_correlacionada_bloco_02 · zeros | 0,059 | 0,294 | 0,001 ± 0,023 | 0,001 | 8–9: 37 (esperado 2,5) |
| A · simulador, 10 qubits | leitura_correlacionada_bloco_02 · uns | 0,067 | 0,271 | 0,002 ± 0,026 | 0,001 | 6–7: 37 (esperado 5,1) |
| A · simulador, 10 qubits | leitura_correlacionada_bloco_03 · zeros | 0,058 | 0,286 | 0,001 ± 0,024 | 0,001 | 2–3: 37 (esperado 3,8) |
| A · simulador, 10 qubits | leitura_correlacionada_bloco_03 · uns | 0,066 | 0,296 | 0,000 ± 0,026 | 0,001 | 8–9: 35 (esperado 6,9) |
| Experimento 4 · IBM, 5 qubits | 2026-11-08_ibm_fez · zeros | 0,015 | -0,001 | -0,000 ± 0,002 | 0,806 | 1–3: 1 (esperado 0,7) |
| Experimento 4 · IBM, 5 qubits | 2026-11-08_ibm_fez · uns | 0,022 | 0,003 | -0,000 ± 0,004 | 0,289 | 1–3: 3 (esperado 1,0) |
| Experimento 4 · IBM, 5 qubits | 2026-11-09_ibm_fez · zeros | 0,009 | -0,001 | -0,000 ± 0,002 | 0,979 | 0–2: 0 (esperado 0,0) |
| Experimento 4 · IBM, 5 qubits | 2026-11-09_ibm_fez · uns | 0,022 | -0,007 | 0,000 ± 0,004 | 0,947 | 1–3: 1 (esperado 0,7) |
| Experimento 4 · IBM, 5 qubits | 2026-11-10_ibm_fez · zeros | 0,015 | 0,001 | 0,000 ± 0,003 | 0,501 | 0–1: 1 (esperado 0,1) |
| Experimento 4 · IBM, 5 qubits | 2026-11-10_ibm_fez · uns | 0,024 | 0,001 | -0,000 ± 0,004 | 0,352 | 0–2: 1 (esperado 0,1) |
<!-- /TABELA:piloto -->

**O que o teste mostra.** No simulador com erro conjunto, os 6 casos deram p = 0,001 e T de 0,21 a 0,30, com um par vizinho no topo: a verificação detecta uma correlação de 0,03. Sem erro conjunto, os p-valores foram de 0,011 a 0,741 (um valor baixo em 6, o que o acaso explica). Nas 3 sessões reais do experimento 4, de 0,29 a 0,98: **nenhum sinal de erros conjuntos em 5 qubits**. Limite: as taxas de erro reais são pequenas (0,9% a 2,4% por qubit, contra 3% a 7% no simulador), então o teste detecta correlações grandes e não garante a ausência de correlações pequenas.

## Resultado, Conclusão e Próximo passo

*Não há dados.*

## Arquivos

| Arquivo | Para que serve |
| --- | --- |
| `experimento.py` | A receita, pronta para `python rodar.py 08b --verificar` (local, não envia). |
| `piloto.py` | Teste prévio da verificação de independência com dados que já existem. Gera `resultados/piloto_independencia.md` e `.json`. |
| `resultados/` | Saída do `piloto.py`. Ainda não há resultados da IBM. |

**Execução:** IBM (`ibm_fez`). **Nada é enviado sem `--enviar` e sem a confirmação do Luiz.**

[Experimento 8](../README.md) · [Experimentos](../../README.md)
