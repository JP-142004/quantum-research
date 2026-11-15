# Quantum Modeling

Modelagem de ruído em computadores quânticos NISQ, calibrada com jobs reais da IBM Quantum.
Parte do PIBIC (PUCPR). Responsável: João Paulo. Orientadores: Rodrigo Pasti e Jonas Krause.

**Pergunta central:** quanto um modelo de ruído local consegue reproduzir o hardware real e,
depois de ajustado (algoritmo evolutivo), quanto ele melhora em circuitos que ficaram fora do ajuste?

## Organização

```
quantum-modeling/
├── circuitos/        O QUE ENVIAR à IBM: README dos circuitos + arquivo de cada lote (lote01.json)
├── dados/            O QUE VOLTOU da IBM — baixado uma vez, nunca sobrescrito
│   ├── jobs_ghz.json     lista única dos jobs usados
│   ├── hardware/         por job: circuito ISA (.qpy), contagens reais e info.json (procedência)
│   ├── calibracao/       snapshot de calibração de cada job + configuração do backend
│   └── lote01/           envio.json (job_ids), circuitos.qpy, saidas.json (só as contagens) e calibracao/
├── nucleo/           código reaproveitado (só funções; nada aqui roda sozinho)
│   ├── dados_jobs.py     baixa da IBM e lê do disco
│   ├── circuitos.py      leitura, GHZ e paridade usados nos lotes
│   ├── lotes.py          montar, transpilar, enviar e baixar lotes
│   ├── modelos_ruido.py  Nível 0 (padrão IBM) e Nível 1 (6 variáveis ajustáveis)
│   ├── simulacao.py      escolha do método e simulação com seed
│   ├── metricas.py       Hellinger, massa GHZ, P(0…0), P(1…1), peso de Hamming
│   └── registro.py       pasta por execução, versões, commit
├── experimentos/     scripts que você RODA, na ordem do número
├── resultados/       uma pasta por execução (AAAA-MM-DD_HHMM_nome/), nada é sobrescrito
└── notebooks/        análises e gráficos
```

## Como rodar

Da raiz do repositório, com o venv ativo (`.\venv\Scripts\Activate.ps1`):

```powershell
pip install -r quantum-modeling/requirements.txt        # só na primeira vez

python quantum-modeling/experimentos/01_baixar_dados.py  # precisa de internet e da conta IBM
python quantum-modeling/experimentos/02_nivel0.py        # roda offline
python quantum-modeling/experimentos/04_ajuste_nivel1.py # roda online (versão antiga do ajuste)

# Lote novo de circuitos (detalhes em circuitos/README.md)
python quantum-modeling/experimentos/05_enviar_lote.py --lote lote01            # só mostra e estima
python quantum-modeling/experimentos/05_enviar_lote.py --lote lote01 --enviar   # envia (gasta cota)
python quantum-modeling/experimentos/06_baixar_saidas_lote.py --lote lote01
python quantum-modeling/experimentos/07_analisar_lote.py --lote lote01
```

| Passo | O que faz | Saída |
|---|---|---|
| `01_baixar_dados.py` | Baixa circuito ISA, contagens, opções do job e a calibração do momento do job. Confere se circuito, registrador e bits batem. Pula o que já foi baixado (`--sobrescrever` para refazer). | `dados/hardware/`, `dados/calibracao/` |
| `02_nivel0.py` | Simula cada circuito com o modelo padrão da IBM montado com a calibração do dia do job e compara com o hardware. Salva após cada job; `--continuar <pasta>` retoma uma execução interrompida. Opções: `--seed`, `--tamanhos 5 10`. | `resultados/<data>_nivel0/` |
| `03_...` | *(próximo PR)* Variabilidade: simulação × simulação com várias seeds; statevector × MPS em GHZ-15 e 20. | |
| `05_enviar_lote.py` | Monta os circuitos de `circuitos/<lote>.json` numa cadeia fixa de qubits, mostra profundidade, nº de CZ e tempo de QPU estimado. Só envia com `--enviar` + confirmação (uma repetição por job, num `Batch`). `--teste-local` simula o hardware com o `FakeKingston`. | `dados/<lote>/envio.json`, `circuitos.qpy` |
| `06_baixar_saidas_lote.py` | Baixa os jobs que já terminaram e grava só as saídas (contagens por circuito) e a calibração de cada job. Pode rodar várias vezes. | `dados/<lote>/saidas.json` |
| `07_analisar_lote.py` | Ajusta as 6 variáveis do Nível 1 (erro 1Q, erro 2Q, leitura 1\|0, leitura 0\|1, T1, T2) no circuito de ajuste e aplica a todos os outros circuitos e repetições, comparando com o Nível 0. Mostra também a variação simulação × simulação e hardware × hardware. `--rapido` para teste. | `resultados/<data>_<lote>_analise/` |
| `04_ajuste_nivel1.py` | Evolução diferencial sobre 5 multiplicadores da calibração (erro 1Q, erro 2Q, leitura, T1, T2). Treino GHZ-5/10/15, validação GHZ-20 a 50. | `resultados/<data>_ajuste_nivel1/` |

