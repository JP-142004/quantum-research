# 03 — Construção conectada

[Experimentos](../README.md) · [Compilação e roteamento](../../docs/livro/03-circuitos-medidas/README.md)

## Objetivo

Preparar o mesmo GHZ usando interações que acompanham conexões físicas, evitando operações adicionais de roteamento quando possível. O número de portas e a profundidade são registrados para comparar o custo compilado.

| Script | Papel |
| --- | --- |
| [ghz_05_original_fez.py](ghz_05_original_fez.py) | Referência original de cinco qubits no Fez, layout 0–4 |
| [comparar_construcoes.py](comparar_construcoes.py) | Compara a construção original com árvores conectadas; testa raízes no compilador e escolhe menor número de portas de dois qubits, depois menor profundidade |
| [comparar_base_x.py](comparar_base_x.py) | Compara as construções com medidas na base X |
| [ghz_50_conectado.py](ghz_50_conectado.py) | Seleciona 50 qubits conectados por busca em largura a partir da raiz física 2 e prepara GHZ |

Todos usam 1.000 shots por circuito e selecionam `ibm_fez` no código histórico. O programa de 50 qubits não aplica calibração completa de leitura; ele mede a população em Z. Seu destino de saída foi organizado para `dados/brutos/03_ghz_conectado`, pasta criada pelo programa se uma execução gerar resultados.

## O que foi recuperado

O [guia histórico](../../docs/experimentos.md) registra a comparação relatada de 13 para 4 portas de dois qubits, profundidade de 35 para 13 e melhora em indicadores. Os arquivos brutos dessas comparações não foram encontrados na importação. Também não foi recuperado resultado do GHZ conectado de cinquenta qubits.

O protocolo novo local usa uma árvore fixa de cinco qubits e dados próprios de simulação; não transforma os relatos históricos em medidas rastreáveis. Veja a [validação local](../../docs/livro/07-simulacao-local/README.md).

**Execução:** estes arquivos consultam o backend e submetem jobs; não são comandos necessários para ler os resultados existentes.
