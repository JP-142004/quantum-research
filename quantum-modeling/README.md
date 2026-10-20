# Quantum Modeling

Modelagem de ruído em circuitos quânticos NISQ, calibrada com dados da IBM Quantum.

Responsável: João Paulo

## Estrutura
- `calibracao/` — snapshots diários de calibração da IBM
- `hardware/` — resultados reais de jobs executados no IBM Quantum
- `circuitos/` — geradores de circuitos (GHZ, Bell, aleatórios)
- `modelos/` — modelos de ruído (padrão, parametrizado, com erros coerentes)
- `ajuste/` — algoritmos evolutivos para calibrar os modelos
- `notebooks/` — análises exploratórias
- `resultados/` — distâncias, gráficos e dados finais
