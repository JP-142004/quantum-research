# Testes da implementação local

[Visão geral](../README.md) · [Scripts](../scripts/README.md)

O arquivo [test_protocolo_local.py](test_protocolo_local.py) usa `unittest`, Qiskit e Aer. Os testes são locais e não requerem conta IBM. O arquivo [test_documentacao.py](test_documentacao.py) não usa Qiskit: confere se as tabelas dos READMEs estão atualizadas em relação aos dados, se os links relativos existem e se alguns números citados no [relatório](../docs/relatorio.md) coincidem com os dados.

| Teste | Falha que procura detectar |
| --- | --- |
| `test_distribuicoes_e_roteamento` | Circuito lógico/compilado incorreto, ligação fora do mapa ou cancelamento do dobramento |
| `test_controle_negativo_e_paridade` | Erro no qubit do controle negativo ou no sinal da paridade |
| `test_canal_assimetrico_e_mapa` | Inversão de convenção e erro de permutação físico/clássico |
| `test_aer_convencao_leitura` | Interpretação incorreta das linhas de `ReadoutError` |
| `test_invalido_e_singular` | Aceitação de contagens inválidas ou matriz singular |
| `test_extrapolacao_linear_e_identidade` | Erro no intercepto linear ou na inversão identidade |

Os seis passaram na execução registrada e novamente em 2 de novembro de 2026, com Qiskit 2.6.0 e Aer 0.17.2. O auditor dos resultados é uma verificação adicional: lê os dados salvos, valida QPY e hashes e compara métricas com o modelo exato. Testes não provam a adequação de um modelo à IBM nem equivalem a novos experimentos reais.

```powershell
.\.venv-simulacao\Scripts\python.exe -m unittest discover -s quantum-mitigation/tests -v
```

Execute a partir da raiz após preparar o ambiente conforme o guia. Não importe os scripts históricos de submissão para realizar testes automáticos.
