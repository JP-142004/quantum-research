# Experimento 6 · A extrapolação a ruído zero reduz o erro das portas?

**Estado:** planejado, ainda não executado nesta versão. Resultado, Conclusão e Próximo passo serão escritos depois da execução.

**Onde e quando:** simulador no PC (Qiskit Aer, CPU), sem acesso à IBM. Cada circuito é simulado 1.000 vezes.

## Pergunta

A calibração de leitura não desfaz o erro das portas ([experimento 5](../05_validacao_simulada/README.md)). Se executarmos o circuito com ruído de portas crescente e extrapolarmos o indicador até ruído zero, chegamos mais perto do valor ideal? A técnica (ZNE) está explicada, com a conta, em [zne](../../fundamentos/tecnicas/zne.md).

## Como será feito

- **Versões com mais ruído:** o GHZ conectado de 5 qubits em três versões com o mesmo resultado ideal, repetindo o bloco de preparação como U · U⁻¹ · U. Os **fatores de ruído** são 1, 3 e 5, com 4, 12 e 20 portas CX.
- **Correção de leitura:** cada versão é ajustada pela calibração do bloco, depois ajustamos uma reta aos três valores e lemos o valor no fator 0.
- **Cenário:** leitura e portas (os parâmetros sintéticos estão em `mitigacao/execucao/ruido.py`).
- **Cada bloco tem 42 circuitos:** 6 de GHZ (3 fatores × Z e X), 32 de calibração e 4 controles independentes. Três blocos, uma sessão cada.
- **Custo:** 3 blocos × 42 circuitos × 1.000 = 126.000 medidas simuladas.
- **Critério (proposta, definida antes de rodar):** relatar, em cada bloco, o valor no fator 1, o valor extrapolado e a referência exata do modelo, com o erro padrão. Sem recortar valores fora do intervalo físico e sem escolher o ajuste que chega mais perto de 1.
- **Limite já conhecido:** a reta é uma escolha; a queda real não é perfeitamente linear, então a extrapolação deixa um viés.

## Arquivos

| Arquivo | Para que serve |
| --- | --- |
| `experimento.py` | A receita, com as 3 sessões. Rode com `python rodar.py 06 --enviar --todas`. |
| `dados/bloco_NN/` | Uma pasta por sessão. **Não se edita.** *(ainda não existem)* |
| `resultados/` | Tabelas e figuras geradas dos dados. *(ainda não existem)* |

**Execução:** tudo local, não acessa a IBM.

[Experimentos](../README.md)
