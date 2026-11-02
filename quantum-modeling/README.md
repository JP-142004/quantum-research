# Quantum Modeling

[Raiz do repositório](../README.md) · [Livro da mitigação](../quantum-mitigation/README.md)

**Responsável indicado no projeto:** João Paulo.

Esta frente investiga quanto um modelo de ruído consegue reproduzir distribuições medidas na IBM. A linha de base implementada é chamada “nível 0”: usa o modelo gerado a partir das propriedades do backend, sem um ajuste evolutivo adicional.

## O que está implementado

O [script de comparação](modelos/comparar_ghz_nivel0.py) contém dez IDs de jobs GHZ, de 5 a 50 qubits. Para cada um, recupera as contagens e o circuito enviado, consulta o backend, cria um modelo de ruído com `NoiseModel.from_backend`, executa uma simulação local com o mesmo número de shots e calcula a distância de Hellinger entre as distribuições.

Usa `statevector` até 20 qubits e `matrix_product_state` acima disso. O uso de MPS aproveita estrutura do circuito; não garante que qualquer circuito de cinquenta qubits seja barato. A seleção implementada é esse limiar de 20, independentemente de comentários aproximados sobre capacidade no código.

O programa consulta a IBM, mas não submete um novo job quântico. A simulação roda localmente. Ao terminar, sobrescreve [resultados_ghz_nivel0.json](resultados/resultados_ghz_nivel0.json). Se um job falhar, pode registrar um campo `erro` em vez de suas métricas.

## Distância de Hellinger

Para distribuições normalizadas p e q, a distância usada pode ser escrita como

$$H(p,q)=\sqrt{1-\sum_x\sqrt{p(x)q(x)}}.$$

Ela vai de 0 a 1: zero significa distribuições iguais e valores maiores indicam maior discrepância. Não é fidelidade do estado quântico. As contagens reais e simuladas são amostras finitas; o arquivo não traz intervalos de incerteza para essa distância.

## Resultados salvos

Os dez registros existentes usam `ibm_kingston` e 1.000 shots. Os números abaixo foram lidos do JSON, não recalculados por nova consulta à IBM.

| Qubits | Método salvo | Hellinger |
| ---: | --- | ---: |
| 5 | `statevector` | 0.1179 |
| 10 | `statevector` | 0.2395 |
| 15 | `statevector` | 0.3632 |
| 20 | `statevector` | 0.4563 |
| 25 | `matrix_product_state` | 0.5767 |
| 30 | `matrix_product_state` | 0.6974 |
| 35 | `matrix_product_state` | 0.6977 |
| 40 | `matrix_product_state` | 0.7675 |
| 45 | `matrix_product_state` | 0.8353 |
| 50 | `matrix_product_state` | 0.8597 |

## Como interpretar e o que falta

Nessa comparação, a discrepância aumenta ao longo dos tamanhos. O script consulta propriedades disponíveis quando é executado; isso não garante uma calibração contemporânea ao job histórico. Não fixa uma semente de simulação nesse código nem salva um snapshot completo do modelo. Reexecutá-lo pode produzir resultados diferentes e não reconstrói exatamente as condições antigas.

Não implementamos nesta etapa ajuste evolutivo, otimização de parâmetros de ruído ou novos modelos coerentes. O README original descrevia destinos planejados de pastas; a tabela abaixo distingue esses planos do conteúdo atual.

| Pasta | Estado e finalidade |
| --- | --- |
| [modelos](modelos/README.md) | Contém o programa de linha de base |
| [resultados](resultados/README.md) | Contém o JSON com resultados reais/simulados e distâncias |
| `calibracao` | Estrutura reservada para snapshots; não há snapshots publicados aqui |
| `hardware` | Estrutura reservada; contagens reais existentes estão dentro do JSON de resultados |
| `circuitos` | Estrutura reservada para geradores |
| `ajuste` | Estrutura reservada; não há algoritmo evolutivo implementado aqui |
| `notebooks` | Estrutura reservada; não há notebook de análise publicado aqui |

Os arquivos `.gitkeep` apenas mantêm diretórios vazios no Git. A nova validação sintética da mitigação é outro experimento e fica na outra frente; ela não atualiza ou substitui esses resultados históricos.
