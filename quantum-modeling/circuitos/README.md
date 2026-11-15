# Circuitos para enviar à IBM

Esta pasta define **o que vamos rodar no hardware**. As saídas que a IBM devolve ficam em
`dados/<lote>/`. O lote a enviar é descrito em um arquivo JSON (por exemplo, `lote01.json`), e
os circuitos são montados por `nucleo/circuitos.py`.

## Por que um lote novo

Os 10 jobs antigos têm um job por tamanho, em dias e layouts diferentes. Assim, o efeito do
tamanho se mistura com o da calibração, do layout e da data (feedback do relatório 1).
No lote novo:
- **todos os circuitos usam a mesma cadeia de qubits físicos** (o GHZ-5 usa os 5 primeiros
  qubits da cadeia do GHZ-40, e assim por diante);
- **cada repetição é um job**, e todos os jobs vão no mesmo `Batch`, rodando em sequência,
  com pouca diferença de calibração entre eles;
- a **calibração de cada job** é salva junto com as saídas.

## Circuitos do `lote01`

| Nome | Qubits | O que faz | Para que serve |
|---|---|---|---|
| `leitura0_n40` | 40 | Não aplica nenhuma porta e mede tudo (ideal: só zeros) | Mede P(1\|0) de cada qubit, o erro de leitura 0→1 |
| `leitura1_n40` | 40 | Aplica X em todos e mede (ideal: só uns) | Mede P(0\|1) de cada qubit, o erro de leitura 1→0, que soma leitura e relaxação T1 |
| `ghz_n05` | 5 | GHZ: H no primeiro qubit + cadeia de CNOTs | Circuito pequeno: pouco ruído de porta |
| `ghz_n20` | 20 | GHZ | Tamanho intermediário |
| `ghz_n40` | 40 | GHZ | Circuito grande: o ruído de porta e de relaxação domina |
| `paridade_n05_fK` | 5 | GHZ-5 + rotação de fase φ_K em cada qubit + medida na base X | Verifica se o estado é **coerente** (a paridade oscila como cos(5φ)), o que as contagens na base Z não mostram |

São 8 fases para a paridade, cobrindo um período (φ_K = K · 2π / (5·8)). No total, cada
repetição tem **13 circuitos**, com 1000 shots cada.

Os dois circuitos de leitura testam a hipótese indicada pelo professor: no GHZ-50 antigo,
"tudo 1" apareceu 2 vezes no hardware e 141 na simulação. Se P(0|1) for muito maior que
P(1|0), a leitura assimétrica explica parte dessa diferença.

## Campos do arquivo do lote

| Campo | Significado |
|---|---|
| `backend` | Computador da IBM (`ibm_kingston`, `ibm_fez`, `ibm_marrakesh`) |
| `shots` | Shots por circuito |
| `repeticoes` | Quantos jobs iguais enviar (para medir a variação do hardware entre execuções) |
| `qubits_fisicos` | Cadeia de qubits físicos a usar. `null` = escolhida automaticamente pelo transpilador para o maior GHZ |
| `tamanhos_ghz` | Tamanhos dos GHZ. O maior define o tamanho da cadeia e dos circuitos de leitura |
| `leitura` | `true` para incluir os circuitos de leitura 0 e 1 |
| `paridade` | Tamanhos e número de fases dos circuitos de paridade (ou `null`) |
| `circuito_de_ajuste` | Circuito(s) e repetição usados para **ajustar** o modelo (padrão: GHZ-5 da repetição 1). Todo o resto serve para **validar** |

Para mudar o lote, copie `lote01.json` para `lote02.json`, edite e passe `--lote lote02` aos scripts.

## Fluxo

```powershell
# 1. Ver os circuitos e o custo estimado (não envia nada)
python quantum-modeling/experimentos/05_enviar_lote.py --lote lote01

# 2. Enviar (pede confirmação; gasta cota da IBM)
python quantum-modeling/experimentos/05_enviar_lote.py --lote lote01 --enviar

# 3. Quando os jobs terminarem: baixar só as saídas para dados/lote01/saidas.json
python quantum-modeling/experimentos/06_baixar_saidas_lote.py --lote lote01

# 4. Ajustar o modelo no circuito de ajuste e aplicar aos demais (offline)
python quantum-modeling/experimentos/07_analisar_lote.py --lote lote01
```

Para testar o fluxo **sem gastar cota**, use `--teste-local` no passo 1. Ele simula o
"hardware" com o `FakeKingston` e grava em `dados/lote01_teste/`, que não vai para o git.
Os passos 3 e 4 funcionam igual com `--lote lote01_teste`.
