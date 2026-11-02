# Experimentos históricos e acesso à IBM

[Índice do livro](../README.md) · [História experimental](../docs/livro/05-experimentos-reais/README.md)

Esta pasta conserva os programas usados ou preparados nas etapas experimentais anteriores. A presença do script não garante que exista um resultado bruto correspondente. Os READMEs de cada etapa indicam o que foi recuperado.

| Etapa | Conteúdo |
| --- | --- |
| [01 — Escala GHZ](01_ghz_escala/README.md) | Dez tamanhos, de 5 a 50 qubits |
| [02 — Controles](02_controles/README.md) | Estados conhecidos e qubits individuais/juntos |
| [03 — GHZ conectado](03_ghz_conectado/README.md) | Comparação de construções e bases |
| [04 — Mitigação de leitura](04_mitigacao_leitura/README.md) | Calibração e três rodadas reais |

## Comportamento de execução

A maior parte desses scripts cria o serviço e submete circuitos no corpo do arquivo. Executar ou importar um desses arquivos pode acessar a IBM e criar um job. A exceção de organização mais recente é `repetir_mitigacao.py`, que separa ações por argumentos e tem um ponto de entrada protegido.

Para estudar os dados já salvos, use os [scripts de análise](../scripts/README.md). Para testar o protocolo novo, use a [reprodução local](../docs/livro/09-reproducao/README.md). Nenhuma dessas tarefas exige reenviar os experimentos históricos.

Os backends escritos nos scripts são configurações históricas, não uma indicação de disponibilidade atual. As dependências históricas em `requirements.txt` não estão fixadas; qualquer execução futura de hardware precisa de revisão das versões e do backend.
