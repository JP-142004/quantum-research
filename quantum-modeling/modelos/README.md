# Modelo de linha de base

[Visão da modelagem](../README.md)

[comparar_ghz_nivel0.py](comparar_ghz_nivel0.py) é o programa existente nesta pasta. Ele recupera dez jobs IBM já conhecidos, extrai circuito/contagens, monta o modelo de ruído do backend, simula localmente e salva distâncias de Hellinger.

A função `escolher_metodo()` retorna `statevector` para tamanhos até 20 e `matrix_product_state` para os maiores. `main()` gerencia a consulta, cache de simuladores por backend/método, cálculo da distância e gravação do JSON. Uma exceção por job é registrada e o programa segue para os demais.

Não é um modelo ajustado por algoritmo evolutivo. Não fixa semente da simulação nem preserva um snapshot completo da calibração usada. Reexecutar acessa a IBM e sobrescreve a saída histórica, embora não envie um novo job quântico. Para apenas estudar o resultado existente, abra o JSON e o README da pasta de resultados.
