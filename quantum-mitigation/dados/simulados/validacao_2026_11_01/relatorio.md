# Validação local do protocolo de cinco qubits

**Execução:** `validacao_2026_11_01`. **Origem:** simulação clássica local em CPU, não hardware IBM.

Foram executados três blocos de 40 circuitos em cada um dos três cenários (ideal, leitura, leitura + portas) e três blocos de 42 circuitos para o piloto local de ZNE. Cada circuito recebeu 1000 shots simulados. Total: 486,000 shots simulados, separados das 102.000 medidas reais históricas.

## Modelo e verificações

O mapa sintético de cinco qubits contém as arestas [(2, 1), (2, 3), (1, 0), (3, 4)], em ambos os sentidos. Não é um snapshot atual do Fez. A base de portas é ['rz', 'sx', 'x', 'cx']; compilação nível 1, semente 42. O GHZ original permite roteamento e o conectado usa as quatro arestas diretamente. A calibração é permutada conforme o mapa físico → clássico de cada circuito antes da inversão.

O canal de leitura é independente por qubit: P(1|0) = [0.01, 0.02, 0.03, 0.04, 0.05] e P(0|1) = [0.06, 0.05, 0.04, 0.03, 0.02], na ordem física 0–4. O terceiro cenário acrescenta o canal despolarizante do Aer com parâmetro 0,02 após cada CX; esse parâmetro não é uma taxa de infidelidade de porta medida. Portas de um qubit são perfeitas no modelo. Não foram importadas calibrações reais da IBM ou modelados T1/T2, deriva e crosstalk.

Todas as distribuições ideais foram verificadas antes e depois da compilação, incluindo os controles e o dobramento ZNE. Os controles usam amostras independentes da calibração. O controle negativo tem |−〉 no qubit 0 (bit à direita). A inversão exata recupera as distribuições anteriores à leitura, inclusive após roteamento, com erro máximo inferior a 10⁻¹². O resíduo de ruído de portas permanece após essa recuperação.

As contagens foram produzidas pelo Aer em CPU com matriz densidade. A referência sem shots usa evolução por matriz densidade para as portas e aplicação analítica do canal de leitura. O bootstrap usa 2000 réplicas por bloco, uma matriz de calibração compartilhada pelos circuitos e reamostragens GHZ independentes. Sementes, versões, contagens, QPY, mapas finais e hashes estão nos registros. Os valores ± abaixo são um erro padrão.

## Comparação original versus conectado

Valores ajustados; as estimativas brutas e os intervalos percentis de 95% estão em cada arquivo `*_analise.json`. A diferença usa bootstrap compartilhando a calibração.

| Cenário | Bloco | PZ original | PZ conectado | Diferença PZ | CX original | CX conectado | Diferença CX |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| ideal | 1 | 1.0000 ± 0.0000 | 1.0000 ± 0.0000 | 0.0000 ± 0.0000 | 1.0000 ± 0.0000 | 1.0000 ± 0.0000 | -0.0000 ± 0.0000 |
| ideal | 2 | 1.0000 ± 0.0000 | 1.0000 ± 0.0000 | 0.0000 ± 0.0000 | 1.0000 ± 0.0000 | 1.0000 ± 0.0000 | 0.0000 ± 0.0000 |
| ideal | 3 | 1.0000 ± 0.0000 | 1.0000 ± 0.0000 | 0.0000 ± 0.0000 | 1.0000 ± 0.0000 | 1.0000 ± 0.0000 | 0.0000 ± 0.0000 |
| leitura | 1 | 0.9773 ± 0.0177 | 1.0135 ± 0.0175 | 0.0362 ± 0.0201 | 1.0277 ± 0.0335 | 0.9940 ± 0.0340 | -0.0337 ± 0.0463 |
| leitura | 2 | 0.9936 ± 0.0190 | 1.0353 ± 0.0179 | 0.0417 ± 0.0209 | 0.9988 ± 0.0342 | 1.0637 ± 0.0325 | 0.0649 ± 0.0456 |
| leitura | 3 | 0.9988 ± 0.0177 | 0.9988 ± 0.0182 | -0.0001 ± 0.0206 | 0.9519 ± 0.0347 | 0.9819 ± 0.0344 | 0.0299 ± 0.0468 |
| leitura_e_portas | 1 | 0.8408 ± 0.0195 | 0.9290 ± 0.0190 | 0.0882 ± 0.0245 | 0.7762 ± 0.0399 | 0.9116 ± 0.0367 | 0.1353 ± 0.0543 |
| leitura_e_portas | 2 | 0.8491 ± 0.0204 | 0.9655 ± 0.0191 | 0.1164 ± 0.0244 | 0.8202 ± 0.0391 | 0.9290 ± 0.0358 | 0.1088 ± 0.0526 |
| leitura_e_portas | 3 | 0.8404 ± 0.0202 | 0.9507 ± 0.0191 | 0.1103 ± 0.0243 | 0.7097 ± 0.0390 | 0.9601 ± 0.0350 | 0.2505 ± 0.0509 |

