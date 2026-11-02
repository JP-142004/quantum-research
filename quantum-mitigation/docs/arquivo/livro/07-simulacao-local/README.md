# 07. Validação no computador local

[← Anterior](../06-estatistica/README.md) · [Índice do livro](../../../../README.md) · [Próximo →](../08-zne/README.md)

## Por que simular antes de usar o hardware

No simulador podemos escolher um canal conhecido e comparar o resultado calculado com uma referência exata. Isso ajuda a detectar erros de circuito, inversão, convenção de bits e cálculo estatístico. Um modelo controlado é apropriado para validar a implementação; não substitui a observação do equipamento real.

A execução `validacao_2026_11_01` foi feita no PC com Qiskit Aer em CPU, usando no máximo quatro threads. Foram aproximadamente 126 segundos de simulação e análise. A GPU não foi utilizada. As versões registradas são Python 3.12.10, NumPy 2.5.4, Qiskit 2.6.0 e Aer 0.17.2.

## O protocolo de comparação

| Componente por bloco | Circuitos | Shots |
| --- | ---: | ---: |
| Calibração de cinco qubits | 32 | 32.000 |
| GHZ original em Z/X | 2 | 2.000 |
| GHZ conectado em Z/X | 2 | 2.000 |
| Controles independentes | 4 | 4.000 |
| Total | 40 | 40.000 |

O mapa sintético tem as arestas (2,1), (2,3), (1,0), (3,4), nos dois sentidos. A base de compilação é `rz`, `sx`, `x`, `cx`, com otimização nível 1, roteamento SABRE e semente 42. A versão original pode usar roteamento; a conectada deve conservar quatro CX. Não consultamos a conectividade atual da IBM para gerar esse mapa.

## Três cenários

| Cenário | Leitura | Portas |
| --- | --- | --- |
| `ideal` | Perfeita | Perfeitas |
| `leitura` | Canal independente e assimétrico por qubit | Perfeitas |
| `leitura_e_portas` | Mesmo canal de leitura | Despolarização após cada CX |

Na ordem dos qubits físicos 0–4, P(1|0) é `[0.01, 0.02, 0.03, 0.04, 0.05]` e P(0|1) é `[0.06, 0.05, 0.04, 0.03, 0.02]`. Esses valores foram escolhidos para testar o código; não são estimativas do Fez.

O canal despolarizante de dois qubits usa parâmetro $\lambda=0,02$, com ação local $\mathcal{E}(\rho)=(1-\lambda)\rho+\lambda I/4$ sobre um estado de dois qubits. Em um sistema maior, o canal atua no par correspondente. Esse parâmetro não é diretamente uma taxa de infidelidade experimental. A [referência do Aer](https://qiskit.github.io/qiskit-aer/stubs/qiskit_aer.noise.depolarizing_error.html) define sua convenção.

Portas de um qubit são perfeitas nesses cenários; não incluímos tempos T1/T2, ruído de espera, crosstalk ou deriva. Em particular, os controles sem CX não recebem o canal de erro de portas escolhido.

## Duas formas de calcular para comparar

O simulador gera contagens finitas com leitura e ruído de portas. Separadamente, uma evolução por matriz densidade sem amostragem produz a distribuição anterior à leitura; aplicamos analiticamente o canal conhecido para obter a distribuição observada de referência. A inversão exata deve recuperar a distribuição anterior à leitura, não necessariamente a ideal.

| Cenário com leitura + portas | PZ antes da leitura | CX antes da leitura |
| --- | ---: | ---: |
| GHZ original | 0,840887 | 0,769022 |
| GHZ conectado | 0,946261 | 0,922368 |

Esses são valores exatos do **modelo sintético**. A construção conectada fica melhor nesse modelo por usar menos portas ruidosas. Isso não autoriza prever os mesmos valores em um processador real.

## Volume e resultados registrados

Foram três blocos por cenário: 9 × 40 × 1.000 = 360.000 shots na comparação. O piloto ZNE adiciona 126.000, totalizando 486.000 shots simulados. Entre blocos de um cenário mudam as sementes, não as propriedades do modelo. Não são três dias diferentes de hardware.

As contagens e análises estão em [dados/simulados](../../../../dados/simulados/README.md), com um [relatório completo](../../../../dados/simulados/validacao_2026_11_01/relatorio.md). O manifesto registra opções, mapas de medida, portas, sementes, versões e tempo de execução. Duração física de circuitos é `null`, pois não há durações no mapa sintético.

## Verificações realizadas

Os seis testes verificam distribuições ideais lógicas e compiladas, controle negativo, canal assimétrico e permutação de bits, convenção de leitura do Aer, rejeição de contagens inválidas/matriz singular e extrapolação linear/identidade. A auditoria conferiu 26 hashes, dois QPY e os totais dos 12 blocos. O maior desvio de uma métrica bruta em relação ao modelo foi 2,14 EP; para ajustadas, 3,22 EP. O limite amplo de sanidade era 6 EP, não um teste confirmatório de cobertura.

O resultado é uma validação operacional e numérica para esses casos. Não é prova de ausência de bugs em todos os circuitos possíveis, nem validação do modelo contra o Fez.

---

[← Anterior](../06-estatistica/README.md) · [Índice do livro](../../../../README.md) · [Próximo →](../08-zne/README.md)
