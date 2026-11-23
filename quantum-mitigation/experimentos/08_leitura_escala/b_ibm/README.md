# Experimento 8, parte B · Na IBM, em 10 e 20 qubits, a calibração por qubit leva os indicadores perto do ideal?

**Estado em 22 de novembro de 2026:** plano, critérios, receita e código de análise prontos e testados com o simulador. **Nada foi enviado à IBM**: a máquina onde o código foi escrito não tem a conta IBM, então o envio é feito pelo Luiz (ver *Como executar*). Cada envio precisa da confirmação dele (`ENVIAR`) depois de conferir o saldo de tempo do plano.

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

### Critérios, definidos antes do envio

Propostos em 22/11/2026 e adotados quando o Luiz pediu para seguir. Se ele quiser mudar algum, tem que ser **antes** da primeira sessão.

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

## Como executar

Na máquina do Luiz, a partir de `quantum-mitigation/` (com a conta IBM salva):

1. `python rodar.py 08b --verificar --online`: consulta o `ibm_fez`, mostra os qubits físicos e as portas de dois qubits de cada circuito. **Não envia nada.** Conferir que, em cada tamanho, os circuitos usam os mesmos qubits.
2. `python rodar.py 08b --enviar --computador ibm_fez`: mostra os 20 circuitos (20.000 medidas) e só envia depois de digitar `ENVIAR`. Cria a pasta `dados/AAAA-MM-DD_ibm_fez/` com a ficha (o job fica registrado).
3. `python rodar.py 08b --coletar --sessao AAAA-MM-DD_ibm_fez`: grava as contagens quando o job terminar.
4. Repetir os passos 1 a 3 **em mais dois dias diferentes** (3 sessões, como no experimento 4).
5. `python experimentos/08_leitura_escala/b_ibm/analisar.py`: gera `resultados/` e preenche as tabelas abaixo. Com menos de 3 sessões, a tabela de critérios avisa.

A análise para se calibrações e circuitos de um tamanho usarem qubits diferentes. Ela foi testada com sessões do simulador de 5 e 10 qubits (o simulador não faz 20), incluindo o cenário com erro conjunto: com erro independente, a verificação 2 não rejeita e o GHZ de 10 qubits chega a 1; com erro conjunto, rejeita e o ajuste passa de 1, como na [parte A](../a_simulador/README.md).

## Resultado

*Ainda não há sessões da IBM. As tabelas abaixo são geradas por `analisar.py` quando houver dados e ficam vazias até lá.*

**Erros conjuntos (verificação 2).**

<!-- TABELA:independencia -->
| Sessão | n | Estado | Taxa de erro | T | p-valor | Pares com mais erros juntos (observado/esperado) |
| --- | ---: | --- | ---: | ---: | ---: | --- |
| 2026-11-23_ibm_fez | 10 | zeros | 0,008 | -0,000 | 0,672 | 6–8: 2/0,6, 0–1: 0/0,0 |
| 2026-11-23_ibm_fez | 10 | uns | 0,021 | -0,006 | 0,795 | 4–6: 2/0,8, 3–4: 3/1,8 |
| 2026-11-23_ibm_fez | 20 | zeros | 0,007 | 0,008 | 0,065 | 9–12: 2/0,0, 12–16: 2/0,2 |
| 2026-11-23_ibm_fez | 20 | uns | 0,018 | -0,031 | 0,981 | 3–13: 6/3,3, 12–14: 2/0,6 |
<!-- /TABELA:independencia -->

**Dependência do estado dos vizinhos (verificação 1).**

<!-- TABELA:contexto -->
| Sessão | n | Maior diferença | Equivalentes | Inconclusivas | Diferentes | Resultado |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| 2026-11-23_ibm_fez | 10 | 0,013 | 17 | 3 | 0 | inconclusivo |
| 2026-11-23_ibm_fez | 20 | 0,011 | 35 | 5 | 0 | inconclusivo |
<!-- /TABELA:contexto -->

**GHZ conectado: observado e ajustado.** Ganho = |observado − 1| − |ajustado − 1| (positivo é melhora).

