# Quantum Modeling

Modelagem de ruído em computadores quânticos NISQ, calibrada com jobs reais da IBM Quantum.
Parte do PIBIC (PUCPR). Responsável: João Paulo. Orientadores: Rodrigo Pasti e Jonas Krause.

**Pergunta central:** quanto um modelo de ruído local consegue reproduzir o hardware real e,
depois de ajustado (algoritmo evolutivo), quanto ele melhora em circuitos que ficaram fora do ajuste?

## Organização

```
quantum-modeling/
├── dados/            ENTRADAS — baixadas uma vez, nunca sobrescritas
│   ├── jobs_ghz.json     lista única dos jobs usados
│   ├── hardware/         por job: circuito ISA (.qpy), contagens reais e info.json (procedência)
│   └── calibracao/       snapshot de calibração de cada job + configuração do backend
├── nucleo/           código reaproveitado (só funções; nada aqui roda sozinho)
│   ├── dados_jobs.py     baixa da IBM e lê do disco
│   ├── modelos_ruido.py  Nível 0 (padrão IBM)
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
python quantum-modeling/experimentos/04_ajuste_nivel1.py # roda online (será revisado no próximo PR)
```

| Passo | O que faz | Saída |
|---|---|---|
| `01_baixar_dados.py` | Baixa circuito ISA, contagens, opções do job e a calibração do momento do job. Confere se circuito, registrador e bits batem. Pula o que já foi baixado (`--sobrescrever` para refazer). | `dados/hardware/`, `dados/calibracao/` |
| `02_nivel0.py` | Simula cada circuito com o modelo padrão da IBM montado com a calibração do dia do job e compara com o hardware. Salva após cada job; `--continuar <pasta>` retoma uma execução interrompida. Opções: `--seed`, `--tamanhos 5 10`. | `resultados/<data>_nivel0/` |
| `03_...` | *(próximo PR)* Variabilidade: simulação × simulação com várias seeds; statevector × MPS em GHZ-15 e 20. | |
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
