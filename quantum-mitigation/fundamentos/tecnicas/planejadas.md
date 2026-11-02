# Técnicas planejadas

Ainda não testadas neste projeto. As duas primeiras existem como opções de execução do serviço da IBM e ficam **desativadas** nos experimentos, para que os resultados não as incluam sem querer.

- **Twirling de Pauli.** Insere portas de Pauli aleatórias antes e depois de cada CX, de modo que o circuito ideal não muda. O ruído passa a se comportar como uma mistura de erros simples, mais fácil de mitigar (Wallman e Emerson, 2016).
- **Desacoplamento dinâmico.** Insere sequências de pulsos nos períodos em que um qubit espera, para reduzir o efeito do ambiente (Viola, Knill e Lloyd, 1999).
- **Cancelamento probabilístico de erros (PEC).** Aprende-se um modelo do ruído das portas, e o circuito é executado com variações sorteadas cuja combinação cancela o ruído em média. Evita o viés da ZNE, mas exige caracterizar o ruído e mais amostras (van den Berg et al., 2023).

Quando uma delas for testada, ganha o seu próprio arquivo em `tecnicas/` e sai desta lista.

[Técnicas](README.md)
