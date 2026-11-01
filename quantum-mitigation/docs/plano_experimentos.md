# Próximos experimentos — protocolo proposto

Plano de 1 de novembro de 2026, baseado nas três rodadas concluídas. Este arquivo não envia jobs e não representa experimento já executado. O job `dbjnndgnceqs73akbkh0` está encerrado e não deve ser reenviado.

## 1. Validação local antes de usar hardware

Construir um novo protocolo separado dos scripts históricos. Conferir por simulação ideal o GHZ original e o conectado nas bases Z e X, além dos controles abaixo. Fixar qubits físicos, sementes, layout e opções; registrar versões e circuitos compilados em QPY. Para a construção original, permitir o roteamento necessário, verificar o mapeamento final e interpretar os bits de acordo com ele. Para a conectada, conferir as quatro conexões esperadas.

Guardar número de operações de dois qubits, profundidade e duração compilada quando disponível. O objetivo é comparar o custo efetivo das construções no mesmo dispositivo. Disponibilidade, conectividade e propriedades atuais do backend precisam ser conferidas quando houver decisão de executar; não pressupomos que o Fez terá a mesma configuração futura.

Verificar o pipeline estatístico com dados sintéticos de identidade e de um canal de leitura conhecido. O teste deve recuperar indicadores ideais sem ruído e reproduzir o efeito do canal dentro do erro de amostragem. O programa de envio futuro deve separar preparação, submissão e coleta e recusar números de rodada já registrados.

## 2. Prioridade: construção do GHZ com controles independentes

**Pergunta:** sob condições comparáveis, quanto a construção conectada melhora PZ e CX, antes e depois da mitigação? A calibração prevê adequadamente resultados de controle que não foram usados para estimá-la?

Proposta: três blocos, cada um com sua própria calibração e 1.000 shots por circuito. Usar os mesmos cinco qubits em cada bloco; se indisponíveis, registrar a mudança como outro protocolo. Distribuir os blocos em janelas distintas, registrando horários reais e dados de calibração disponíveis. Três blocos constituem piloto, não uma caracterização definitiva da deriva.

| Componente por bloco | Circuitos | Medidas | Objetivo |
| --- | ---: | ---: | --- |
| Estados de calibração de 00000 a 11111 | 32 | 32.000 | Estimar A para esse bloco |
| GHZ original em Z e X | 2 | 2.000 | Referência com roteamento |
| GHZ conectado em Z e X | 2 | 2.000 | Comparação de construção |
| Repetições independentes de 00000 e 11111 | 2 | 2.000 | Validar previsão em Z sem reutilizar contagens de calibração |
| Estados +++++ e −++++, medidos em X | 2 | 2.000 | Controles de paridade +1 e −1 |
| **Total por bloco** | **40** | **40.000** | |
| **Total de três blocos** | **120** | **120.000** | |

Em −++++, definir explicitamente qual qubit recebe |−〉 e respeitar a ordem dos bits. Esses controles também incluem portas de preparação e mudança de base: não isolam perfeitamente o erro de leitura. Seus dados devem ser amostras novas, distintas das colunas usadas para ajustar A.

Manter DD e twirling desativados na comparação inicial, registrar opções efetivas e embaralhar a lista com semente salva. Embaralhar a lista não garante a ordem física no serviço. Não estimar tempo de QPU a partir do número de shots; usar o circuito compilado e os recursos disponíveis para avaliar o orçamento antes da execução.

### Análise e critérios definidos antes da coleta

- Apresentar PZ e CX brutos e ajustados por construção e bloco, com EP e intervalos do ganho. Não combinar calibrações de blocos distintos.
- Calcular conectado − original usando bootstrap com uma mesma matriz de calibração reamostrada por bloco, preservando a dependência dos dois estimadores; as amostras GHZ das duas construções são reamostradas separadamente.
- Informar condição de A, resíduo da inversão, normalização e menores quasiprobabilidades. Uma condição acima de 100 interrompe a inversão segundo a regra já adotada no projeto; esse limiar é operacional e não valida a física do modelo.
- Nos controles, comparar o valor ideal conhecido e o ajustado com intervalos bootstrap. Desvios persistentes ou de mesmo sinal em blocos distintos motivam investigar preparação, mudança de base e deriva antes de atribuir a melhora à leitura. Não exigir que todos os intervalos de 95% incluam o ideal, pois haverá múltiplas comparações.
- Relatar todos os blocos, inclusive os sem melhora. Separar análise descritiva de inferência confirmatória; se houver testes formais múltiplos, definir previamente a família e o ajuste.
- Só interpretar a construção como vantajosa quando os ganhos e as contagens de portas/profundidade forem consistentes; incerteza grande ou sinais divergentes levam a resultado inconclusivo, não à seleção da melhor rodada.

