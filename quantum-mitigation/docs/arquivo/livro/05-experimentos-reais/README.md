# 05. Experimentos e resultados reais

> Atualização de 2 de novembro de 2026: as contagens e os circuitos históricos das [etapas 2](../../../../dados/brutos/02_controles/README.md) e [3](../../../../dados/brutos/03_ghz_conectado/README.md) foram recuperados diretamente da IBM. Referências abaixo à ausência desses arquivos descrevem o estado anterior da importação.

[← Anterior](../04-mitigacao-leitura/README.md) · [Índice do livro](../../../../README.md) · [Próximo →](../06-estatistica/README.md)

## Importação e preservação

Foram organizados 23 arquivos históricos da pasta “Mitigaçao de ruido”. Dezenove cópias eram idênticas aos originais; quatro receberam ajustes documentados: remoção de um preâmbulo com credencial, remoção da identificação privada de instância em um script e mudança do destino de exportação em dois scripts. As contagens foram preservadas. O [inventário](../../../inventario_importacao.json) relaciona origem, destino e hashes; o [registro de organização](../../organizacao.md) explica o processo.

## Etapa 1: tamanho do GHZ

O [arquivo de contagens](../../../../dados/brutos/01_ghz_escala/ghz_05_a_50.txt) contém a série de 5 a 50 qubits, com 1.000 medidas por tamanho. O nome original da pasta mencionava simulações, mas os scripts correspondentes submetem circuitos à IBM. O texto não contém todos os metadados para reconstruir cada execução.

| Qubits | PZ observado |
| ---: | ---: |
| 5 | 0,922 |
| 10 | 0,740 |
| 15 | 0,601 |
| 20 | 0,477 |
| 25 | 0,454 |
| 30 | 0,308 |
| 35 | 0,285 |
| 40 | 0,219 |
| 45 | 0,187 |
| 50 | 0,109 |

A tendência descreve essa série. Não separa, por si, número de qubits, profundidade, roteamento, calibração ou backend. A tabela completa, com zeros, uns e demais resultados, está em [resumo_escala.csv](../../../../dados/processados/resumo_escala.csv).

## Etapas 2 e 3: controles e construção conectada

Há scripts de estados conhecidos, comparação de zeros, qubits individuais e GHZ conectado. Não foram recuperados arquivos separados de contagens para todos esses testes. O [guia histórico](../../experimentos.md) conserva números relatados em conversa, como 13 contra 4 portas de dois qubits e PZ de 0,833 contra 0,888. Esses valores não têm a mesma rastreabilidade dos três JSONs de mitigação e não entram como novas rodadas na comparação estatística.

O script conectado de 50 qubits existe; não há resultado bruto dessa execução no conjunto importado. Não atribuímos a ele uma melhora medida.

## Etapa 4: três rodadas reais de mitigação

As três usam backend registrado `ibm_fez`, qubits físicos 0–4, 32 preparações de calibração e GHZ conectado em Z/X. São 34 circuitos × 1.000 shots = 34.000 medidas por rodada, ou 102.000 no conjunto.

| Rodada na análise | Job | Registro |
| --- | --- | --- |
| 1 | `dbccq67i0auc73dumdk0` | [JSON histórico 1](../../../../dados/brutos/04_mitigacao_leitura/GHZ_leitura_dbccq67i0auc73dumdk0.json) |
| 2 | `dbccri9gv2cc73ea3630` | [JSON histórico 2](../../../../dados/brutos/04_mitigacao_leitura/GHZ_leitura_dbccri9gv2cc73ea3630.json) |
| 3 | `dbjnndgnceqs73akbkh0` | [JSON da rodada 3](../../../../dados/brutos/04_mitigacao_leitura/rodada_03/rodada_03.json) |

Os rótulos 1 e 2 identificam os arquivos históricos; não recuperam datas que não foram registradas. A rodada 3 tem envio registrado em 1 de novembro de 2026, versões, opções, metadados e [QPY](../../../../dados/brutos/04_mitigacao_leitura/rodada_03/rodada_03.qpy). As primeiras duas não oferecem uma auditoria equivalente dos circuitos compilados.

| Rodada | PZ bruto | PZ ajustado | CX bruto | CX ajustado |
| --- | ---: | ---: | ---: | ---: |
| 1 | 0,8730 | 0,9436 | 0,7960 | 0,9440 |
| 2 | 0,8640 | 0,9360 | 0,7960 | 0,9481 |
| 3 | 0,8950 | 0,9648 | 0,8060 | 0,9702 |

Essa tabela traz valores centrais. As incertezas e intervalos estão no [relatório comparativo](../../../comparacao_rodadas.md). O aumento dos dois indicadores se repete nas três execuções; isso sustenta repetibilidade preliminar do efeito do estimador nesse conjunto. Não demonstra estabilidade para qualquer dia, backend ou tamanho.

## O que ocorreu nesta cópia do Desktop

Os três commits de organização e da rodada 3 vieram de outra cópia local. O job da rodada 3 já estava concluído. Depois fizemos processamento local, documentação e simulação; não reenviamos esse job. A autorização posterior para push publicou código e resultados no GitHub, não executou circuitos na IBM.

**Para conferir uma afirmação:** escolha uma linha da tabela, abra seu JSON, identifique `contagens` e o `job_id`, e compare com o arquivo processado. O próximo capítulo explica o cálculo e seus erros.

---

[← Anterior](../04-mitigacao-leitura/README.md) · [Índice do livro](../../../../README.md) · [Próximo →](../06-estatistica/README.md)
