# 04 — Calibração e mitigação de leitura

[Experimentos](../README.md) · [Teoria da mitigação](../../docs/livro/04-mitigacao-leitura/README.md) · [Resultados reais](../../docs/livro/05-experimentos-reais/README.md)

O protocolo real prepara 32 estados de calibração e GHZ conectado em Z/X, com 1.000 shots por circuito. Os cinco qubits físicos são 0–4 e o backend registrado é `ibm_fez`. As opções registradas da rodada 3 deixam DD e twirling desativados e inicialização habilitada.

## Dois programas, comportamentos diferentes

| Programa | Funcionamento |
| --- | --- |
| [mitigacao_leitura.py](mitigacao_leitura.py) | Versão histórica: `JOB_ID` vazio envia um job; preenchido consulta o job indicado. O corpo do arquivo executa essas ações. Salva contagens e imprime análise com 300 bootstraps. |
| [repetir_mitigacao.py](repetir_mitigacao.py) | Versão que separa verificação ideal, envio e coleta por argumentos; grava registro e QPY da rodada. |

`repetir_mitigacao.py --verificar` confere idealmente os 34 circuitos sem acessar o serviço, embora o módulo importe a dependência Runtime. `--coletar` consulta o job já registrado e pode salvar contagens/análise; se ainda não terminou, retorna sem aguardar indefinidamente. `--enviar` exige que o arquivo daquela rodada não exista, compila e submete uma rodada real. Números menores que 3 são reservados às históricas.

A semente de ordem é 42 + número da rodada; a semente de compilação é 42. A análise da coleta usa 300 réplicas e semente 2000 + rodada. O limite de execução solicitado é 120 segundos, diferente de tempo de fila. O envio recusa mapeamento inesperado; as conexões precisam existir no backend escolhido.

## Rodada 3 concluída

O job `dbjnndgnceqs73akbkh0` já terminou. O [JSON](../../dados/brutos/04_mitigacao_leitura/repeticoes/rodada_03.json), o [QPY](../../dados/brutos/04_mitigacao_leitura/repeticoes/rodada_03.qpy) e o [relatório original](../../docs/rodada_03.md) estão preservados. Não é necessário consultar ou enviar esse job para reproduzir a análise consolidada: use [comparar_rodadas.py](../../scripts/comparar_rodadas.py), que é local.

O script de repetição implementa o protocolo antigo de 34 circuitos. Ele **não** implementa a proposta nova de 40 circuitos com duas construções e controles; essa proposta foi implementada e validada apenas no executor local.