<!-- TABELA:ghz -->
| Sessão | n | Indicador | Observado | Ajustado (2 estados) | Ganho [IC 95%] | Ajustado (4 estados) |
| --- | ---: | --- | ---: | ---: | ---: | ---: |
| 2026-11-23_ibm_fez | 10 | PZ | 0,7820 ± 0,0129 | 0,8986 ± 0,0170 | 0,117 [0,101; 0,134] | 0,8970 ± 0,0160 |
| 2026-11-23_ibm_fez | 10 | CX | 0,6640 ± 0,0235 | 0,8920 ± 0,0351 | 0,228 [0,195; 0,265] | 0,8862 ± 0,0331 |
| 2026-11-23_ibm_fez | 20 | PZ | 0,6160 ± 0,0153 | 0,7894 ± 0,0222 | 0,173 [0,153; 0,195] | 0,7805 ± 0,0208 |
| 2026-11-23_ibm_fez | 20 | CX | 0,5160 ± 0,0269 | 0,8670 ± 0,0491 | 0,351 [0,301; 0,406] | 0,8469 ± 0,0458 |
<!-- /TABELA:ghz -->

**Controles independentes.**

<!-- TABELA:controles -->
| Sessão | n | Controle | Observado | Ajustado (2 estados) | (ajustado − 1) / erro padrão |
| --- | ---: | --- | ---: | ---: | ---: |
| 2026-11-23_ibm_fez | 10 | `0000000000` em Z | 0,9270 ± 0,0081 | 1,0021 ± 0,0129 | 0,2 |
| 2026-11-23_ibm_fez | 10 | `1111111111` em Z | 0,8300 ± 0,0119 | 1,0272 ± 0,0211 | 1,3 |
| 2026-11-23_ibm_fez | 10 | `++++++++++` em X | 0,9200 ± 0,0086 | 0,9942 ± 0,0131 | -0,4 |
| 2026-11-23_ibm_fez | 10 | `+++++++++-` em X | 0,9070 ± 0,0092 | 1,0066 ± 0,0152 | 0,4 |
| 2026-11-23_ibm_fez | 20 | `00000000000000000000` em Z | 0,8710 ± 0,0108 | 1,0044 ± 0,0183 | 0,2 |
| 2026-11-23_ibm_fez | 20 | `11111111111111111111` em Z | 0,7020 ± 0,0143 | 1,0234 ± 0,0287 | 0,8 |
| 2026-11-23_ibm_fez | 20 | `++++++++++++++++++++` em X | 0,8350 ± 0,0116 | 0,9620 ± 0,0185 | -2,1 |
| 2026-11-23_ibm_fez | 20 | `+++++++++++++++++++-` em X | 0,8280 ± 0,0118 | 0,9797 ± 0,0198 | -1,0 |
<!-- /TABELA:controles -->

**Critérios, por sessão (na ordem das sessões).**

<!-- TABELA:criterios -->
| n | Erros conjuntos | Dependência dos vizinhos | GHZ melhorou (PZ e CX) | Controles a 2 erros padrão |
| --- | --- | --- | --- | --- |
| 10 | não rejeitada | inconclusivo | sim | sim (só 1 de 3 sessões) |
| 20 | não rejeitada | inconclusivo | sim | não (só 1 de 3 sessões) |
<!-- /TABELA:criterios -->

## Conclusão e Próximo passo

*Depois dos dados.*

## Arquivos

| Arquivo | Para que serve |
| --- | --- |
| `experimento.py` | A receita, pronta para `python rodar.py 08b --verificar` (local, não envia). |
| `analisar.py` | Analisa as sessões da IBM (10 e 20 qubits) e gera `resultados/` e as tabelas deste relatório. Código em `mitigacao/leitura_ibm.py` e `leitura_ibm_saida.py`. |
| `dados/AAAA-MM-DD_ibm_fez/` | Uma pasta por sessão (ainda não existem). **Não se edita.** |
| `piloto.py` | Teste prévio da verificação de independência com dados que já existem. Gera `resultados/piloto_independencia.md` e `.json`. |
| `resultados/` | Saída do `piloto.py`. Ainda não há resultados da IBM. |

**Execução:** IBM (`ibm_fez`). **Nada é enviado sem `--enviar` e sem a confirmação do Luiz.**

[Experimento 8](../README.md) · [Experimentos](../../README.md)
