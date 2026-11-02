# Quantum Research — PIBIC

Pesquisa em circuitos GHZ, ruído e mitigação. O repositório reúne código, dados reais da IBM, análise estatística e simulações locais. A documentação distingue resultados disponíveis de propostas ainda não executadas.

## Comece por aqui

- [Frente de mitigação](quantum-mitigation/README.md): introdução, fundamentos, um relatório por experimento, dados e scripts.
- [Frente de modelagem](quantum-modeling/README.md): comparação histórica entre hardware e modelos ruidosos.
- [Relatório da mitigação](quantum-mitigation/docs/relatorio.md): a pesquisa em formato de artigo.
- [Planejamento](quantum-mitigation/docs/planejamento.md): próximos passos propostos.

## As duas frentes

| Frente | Pergunta |
| --- | --- |
| `quantum-mitigation` | Quanto melhorar a construção do circuito e ajustar a leitura muda os indicadores GHZ? |
| `quantum-modeling` | Quanto um modelo de ruído reproduz as distribuições medidas no equipamento? |

Na frente de mitigação há três rodadas reais de cinco qubits, 102.000 shots nesse conjunto e uma validação local de 486.000 shots simulados. Há também uma série histórica de GHZ de 5 a 50 qubits. Esses conjuntos não devem ser somados ou confundidos como se fossem um único experimento.

A modelagem já tinha código e resultados de linha de base; várias de suas pastas ainda são estrutura reservada. A validação local nova não implementou um ajuste evolutivo nem substituiu essa frente.

## Estado da branch e reprodução

O trabalho documentado foi publicado na branch `mitigation`, sem merge em `main`. Esta revisão documental é de 2 de novembro de 2026. O [README dos scripts](quantum-mitigation/scripts/README.md) contém os comandos de análise, testes e simulação local.

Scripts históricos podem acessar a IBM e enviar jobs; a documentação de cada pasta informa esse comportamento. O job `dbjnndgnceqs73akbkh0` já está concluído. Não é necessário reenviá-lo para estudar ou recalcular os resultados.