## Controles independentes

Valores ajustados. Os alvos são 1 para os três primeiros controles e −1 para o último. Desvios em amostras finitas são registrados, sem selecionar apenas blocos favoráveis.

| Cenário/protocolo | Bloco | 00000 em Z | 11111 em Z | +++++ em X | ++++− em X |
| --- | ---: | ---: | ---: | ---: | ---: |
| ideal/comparacao | 1 | 1.0000 ± 0.0000 | 1.0000 ± 0.0000 | 1.0000 ± 0.0000 | -1.0000 ± 0.0000 |
| ideal/comparacao | 2 | 1.0000 ± 0.0000 | 1.0000 ± 0.0000 | 1.0000 ± 0.0000 | -1.0000 ± 0.0000 |
| ideal/comparacao | 3 | 1.0000 ± 0.0000 | 1.0000 ± 0.0000 | 1.0000 ± 0.0000 | -1.0000 ± 0.0000 |
| leitura/comparacao | 1 | 1.0051 ± 0.0194 | 1.0078 ± 0.0220 | 1.0128 ± 0.0424 | -0.9933 ± 0.0464 |
| leitura/comparacao | 2 | 0.9953 ± 0.0191 | 1.0073 ± 0.0234 | 0.9739 ± 0.0412 | -1.0308 ± 0.0503 |
| leitura/comparacao | 3 | 1.0002 ± 0.0207 | 0.9881 ± 0.0216 | 1.0283 ± 0.0448 | -0.9623 ± 0.0461 |
| leitura_e_portas/comparacao | 1 | 0.9785 ± 0.0178 | 1.0364 ± 0.0237 | 0.9844 ± 0.0397 | -0.9598 ± 0.0498 |
| leitura_e_portas/comparacao | 2 | 1.0178 ± 0.0191 | 1.0076 ± 0.0237 | 0.9992 ± 0.0429 | -1.0145 ± 0.0495 |
| leitura_e_portas/comparacao | 3 | 1.0198 ± 0.0199 | 0.9930 ± 0.0223 | 1.0495 ± 0.0428 | -0.9234 ± 0.0483 |
| leitura_e_portas/zne | 1 | 0.9857 ± 0.0185 | 1.0468 ± 0.0234 | 0.9631 ± 0.0399 | -0.9521 ± 0.0456 |
| leitura_e_portas/zne | 2 | 0.9836 ± 0.0177 | 0.9683 ± 0.0194 | 0.9249 ± 0.0409 | -1.0066 ± 0.0487 |
| leitura_e_portas/zne | 3 | 1.0332 ± 0.0193 | 1.0124 ± 0.0225 | 0.9983 ± 0.0435 | -0.9813 ± 0.0506 |

## Referências exatas do modelo

Sem erro de shots. Estes valores permitem separar o ruído de portas do ruído de leitura dentro do modelo escolhido.

| Cenário | Construção | PZ antes da leitura | PZ observado | CX antes da leitura | CX observado |
| --- | --- | ---: | ---: | ---: | ---: |
| ideal | original | 1.000000 | 1.000000 | 1.000000 | 1.000000 |
| ideal | conectado | 1.000000 | 1.000000 | 1.000000 | 1.000000 |
| leitura | original | 1.000000 | 0.836604 | 1.000000 | 0.695688 |
| leitura | conectado | 1.000000 | 0.836604 | 1.000000 | 0.695688 |
| leitura_e_portas | original | 0.840887 | 0.706524 | 0.769022 | 0.535000 |
| leitura_e_portas | conectado | 0.946261 | 0.792424 | 0.922368 | 0.641681 |

