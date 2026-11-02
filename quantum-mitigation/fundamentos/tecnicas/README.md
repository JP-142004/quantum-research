# Técnicas de mitigação

**Mitigação não é correção de erros.** A correção de erros protege os qubits durante a computação e exige qubits adicionais. A mitigação, segundo van den Berg et al. (2023), só busca estimativas corretas de valores esperados, tratando o equipamento como ele é. Este projeto estuda mitigação.

| Técnica | Fonte de ruído que ataca | Explicação | Situação |
| --- | --- | --- | --- |
| Construção do circuito com menos portas | Portas, decoerência | [construcao.md](construcao.md) | Nesta rodada (experimento 3) |
| Calibração de leitura | Leitura | [leitura.md](leitura.md) | Nesta rodada (experimento 4) |
| Extrapolação a ruído zero (ZNE) | Portas | [zne.md](zne.md) | Nesta rodada, só em simulação (experimento 6) |
| Twirling de Pauli | Ruído coerente | [planejadas.md](planejadas.md) | Planejada |
| Desacoplamento dinâmico | Decoerência | [planejadas.md](planejadas.md) | Planejada |
| Cancelamento probabilístico de erros (PEC) | Portas | [planejadas.md](planejadas.md) | Planejada |

Os termos "leitura", "portas" e "decoerência" estão explicados em [ruido.md](../ruido.md).

## Como acrescentar uma técnica

1. Escreva `mitigacao/tecnicas/<nome>.py` (que circuitos extras ela precisa e como corrige as contagens).
2. Escreva `fundamentos/tecnicas/<nome>.md`, com a ideia, uma conta com números e os limites. Uma técnica planejada começa em [planejadas.md](planejadas.md) e ganha o seu arquivo quando for testada.
3. Acrescente a referência em [referencias.md](../referencias.md).

[Fundamentos](../README.md)
