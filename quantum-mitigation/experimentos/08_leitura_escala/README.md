# Experimento 8 · A calibração por qubit funciona em circuitos maiores?

**Estado em 22 de novembro de 2026:** parte A rodada e analisada (critérios escritos antes); parte B com plano, critérios e análise prontos e testados, **aguardando o envio à IBM pelo Luiz** (nada foi enviado).

## Por que este experimento

O [experimento 7](../07_leitura_fatorizada/README.md) comparou, em 5 qubits, a calibração de leitura com a matriz completa (32 × 32) e a calibração com uma tabela 2 × 2 por qubit. O resultado foi inconclusivo, sem nenhuma diferença clara. A matriz completa não passa de uns 10 qubits (com n qubits ela precisa de 2ⁿ calibrações), então a tabela por qubit só tem valor prático se funcionar em tamanhos maiores. Este experimento testa isso.

## Duas partes

| Parte | Onde | Pergunta | Estado |
| --- | --- | --- | --- |
| [A · simulador](a_simulador/README.md) | simulador, 10 qubits | Com erro de leitura conhecido, a tabela por qubit reproduz a correção da matriz completa? E se os qubits de um par erram juntos? | **feita**: o modelo por qubit acompanha o completo com erro independente e falha com erro conjunto nos pares |
| [B · IBM](b_ibm/README.md) | `ibm_fez`, 10 e 20 qubits | Os indicadores do GHZ chegam perto do ideal só com a calibração por qubit? | pronta para rodar; **o envio é feito pelo Luiz**, sessão a sessão, com confirmação |

A parte A vem primeiro: no simulador o erro é conhecido, então dá para saber o que esperar antes de gastar tempo da IBM.

## Como rodar cada parte

A partir de `quantum-mitigation/`: `python rodar.py 08a ...` (parte A) e `python rodar.py 08b ...` (parte B). A letra escolhe a pasta `a_*` ou `b_*` dentro deste experimento.

[Experimentos](../README.md)
