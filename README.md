# quantum-research

Iniciação Científica (PIBIC, PUCPR): técnicas de modelagem e mitigação de ruído em
computadores quânticos NISQ, com dados reais da IBM Quantum.
Orientadores: Rodrigo Pasti e Jonas Krause.

| Pasta | Conteúdo |
|---|---|
| [`quantum-modeling/`](quantum-modeling/README.md) | Modelagem de ruído: simulação local vs. hardware real e ajuste evolutivo do modelo (João Paulo) |
| [`quantum-mitigation/`](quantum-mitigation/README.md) | Técnicas de mitigação de erro |

## Ambiente

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r quantum-modeling/requirements.txt
```

A conta da IBM é salva uma vez com `QiskitRuntimeService.save_account(...)` e fica fora do
repositório. Nunca versione tokens ou CRNs.
