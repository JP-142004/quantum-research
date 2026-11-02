# Como chegamos à mitigação de leitura

Começamos com uma pergunta simples. Se o GHZ deveria produzir apenas todos zeros ou todos uns em Z, com que frequência o equipamento devolvia outra coisa? Cada etapa abaixo responde a uma dúvida deixada pela anterior.

1. [Escala](01_ghz_escala/README.md). Contamos os resultados esperados em circuitos de cinco a cinquenta qubits.
2. [Controles](02_controles/README.md). Investigamos como testar o equipamento com estados conhecidos.
3. [Reconstrução](03_ghz_conectado/README.md). Procuramos um caminho com menos operações para preparar o mesmo estado.
4. [Leitura](04_mitigacao_leitura/README.md). Medimos como o equipamento registrava respostas conhecidas e usamos essa informação para ajustar os indicadores do GHZ.

Depois, passamos ao [simulador local](../dados/simulados/README.md), onde é possível escolher qual erro introduzir. Os programas históricos desta pasta podem submeter jobs quando executados ou importados. Para acompanhar as contas, basta abrir os arquivos de dados indicados em cada etapa.
