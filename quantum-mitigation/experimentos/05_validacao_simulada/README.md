# Experimento 5 · O que a calibração recupera quando o erro é conhecido?

**Estado:** planejado, ainda não executado nesta versão. Resultado, Conclusão e Próximo passo serão escritos depois da execução.

**Onde e quando:** simulador no PC (Qiskit Aer, CPU), sem acesso à IBM. Cada circuito é simulado 1.000 vezes.

## Pergunta

Na IBM só vemos as contagens finais, não o estado antes da leitura. No simulador **nós escolhemos o erro**, então sabemos a resposta certa. A calibração de leitura recupera o estado anterior à leitura, e o que ela deixa para trás? O [experimento 4](../04_calibracao_leitura/README.md) mede na IBM; este separa as fontes de erro, uma de cada vez.

## Como será feito

- **Três cenários**, com três blocos cada (uma sessão por bloco, com calibração e semente próprias): **ideal** (sem ruído), **só leitura** e **leitura e portas** (erro de leitura mais ruído depois de cada CX).
- **Cada bloco tem 40 circuitos** de cinco qubits: 32 de calibração, 4 de GHZ (original e conectado, em Z e em X) e 4 controles independentes.
- **Parâmetros do modelo:** valores **sintéticos**, escolhidos por nós, em `mitigacao/execucao/ruido.py`. **Não** são de um computador real, então as magnitudes valem para este modelo e não para o Fez.
- **Referência exata:** para cada circuito, a distribuição exata do modelo antes e depois da leitura, sem flutuação de shots. Com ela medimos o que a análise deveria recuperar.
- **Custo:** 9 blocos × 40 circuitos × 1.000 = 360.000 medidas simuladas.
- **Critério (proposta, definida antes de rodar):** de sanidade, não de cobertura. Nenhum valor ajustado pode ficar a mais de 6 erros padrão da referência exata. Com erro só na leitura, a inversão exata deve recuperar a distribuição anterior à leitura.

## Arquivos

| Arquivo | Para que serve |
| --- | --- |
| `experimento.py` | A receita, com as 9 sessões. Rode com `python rodar.py 05 --enviar --todas`. |
| `dados/<cenário>_bloco_NN/` | Uma pasta por sessão. **Não se edita.** *(ainda não existem)* |
| `resultados/` | Tabelas e figuras geradas dos dados. *(ainda não existem)* |

**Execução:** tudo local, não acessa a IBM.

[Experimentos](../README.md)
