# Experimentos

Cada pasta numerada é um mini relatório: a pergunta, como foi feito, o resultado, a conclusão e o próximo passo, com o código ao lado. Os experimentos seguem a ordem em que as perguntas surgiram, e cada conclusão leva à pergunta seguinte.

| # | Experimento | Onde | O que ficou claro | Pergunta que abriu |
| --- | --- | --- | --- | --- |
| 1 | [Escala do GHZ](01_ghz_escala/README.md) | IBM | PZ cai de 0,922 para 0,109 entre 5 e 50 qubits. | O desvio já aparece em estados simples? |
| 2 | [Controles](02_controles/README.md) | IBM | Sim, e depende do backend e do dia. | Dá para preparar o GHZ com menos operações? |
| 3 | [Construção com menos portas](03_ghz_conectado/README.md) | IBM | A construção conectada tem indicadores brutos melhores. | E o erro de leitura, dá para corrigir? |
| 4 | [Calibração de leitura](04_mitigacao_leitura/README.md) | IBM | PZ e CX se aproximam de 1 nas três rodadas. | O que a calibração recupera se o erro for conhecido? |
| 5 | [Validação simulada](05_validacao_simulada/README.md) | PC | A calibração compensa a leitura, não as portas. | Existe uma técnica para o erro das portas? |
| 6 | [ZNE simulada](06_zne_simulado/README.md) | PC | A extrapolação aproxima do ideal, com viés e mais incerteza. | A ZNE funciona no hardware? (não testado) |

Antes de ler, vale passar por [fundamentos](../fundamentos/README.md): os experimentos usam termos como shot, PZ e CX, que lá estão explicados.

Os dados de cada experimento estão em [dados](../dados/README.md) e as figuras em [figuras](../figuras/README.md).

## Antes de executar qualquer programa

Os programas Python das pastas 1 a 4 **enviam jobs à IBM** quando executados. Para estudar os resultados não é necessário executá-los: os dados já estão salvos. Os comandos que apenas leem dados, sem acessar a IBM, estão em [scripts](../scripts/README.md). Novos envios à IBM exigem decisão específica do Luiz, com o orçamento de medidas combinado antes.

## Como acrescentar um experimento

1. Copie a pasta [_modelo](_modelo/README.md) para a próxima numeração, por exemplo `07_nome_curto`.
2. Escreva pergunta, indicador, controle, custo e critério de sucesso **antes** de executar.
3. Guarde as contagens em `dados/` com o mesmo número e calcule os indicadores por script, nunca à mão.
4. Para tabelas, use os marcadores de [gerar_tabelas.py](../scripts/gerar_tabelas.py), para que o número do texto sempre venha do dado.
5. Acrescente uma linha na tabela acima, em [dados](../dados/README.md), em [figuras](../figuras/README.md) e, se houver técnica nova, em [tecnicas.md](../fundamentos/tecnicas.md).

[Visão geral](../README.md)
