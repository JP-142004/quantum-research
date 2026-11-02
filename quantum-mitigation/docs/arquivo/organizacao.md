# Organização dos arquivos

> Atualização de 2 de novembro de 2026: as contagens e os circuitos históricos das [etapas 2](../../dados/brutos/02_controles/README.md) e [3](../../dados/brutos/03_ghz_conectado/README.md) foram recuperados diretamente da IBM. Referências abaixo à ausência desses arquivos descrevem o estado anterior da importação.

Foram importados os 23 arquivos encontrados na pasta de origem `Mitigaçao de ruido`, dentro de `OneDrive_2026-10-18`. Os originais foram preservados. Os nomes das cópias foram padronizados para facilitar a navegação e o uso no terminal.

O arquivo `inventario_importacao.json` relaciona cada caminho original ao novo caminho e registra os hashes SHA-256. Dezenove cópias são idênticas aos originais. Quatro receberam ajustes documentados:

- `ghz_05_a_50.txt`: removido o preâmbulo de configuração que continha uma credencial. As contagens foram preservadas.
- `recuperar_job.py`: removida a identificação privada da instância IBM; o serviço usa as credenciais locais.
- `ghz_50_conectado.py` e `mitigacao_leitura.py`: alterado somente o destino de exportação dos resultados para `dados/brutos/`.

As tabelas em `dados/processados/` são derivadas; podem ser recriadas com `scripts/resumir_resultados.py`. Elas não substituem os dados brutos. Resultados mencionados apenas na conversa estão identificados como tal no guia; não foram apresentados como arquivos brutos recuperados.

O diretório `quantum-modeling/` foi preservado. Nenhum circuito foi executado na IBM durante esta organização.
