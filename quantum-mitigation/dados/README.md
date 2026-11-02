# Dados

Aqui estão os dados da pesquisa, sem análise. A interpretação de cada experimento está no relatório dele, em [experimentos](../experimentos/README.md). As figuras feitas a partir destes dados estão em [figuras](../figuras/README.md).

Os dados são de três tipos, e cada tipo tem uma pasta:

| Pasta | O que tem | Como foi obtido |
| --- | --- | --- |
| `brutos` ([ver](#dados-brutos-ibm)) | Contagens e circuitos compilados. | Circuitos executados em computadores quânticos da IBM. Cada execução devolve quantas vezes cada sequência de bits apareceu. |
| `processados` ([ver](#dados-processados)) | Indicadores calculados (PZ, CX), ajustes de leitura e incertezas. | Scripts locais leem os dados brutos e fazem as contas. |
| `simulados` ([ver](#dados-simulados)) | Contagens e análises de simulações. | Simulador no PC, com ruído sintético escolhido por nós. |

## Onde estão os dados de cada experimento

| Experimento | Brutos (IBM) | Processados | Simulados |
| --- | --- | --- | --- |
| [1. Escala do GHZ](../experimentos/01_ghz_escala/README.md) | `brutos/01_ghz_escala` | `processados/01_ghz_escala` | — |
| [2. Controles](../experimentos/02_controles/README.md) | `brutos/02_controles` | `processados/02_controles` | — |
| [3. Construção com menos portas](../experimentos/03_ghz_conectado/README.md) | `brutos/03_ghz_conectado` | `processados/03_ghz_conectado` | — |
| [4. Calibração de leitura](../experimentos/04_mitigacao_leitura/README.md) | `brutos/04_mitigacao_leitura` | `processados/04_mitigacao_leitura` | — |
| [5. Validação simulada](../experimentos/05_validacao_simulada/README.md) | — | — | `simulados/validacao_2026_11_01` |
| [6. ZNE simulada](../experimentos/06_zne_simulado/README.md) | — | — | `simulados/validacao_2026_11_01` |

**Regra:** `brutos` e `simulados` são o registro original e não se editam. Os processados e as figuras podem ser refeitos pelos [scripts](../scripts/README.md).

**Novo experimento:** crie a pasta com o mesmo número do experimento (por exemplo `brutos/07_nome_curto`) e acrescente uma linha na tabela acima.

---

## Dados brutos (IBM)

Contagens medidas em computadores quânticos da IBM, como foram devolvidas. Cada arquivo `.json` guarda as contagens de um job (uma execução na IBM); o `.qpy` de mesmo nome guarda os circuitos compilados desse job, na ordem dos índices do JSON. O nome do arquivo é o identificador do job.

### 01 · Escala do GHZ

| Arquivo | O que é |
| --- | --- |
| `brutos/01_ghz_escala/ghz_05_a_50.txt` | Contagens por sequência de bits, em dez seções (5, 10, … 50 qubits), 1.000 medidas cada. Backend e data não foram registrados. |

Figura: [01_escala_observada](../figuras/01_escala_observada.png). Tabela calculada: [resumo_escala.csv](processados/01_ghz_escala/resumo_escala.csv).

### 02 · Controles de estados conhecidos

Recuperados da IBM em 2 de novembro de 2026.

| Job | Circuitos | Backend |
| --- | --- | --- |
| `brutos/02_controles/dbbrrnpgv2cc73e922r0` | todos zeros | ibm_kingston |
| `brutos/02_controles/dbbsd47i0auc73948300` | todos uns | ibm_kingston |
| `brutos/02_controles/dbcbsopgv2cc73ea1300` | qubits individuais | ibm_kingston |
| `brutos/02_controles/dbcc4g9gv2cc73ea1j10` | qubits individuais | ibm_fez |
| `brutos/02_controles/dbcc5ggc77vs7385vfsg` | zeros medidos separados e juntos | ibm_fez |

Figura: [02_controles_reais](../figuras/02_controles_reais.png).

### 03 · Construções do GHZ

Recuperados da IBM em 2 de novembro de 2026. Todos no ibm_fez.

| Job | Circuitos |
| --- | --- |
| `brutos/03_ghz_conectado/dbccaqpgv2cc73ea21fg` | GHZ original de 5 qubits |
| `brutos/03_ghz_conectado/dbcccpc24mrc73cjb6bg` | original e conectado, medidos em Z |
| `brutos/03_ghz_conectado/dbcco2fi0auc73dum8i0` | original e conectado, medidos em X |
| `brutos/03_ghz_conectado/dbch2kpgv2cc73eabim0` | GHZ conectado de 50 qubits |

Figura: [03_construcoes_reais](../figuras/03_construcoes_reais.png).

### 04 · Calibração de leitura

Cada rodada tem 34 circuitos (32 de calibração, mais o GHZ em Z e em X), 1.000 medidas por circuito, no ibm_fez. A tabela mostra as contagens do GHZ.

| Rodada | Arquivo | Z: 00000 | Z: 11111 | Z: outros | X: par | X: ímpar |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| 1 | `brutos/04_mitigacao_leitura/GHZ_leitura_dbccq67i0auc73dumdk0.json` | 439 | 434 | 127 | 898 | 102 |
| 2 | `brutos/04_mitigacao_leitura/GHZ_leitura_dbccri9gv2cc73ea3630.json` | 445 | 419 | 136 | 898 | 102 |
| 3 | `brutos/04_mitigacao_leitura/rodada_03/rodada_03.json` (+ `.qpy`) | 454 | 441 | 105 | 903 | 97 |

Em X, "par" e "ímpar" contam as sequências com número par ou ímpar de bits 1. A rodada 3 (job `dbjnndgnceqs73akbkh0`) é a única com os circuitos salvos em QPY; sua pasta se chamava `repeticoes` e foi renomeada.

Figura: [04_comparacao_rodadas](../figuras/04_comparacao_rodadas.png).

---

## Dados processados

Resultados calculados localmente a partir dos [dados brutos](#dados-brutos-ibm), sem acessar a IBM. Cada experimento tem sua pasta, com o mesmo número. Os arquivos são refeitos pelos [scripts](../scripts/README.md).

| Pasta | Arquivo | O que tem | Feito por |
| --- | --- | --- | --- |
| `01_ghz_escala` | `resumo_escala.csv` | Uma linha por tamanho de circuito (5 a 50 qubits): medidas, todos zeros, todos uns, outros e PZ. | `resumir_resultados.py` |
| `02_controles` | `resultados_recuperados.json` | Uma linha por circuito: job, backend, contagens resumidas, indicadores e custo compilado. | Recuperação da IBM |
| `03_ghz_conectado` | `resultados_recuperados.json` | Idem, para as construções do GHZ. | Recuperação da IBM |
| `04_mitigacao_leitura` | `comparacao_rodadas.json` | As três rodadas com valores brutos e ajustados, erros padrão, ganhos, intervalos de 95%, condicionamento da matriz de calibração, menor quasiprobabilidade e hashes dos arquivos de origem. | `comparar_rodadas.py` |

Relatório completo das rodadas, gerado a partir de `comparacao_rodadas.json`: [docs/comparacao_rodadas.md](../docs/comparacao_rodadas.md).

---

## Dados simulados

Resultados de simulações no PC (Qiskit Aer), com ruído sintético escolhido por nós. Como o ruído é conhecido, dá para comparar o que a técnica estima com o valor exato do modelo. Os valores **não** valem para o hardware da IBM.

Existe uma única execução, `simulados/validacao_2026_11_01` (1º de novembro de 2026), e todos os arquivos ficam na mesma pasta porque o manifesto, o auditor e os scripts usam esses caminhos. Cada circuito foi simulado com 1.000 medidas.

### Achar um resultado

Cada **bloco** é uma repetição independente: tem sementes próprias e a sua própria calibração de leitura. Cada célula abre os dados (contagens) e os indicadores calculados (análise) daquele bloco.

| Cenário | Experimento | Bloco 1 | Bloco 2 | Bloco 3 |
| --- | --- | --- | --- | --- |
| Ideal (sem ruído) | [5](../experimentos/05_validacao_simulada/README.md) | [contagens](simulados/validacao_2026_11_01/comparacao_ideal_bloco_01_contagens.json) · [análise](simulados/validacao_2026_11_01/comparacao_ideal_bloco_01_analise.json) | [contagens](simulados/validacao_2026_11_01/comparacao_ideal_bloco_02_contagens.json) · [análise](simulados/validacao_2026_11_01/comparacao_ideal_bloco_02_analise.json) | [contagens](simulados/validacao_2026_11_01/comparacao_ideal_bloco_03_contagens.json) · [análise](simulados/validacao_2026_11_01/comparacao_ideal_bloco_03_analise.json) |
| Só erro de leitura | [5](../experimentos/05_validacao_simulada/README.md) | [contagens](simulados/validacao_2026_11_01/comparacao_leitura_bloco_01_contagens.json) · [análise](simulados/validacao_2026_11_01/comparacao_leitura_bloco_01_analise.json) | [contagens](simulados/validacao_2026_11_01/comparacao_leitura_bloco_02_contagens.json) · [análise](simulados/validacao_2026_11_01/comparacao_leitura_bloco_02_analise.json) | [contagens](simulados/validacao_2026_11_01/comparacao_leitura_bloco_03_contagens.json) · [análise](simulados/validacao_2026_11_01/comparacao_leitura_bloco_03_analise.json) |
| Leitura e portas | [5](../experimentos/05_validacao_simulada/README.md) | [contagens](simulados/validacao_2026_11_01/comparacao_leitura_e_portas_bloco_01_contagens.json) · [análise](simulados/validacao_2026_11_01/comparacao_leitura_e_portas_bloco_01_analise.json) | [contagens](simulados/validacao_2026_11_01/comparacao_leitura_e_portas_bloco_02_contagens.json) · [análise](simulados/validacao_2026_11_01/comparacao_leitura_e_portas_bloco_02_analise.json) | [contagens](simulados/validacao_2026_11_01/comparacao_leitura_e_portas_bloco_03_contagens.json) · [análise](simulados/validacao_2026_11_01/comparacao_leitura_e_portas_bloco_03_analise.json) |
| ZNE (leitura e portas, fatores 1, 3 e 5) | [6](../experimentos/06_zne_simulado/README.md) | [contagens](simulados/validacao_2026_11_01/zne_leitura_e_portas_bloco_01_contagens.json) · [análise](simulados/validacao_2026_11_01/zne_leitura_e_portas_bloco_01_analise.json) | [contagens](simulados/validacao_2026_11_01/zne_leitura_e_portas_bloco_02_contagens.json) · [análise](simulados/validacao_2026_11_01/zne_leitura_e_portas_bloco_02_analise.json) | [contagens](simulados/validacao_2026_11_01/zne_leitura_e_portas_bloco_03_contagens.json) · [análise](simulados/validacao_2026_11_01/zne_leitura_e_portas_bloco_03_analise.json) |

Figuras: [ideal](../figuras/05_simulacao_ideal.png), [leitura](../figuras/05_simulacao_leitura.png), [leitura e portas](../figuras/05_simulacao_leitura_e_portas.png), [controles](../figuras/05_controles_simulados.png) (experimento 5); [blocos de ZNE](../figuras/06_zne_blocos.png) e [fatores](../figuras/06_zne_fatores.png) (experimento 6).

### Como ler o nome de um arquivo

`comparacao_leitura_e_portas_bloco_02_analise.json` se divide em quatro partes:

| Parte | Significado |
| --- | --- |
| `comparacao` ou `zne` | Qual experimento: `comparacao` é o 5 (GHZ original contra conectado); `zne` é o 6. |
| `ideal`, `leitura`, `leitura_e_portas` | O cenário de ruído simulado. O ZNE só foi feito em `leitura_e_portas`. |
| `bloco_01` a `bloco_03` | A repetição. Cada bloco tem a sua calibração. |
| `_contagens` ou `_analise` | `_contagens`: quantas vezes cada sequência de bits apareceu em cada circuito. `_analise`: indicadores brutos e ajustados, erros padrão, ganhos e intervalos, calculados dessas contagens. |

Os quatro **controles** (todos zeros, todos uns, paridade positiva e negativa) não têm arquivo próprio: estão dentro de cada `_analise`. Um bloco de comparação tem 40 circuitos (32 de calibração, 4 GHZ e 4 controles) e um bloco de ZNE tem 42 (32 de calibração, 6 GHZ e 4 controles).

### Registro da execução

Estes cinco arquivos descrevem a execução inteira, não um bloco.

| Arquivo | O que tem |
| --- | --- |
| `manifesto.json` | Origem, modelo de ruído, sementes, versões, referências exatas do modelo e o hash de cada arquivo. |
| `verificacao.json` | Resultado da auditoria de integridade e consistência (`scripts/verificar_registro_local.py`). |
| `relatorio.md` | Todos os valores desta execução, em texto. |
| `comparacao.qpy` | 40 circuitos compilados da comparação, para o experimento 5. |
| `zne.qpy` | 42 circuitos compilados do ZNE, para o experimento 6. |

Pasta da execução: [validacao_2026_11_01](simulados/validacao_2026_11_01/relatorio.md).

---

## Registro de origem

O arquivo [registro_origem.json](registro_origem.json) guarda, em duas partes, de onde vieram os dados:

- `inventario_importacao`: os 23 arquivos copiados do OneDrive na organização inicial, com o hash de origem e de destino e os ajustes feitos (por exemplo, a remoção de uma linha de configuração que continha credencial).
- `recuperacao_etapas_02_03`: os 9 jobs recuperados da conta IBM em 2 de novembro de 2026 e a verificação de cada circuito contra a preparação esperada.