## 3. Segunda prioridade: piloto de ZNE

Prosseguir após conferir os controles e a implementação local. A extrapolação a ruído zero usa circuitos equivalentes com níveis distintos de ruído; a base conceitual é apresentada por [Temme, Bravyi e Gambetta](https://arxiv.org/abs/1612.02058). O uso de dobramento unitário para ampliar o ruído é discutido por [Giurgica-Tiron e colaboradores](https://arxiv.org/abs/2005.10921).

Proposta inicial: GHZ conectado em Z e X, fatores nominais de dobramento 1, 3 e 5. Definir o dobramento no bloco unitário de preparação; não dobrar medições ou reset. Verificar equivalência ideal antes da execução e conferir que a compilação não cancelou as portas extras. Os fatores nominais não são medidas exatas da intensidade física de ruído.

Por bloco: 32 circuitos de calibração + 6 circuitos GHZ + os mesmos 4 controles = 42 circuitos. Com 1.000 shots, são 42.000 medidas; um piloto de três blocos seria 126.000 medidas adicionais. Este orçamento é separado da etapa anterior e não está agendado.

Comparar, nos mesmos dados, bruto, mitigação de leitura e mitigação de leitura seguida de ZNE. Pré-definir ajuste linear como análise principal e avaliar a sensibilidade à faixa de fatores; um polinômio quadrático em três pontos interpola sem deixar graus de liberdade para avaliar qualidade de ajuste, portanto não é validação suficiente. Reamostrar calibração e todos os fatores conjuntamente para propagar incerteza à extrapolação.

O piloto é informativo mesmo sem ganho. Não recortar valores extrapolados para o intervalo físico nem selecionar o ajuste que chega mais perto de 1. Se o ruído não variar de forma interpretável, a compilação cancelar o dobramento ou a incerteza dominar o ganho, revisar o protocolo antes de ampliar shots.

## 4. Expansão do número de qubits

Não estender diretamente a calibração completa a 50 qubits: ela exige 2^n circuitos de calibração e uma matriz de dimensão 2^n × 2^n. Para 10 qubits, já seriam 1.024 circuitos só de calibração. Antes de ampliar, comparar em cinco qubits um modelo fatorizado ou outro método escalável com a matriz completa, verificando hipóteses de correlação. O [tutorial da IBM sobre M3](https://quantum.cloud.ibm.com/docs/en/tutorials/readout-error-mitigation-sampler) oferece uma referência para essa avaliação futura.

## Entregáveis de cada rodada futura

Preservar contagens originais, IDs, timestamps, qubits, shots, ordem de circuitos, sementes, opções, versões, QPY e metadados de compilação. Salvar a análise em arquivos derivados, sem substituir o registro bruto. Registrar execuções malsucedidas e os motivos de exclusão, se houver, sem reenviar automaticamente.

**Próxima decisão de pesquisa:** discutir o protocolo de 120.000 medidas com o orientador; implementar e validar sua versão local antes de qualquer submissão. Este plano não contém comandos que enviem circuitos.

## Atualização: validação local realizada

Em 1 de novembro de 2026, a comparação de construções, os controles e um piloto de ZNE foram implementados e executados em simulador local. Consulte o [registro de trabalho](registro_trabalho.md) e o [relatório da simulação](../dados/simulados/validacao_2026_11_01/relatorio.md). Os seis testes automatizados e a auditoria dos registros passaram. Isso conclui a validação em mapa e ruídos sintéticos; a compilação específica para um backend real e a execução no hardware continuam como etapas futuras. As contagens simuladas não foram misturadas com as três rodadas reais.
