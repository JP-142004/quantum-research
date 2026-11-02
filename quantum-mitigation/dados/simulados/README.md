# 5. O que a calibração consegue corrigir?

Na IBM, vemos os bits registrados ao fim de cada medida. No PC podemos escolher o erro e calcular quanto o indicador valia **antes** da leitura. Isso permite saber se o ajuste recuperou aquilo que pretendíamos recuperar.

## O mesmo teste, com três condições

Preparamos o GHZ original e o conectado. Os dois devem produzir o mesmo estado ideal, embora o circuito original possa precisar de mais operações ao ser adaptado às conexões disponíveis.

| O que introduzimos no simulador | O que vimos |
| --- | --- |
| Nenhum erro | Os dois circuitos atingiram 1 em PZ e na correlação X. Os controles também deram os sinais esperados. |
| Somente erro de leitura | Na referência calculada sem sorteio de shots, PZ valia 1 antes da leitura e 0,8366 depois. Ao inverter o canal conhecido, recuperamos 1. |
| Erro nas operações e na leitura | Antes mesmo de medir, PZ já era 0,8409 no circuito original e 0,9463 no conectado. A inversão exata da leitura recuperou esses valores. |

A última linha explica por que usamos duas técnicas. Construir um caminho mais curto diminui a exposição a portas ruidosas. Calibrar o leitor permite ajustar o que ele registrou. Se o circuito chegou à leitura com PZ de 0,8409, corrigir perfeitamente o leitor recupera **0,8409**.

## Como fizemos a comparação com shots

Em cada bloco, executamos 32 calibrações, quatro circuitos GHZ (duas construções em duas bases) e quatro controles com respostas conhecidas. Os controles receberam amostras próprias. Foram 40 circuitos × 1.000 shots × 3 blocos × 3 condições = **360.000 shots simulados**.

Uma referência exata e uma estimativa com shots são coisas diferentes. Por exemplo, no primeiro bloco com erros nas portas e na leitura, PZ ajustado foi 0,8408 ± 0,0195 no original e 0,9290 ± 0,0190 no conectado. Compare esses números com a última linha da tabela. A diferença é esperada quando estimamos tanto a calibração quanto o GHZ com amostras finitas.

O [protocolo](../../scripts/protocolo_local.py) define circuitos e ruídos; o [executor](../../scripts/validar_protocolo_local.py) produz os blocos. Em cada par de JSONs, `_contagens` contém as frequências e `_analise` contém os cálculos. O [manifesto](validacao_2026_11_01/manifesto.json) guarda sementes, versões e referências exatas. Consulte o [relatório](validacao_2026_11_01/relatorio.md) para ver todos os blocos e a [verificação](validacao_2026_11_01/verificacao.json) para conferir a auditoria. Esses erros foram escolhidos para testar o método no PC.

**Próxima pergunta:** o que podemos tentar quando o erro das operações permanece? O [passo 6, piloto de ZNE](zne/README.md), acrescentou 126.000 shots, totalizando **486.000 shots locais**.