## Piloto local de ZNE

Usamos dobramento global U(U†U)^k na preparação conectada, fatores 1, 3 e 5. Barreiras preservam os blocos durante a compilação; foram conferidas 4, 12 e 20 CX, respectivamente. As rotações finais de X e a leitura não são dobradas. O ajuste principal é uma reta por mínimos quadrados ordinários em função do fator nominal, extrapolada a zero, após mitigação de leitura. O bootstrap propaga a calibração compartilhada e as contagens de todos os fatores. Valores fora do intervalo físico não são recortados.

| Bloco | Base | Leitura ajustada, fator 1 | ZNE linear | ZNE − fator 1 |
| --- | --- | ---: | ---: | ---: |
| 1 | Z | 0.9639 ± 0.0188 | 1.0072 ± 0.0226 | 0.0432 ± 0.0098 |
| 1 | X | 0.9190 ± 0.0351 | 0.9532 ± 0.0434 | 0.0342 ± 0.0211 |
| 2 | Z | 0.8868 ± 0.0185 | 0.9135 ± 0.0218 | 0.0267 ± 0.0094 |
| 2 | X | 0.9579 ± 0.0353 | 1.0582 ± 0.0435 | 0.1003 ± 0.0212 |
| 3 | Z | 0.9763 ± 0.0188 | 1.0065 ± 0.0224 | 0.0302 ± 0.0098 |
| 3 | X | 0.8914 ± 0.0375 | 0.9283 ± 0.0455 | 0.0369 ± 0.0210 |

A sensibilidade à faixa de fatores pode ser examinada sem shots no modelo:

| Base | Fator 1 | Fator 3 | Fator 5 | Intercepto linear 1,3,5 | Intercepto linear 1,3 |
| --- | ---: | ---: | ---: | ---: | ---: |
| Z | 0.946261 | 0.848950 | 0.763687 | 0.989897 | 0.994917 |
| X | 0.922368 | 0.784717 | 0.667608 | 0.982634 | 0.991194 |

## Conclusão e próximo passo

A validação verifica a lógica do protocolo e o tratamento do roteamento em um modelo controlado. A leitura pode ser invertida, mas o ruído das portas permanece; ZNE é uma extrapolação com viés de modelo e custo de variância, não garantia de recuperação exata. Resultados com mais de 1 ou abaixo de −1 são possíveis para os estimadores não restringidos.

Os três blocos de cada cenário mudam a semente de amostragem, não o equipamento ou o modelo: não representam deriva temporal real. O mapa, portas e ruídos sintéticos não permitem prever numericamente o próximo resultado no Fez. O próximo passo experimental continua sendo discutir os controles e preparar uma compilação específica para um backend disponível; nenhuma submissão é feita por estes scripts.

## Reprodução

```powershell
python -m venv .venv-simulacao
.venv-simulacao/Scripts/python -m pip install -r quantum-mitigation/requirements-simulacao.txt
.venv-simulacao/Scripts/python -m unittest discover -s quantum-mitigation/tests -v
.venv-simulacao/Scripts/python quantum-mitigation/scripts/validar_protocolo_local.py --execucao minha_validacao
```

O comando recusa reutilizar uma pasta existente. Para uma repetição, escolher outro nome. Os parâmetros padrão são três blocos, 1.000 shots e 2.000 réplicas bootstrap. A execução registrada levou 126.2 segundos para simulação e análise neste PC; não é uma previsão de tempo de QPU. O teste usa no máximo quatro threads de CPU, não utiliza a GPU nem lê credenciais.

Referências de implementação: [AerSimulator](https://qiskit.github.io/qiskit-aer/stubs/qiskit_aer.AerSimulator.html), [ReadoutError](https://qiskit.github.io/qiskit-aer/stubs/qiskit_aer.noise.ReadoutError.html), [canal despolarizante](https://qiskit.github.io/qiskit-aer/stubs/qiskit_aer.noise.depolarizing_error.html). As versões efetivamente usadas estão no manifesto; a documentação online pode descrever versão posterior.