Cada pasta de resultados tem:
- `resultados.json` — contagens reais e simuladas, Hellinger e métricas por job;
- `manifesto.json` — versões do Qiskit/Aer/Runtime, commit do git, seed, configuração do
  simulador e, por job: calibração usada (id, origem, defasagem em horas), profundidade,
  nº de portas de 2 qubits, layout, opções do job e avisos das checagens.

A credencial da IBM fica salva fora do repositório (`QiskitRuntimeService.save_account`).
Nunca coloque token ou CRN em arquivos deste repositório.

## Métodos

- **Distância de Hellinger** entre os histogramas normalizados: 0 = idênticos, 1 = sem nenhuma
  cadeia em comum. Queremos que diminua.
- **Métricas complementares** (feedback do relatório 1): massa GHZ (P(0…0) + P(1…1)), cada uma
  separadamente, distribuição do peso de Hamming e número de cadeias distintas e em comum.
- **Método de simulação:** `statevector` (trajetórias) até 20 qubits; `matrix_product_state`
  acima disso. `density_matrix` cresce em 4^n e estourou 16 GB no GHZ-15.
- **Seed fixa** no simulador (padrão 1234): a mesma configuração sempre dá o mesmo resultado.
  Atenção: o Aer usa `seed + i` no shot `i`, então seeds vizinhas repetem quase todos os shots.
  Para amostras independentes use `simulacao.seed_independente`.
- **Nível 1** (`nucleo/modelos_ruido.py`): erro uniforme em todos os qubits, a partir da média
  da calibração **só dos qubits usados**, com leitura assimétrica (P(1|0) ≠ P(0|1)), sem erro
  no `rz` (virtual no hardware) e erro de 2 qubits só no `cz`.

## Resultados até agora

Nível 0 com a calibração **atual** do backend, consultada em 21/10/2026, ou seja, posterior aos
jobs (`resultados/2026-10-21_nivel0/`):

| GHZ | 5 | 10 | 15 | 20 | 25 | 30 | 35 | 40 | 45 | 50 |
|---|---|---|---|---|---|---|---|---|---|---|
| Hellinger | 0.118 | 0.240 | 0.363 | 0.456 | 0.577 | 0.697 | 0.698 | 0.768 | 0.835 | 0.860 |

O modelo padrão superestima a massa GHZ em todos os tamanhos. No GHZ-50, "tudo 1" aparece
2 vezes no hardware e 141 na simulação. A próxima execução do `02_nivel0.py` repete a análise
com a calibração do dia de cada job.

## Limitações conhecidas

- Um job por tamanho: o efeito do tamanho se mistura a layout, profundidade, calibração e data.
- O método de simulação muda entre 20 e 25 qubits (a comparar no passo 03).
- A Hellinger com 1000 shots inclui variação de amostragem (a medir no passo 03).
- Contagens na base computacional não verificam a coerência do estado GHZ.
- O modelo ajustado (Nível 1) usa médias uniformes da calibração, não valores por qubit.

## Referências

- Georgopoulos, Emary e Zuliani (2021), *Modelling and Simulating the Noisy Behaviour of
  Near-term Quantum Computers*, Phys. Rev. A 104, 062432 — arXiv:2101.02109.
- Storn e Price (1997), *Differential Evolution*, J. Global Optimization 11(4).
