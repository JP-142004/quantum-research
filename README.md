# Quantum Research — PIBIC

Pesquisa em circuitos GHZ, ruído e mitigação. O repositório reúne código, dados reais da IBM, análise estatística e simulações locais. A documentação distingue resultados disponíveis de propostas ainda não executadas.

## Comece por aqui

- [Livro da frente de mitigação](quantum-mitigation/README.md): 12 capítulos, dos fundamentos ao código e à reprodução.
- [Frente de modelagem](quantum-modeling/README.md): comparação histórica entre hardware e modelos ruidosos.
- [Resumo para o orientador](quantum-mitigation/docs/resumo_orientador.md): síntese dos três registros reais de mitigação.
- [Histórico e limites](quantum-mitigation/docs/livro/11-historico-limites/README.md): trabalho concluído e próximos passos.

## As duas frentes

| Frente | Pergunta |
| --- | --- |
| `quantum-mitigation` | Quanto melhorar a construção do circuito e ajustar a leitura muda os indicadores GHZ? |
| `quantum-modeling` | Quanto um modelo de ruído reproduz as distribuições medidas no equipamento? |

Na frente de mitigação há três rodadas reais de cinco qubits, 102.000 shots nesse conjunto e uma validação local de 486.000 shots simulados. Há também uma série histórica de GHZ de 5 a 50 qubits. Esses conjuntos não devem ser somados ou confundidos como se fossem um único experimento.

A modelagem já tinha código e resultados de linha de base; várias de suas pastas ainda são estrutura reservada. A validação local nova não implementou um ajuste evolutivo nem substituiu essa frente.

## Estado da branch e reprodução

O trabalho documentado foi publicado na branch `mitigation`, sem merge em `main`. Esta revisão documental é de 2 de novembro de 2026. O [guia de reprodução](quantum-mitigation/docs/livro/09-reproducao/README.md) contém os comandos de análise, testes e simulação local.

Scripts históricos podem acessar a IBM e enviar jobs; a documentação de cada pasta informa esse comportamento. O job `dbjnndgnceqs73akbkh0` já está concluído. Não é necessário reenviá-lo para estudar ou recalcular os resultados.
