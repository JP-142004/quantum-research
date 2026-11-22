# Experimento 8, parte A · Em 10 qubits, a tabela por qubit reproduz a matriz completa?

**Estado:** critérios definidos em 22 de novembro de 2026, **antes** de rodar. Os dados e os resultados são gerados depois e este arquivo é atualizado sem mudar os critérios.

**Onde e quando:** simulador local (Qiskit Aer, matriz densidade), 10 qubits em linha, 1.000 medidas por circuito. Nenhum acesso à IBM.

## Resposta curta

*A escrever depois da análise.*

## Pergunta

O [experimento 7](../../07_leitura_fatorizada/README.md) comparou em 5 qubits, com dados reais, a matriz completa e as tabelas por qubit. Aqui o erro de leitura é **escolhido por nós**, então sabemos o valor verdadeiro dos indicadores (1, porque não há erro de portas). Dois cenários:

- **`leitura`:** cada qubit erra sozinho (as chances de 0 virar 1 e de 1 virar 0 são as do [simulador](../../../mitigacao/execucao/ruido.py), as mesmas do experimento 5). É o caso em que o modelo por qubit está certo.
- **`leitura_correlacionada`:** o mesmo erro por qubit e, além disso, com chance 0,03 os dois qubits de cada par (0,1), (2,3), …, (8,9) leem errado **ao mesmo tempo**. É o caso em que o modelo por qubit está errado. O valor 0,03 foi escolhido antes de rodar, do tamanho dos erros por qubit (0,01 a 0,06). Os pares vizinhos são só uma escolha simples; o simulador não representa nenhum computador real.

## Como será feito

- **Circuitos por sessão:** GHZ conectado de 10 qubits em Z e em X, as 1.024 calibrações (`0000000000` a `1111111111`) e 4 controles independentes (zeros e uns em Z; todos em `+` e todos em `+` com o qubit 0 em `−`, em X). 1.030 circuitos × 1.000 = 1.030.000 medidas por sessão.
- **Sessões:** 3 blocos por cenário, cada um com a sua calibração e a sua semente (sementes 8001 a 8003 e 8101 a 8103; ver `experimento.py`). 6 sessões.
- **Métodos**, como no experimento 7: completo (1.024 × 1.024), fatorizado (a) (10 tabelas 2 × 2 com as 1.024 calibrações) e fatorizado (b) (só `0000000000` e `1111111111`).
- **Indicadores:** PZ e CX do GHZ ([indicadores](../../../fundamentos/indicadores.md)). Verdadeiro = 1.
- **Incerteza:** bootstrap compartilhado entre os métodos, como no experimento 7, com semente 2026 e **250 réplicas** (e não 5.000): a verificação do condicionamento de uma matriz 1.024 × 1.024 leva cerca de 0,4 s e o bootstrap completo levaria horas. Os intervalos de 95% ficam mais grosseiros que no experimento 7.
- **Verificações:** previsão da calibração com metade das medidas (semente 20261122, como no 7) e os 4 controles.
- **Valores negativos e condicionamento:** como no experimento 7 (nada é recortado; registramos a menor quasiprobabilidade, o condicionamento e as réplicas descartadas).

## Critérios, definidos antes de rodar

Mesma regra do experimento 7, sobre **fatorizado menos completo**, com intervalo de 95% e **margem ±0,02**: *equivalente* (intervalo dentro da margem), *diferente* (inteiro fora, de um lado) ou *inconclusivo*. A justificativa científica da margem continua pendente (ver o experimento 7). Cada bloco aparece separado.

Também medimos o **erro contra o valor verdadeiro** (ajustado − 1), porque aqui o 1 é conhecido.

O que cada cenário **deve** mostrar:

| Cenário | Esperado | Se não acontecer |
| --- | --- | --- |
| `leitura` | O fatorizado (a) e o completo estimam a mesma coisa, então a diferença deve ficar dentro da margem. | Não é falha do modelo: o completo estima 1.024 × 1.024 números com 1.000 medidas por coluna e pode ser mais ruidoso que o fatorizado. Reportamos o erro de cada método contra o 1 para ver quem erra mais. |
| `leitura_correlacionada` | Sem previsão de tamanho. Se o fatorizado ficar "diferente" do completo, o experimento detecta a correlação. Se continuar "equivalente", essa correlação (0,03 por par) não é detectada pelos indicadores. | Os dois resultados são informativos e entram no relatório. |

O que este experimento **não** diz: nada sobre o computador real. Só mostra o que a análise detecta quando o erro de leitura é conhecido.

## Resultado

*Gerado dos dados depois da execução.*

## Conclusão

*A escrever depois da análise.*

## Próximo passo

*Depende do resultado. A [parte B](../b_ibm/README.md) leva o modelo por qubit para a IBM.*

## Arquivos

| Arquivo | Para que serve |
| --- | --- |
| `experimento.py` | A receita: circuitos, cenários e sementes. |
| `dados/NOME_bloco_NN/` | Uma pasta por sessão: ficha, contagens e circuitos. **Não se edita.** |
| `analisar.py` | Compara os três métodos em cada sessão e grava `resultados/`. |
| `resultados/` | Tabelas, figura e `resultados.json`, gerados dos dados. |

**Execução:** simulador; não envia nada à IBM. A correlação entre qubits é aplicada às contagens depois da simulação (o simulador não tem erro de leitura entre dois qubits); ver `mitigacao/execucao/ruido.py`.

[Experimento 8](../README.md) · [Experimentos](../../README.md)
