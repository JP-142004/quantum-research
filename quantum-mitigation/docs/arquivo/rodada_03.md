# Terceira rodada de mitigação de leitura

Execução enviada em 1 de novembro de 2026 ao `ibm_fez`.

- Job: `dbjnndgnceqs73akbkh0`, concluído.
- Qubits físicos: 0, 1, 2, 3 e 4.
- Circuitos: 32 estados de calibração e GHZ conectado nas bases Z e X.
- Medidas: 1.000 por circuito, 34.000 no total.
- Construção GHZ: raiz 2, conexões (2,1), (2,3), (1,0), (3,4).
- DD e twirling desativados, como nas rodadas anteriores.

| Indicador | Bruto | Ajustado |
| --- | ---: | ---: |
| População em Z | 0,8950 ± 0,0094 | 0,9648 ± 0,0125 |
| Correlação em X | 0,8060 ± 0,0182 | 0,9702 ± 0,0226 |

Os erros apresentados são erros padrão calculados com 300 reamostragens bootstrap, incluindo a amostragem de calibração e GHZ. Não incluem toda a deriva do hardware ou o erro do modelo de calibração.

O condicionamento da matriz foi 1,2129. As menores quasiprobabilidades foram −0,00787 em Z e −0,00426 em X. Não houve recorte dos valores negativos na análise.

Assim como nas duas rodadas históricas, o ajuste aproximou os dois indicadores de 1. Isso reforça a observação de repetibilidade nestas três execuções. Não demonstra que os erros das portas foram eliminados, nem mede a fidelidade completa do GHZ.

As contagens originais, versões, parâmetros, ID do job e análise estão em `dados/brutos/04_mitigacao_leitura/rodada_03/rodada_03.json`. Os circuitos compilados enviados foram preservados no arquivo QPY de mesmo nome. Nenhuma credencial foi incluída nesses arquivos.
