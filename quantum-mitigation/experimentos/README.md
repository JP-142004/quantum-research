# Experimentos

Cada pasta numerada é um experimento completo: o relatório (`README.md`), a receita (`experimento.py`), os dados e os resultados. As perguntas seguem a ordem em que surgem, e cada conclusão leva à pergunta seguinte.

## O plano desta rodada

| # | Pasta | Pergunta | Circuito | Técnica | Onde roda | Tamanhos |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | `01_escala` | Como o erro cresce de 5 a 50 qubits? | GHZ original | nenhuma | IBM | 5, 10, … 50 |
| 2 | `02_controles` | O computador acerta o que é fácil? | estados simples (zeros, uns, um qubit) | nenhuma | IBM | 1 e 5 |
| 3 | `03_construcao` | Montar o GHZ com menos passos melhora o resultado? | GHZ original e conectado | construção | IBM | 5, 10, 20 |
| 4 | `04_calibracao_leitura` | A calibração de leitura aproxima os indicadores do ideal? | GHZ conectado, mais 4 controles | leitura | IBM | 5 |
| 5 | `05_validacao_simulada` | O que a calibração recupera quando o erro é conhecido? | GHZ original e conectado | leitura | simulador | 5 |
| 6 | `06_zne_simulado` | A extrapolação a ruído zero reduz o erro das portas? | GHZ conectado | ZNE e leitura | simulador | 5 |

Os experimentos 1 a 4 rodam em **3 sessões, em 3 dias diferentes**. Em cada sessão, os quatro rodam no mesmo computador, com as mesmas opções, e cada sessão tem a sua pasta de dados. Isso permite comparar os experimentos entre si e ver o quanto o computador muda de um dia para o outro. A estimativa é de cerca de 72 mil medidas por sessão. O número de medidas não é o tempo de uso da IBM.

Opções fixas em todos os envios: desacoplamento dinâmico desligado, twirling desligado, `init_qubits` ligado, compilação nível 1, semente 42 e 1.000 shots por circuito.

## Critérios de sucesso (proposta, a confirmar antes da primeira sessão)

Definidos antes de rodar, para não escolher o resultado depois:

- **Experimento 3:** a conectada só conta como melhor se a diferença tiver o mesmo sinal nas 3 sessões. Caso contrário, o resultado é "inconclusivo".
- **Experimento 4:** a calibração só conta como "ajudou" se o valor ajustado ficar mais perto de 1 nas 3 sessões. Os controles independentes decidem se a melhora vem mesmo da leitura.
- **Todos:** cada sessão aparece separada, com a variação entre elas, sem juntar tudo numa média só.

## Regras de envio à IBM

- Todo programa de envio tem três modos: `--verificar` (local, mostra o que seria enviado e quantas medidas), `--enviar` e `--coletar`. Nada vai à IBM sem `--enviar`.
- Uma sessão já registrada não é reenviada.
- Antes de cada envio, o autor aprova o que vai sair (circuitos, medidas, computador) e confere o saldo de tempo do seu plano.
- Credenciais ficam só no computador do autor.

## Roteiro para rodar

Os comandos partem da pasta `quantum-mitigation`, com o ambiente da raiz do repositório (`..\venv`).

**No simulador** (não gasta IBM, leva segundos). Cada comando grava todas as sessões do experimento:

```powershell
..\venv\Scripts\python rodar.py 05 --enviar --todas
..\venv\Scripts\python rodar.py 06 --enviar --todas
```

**Na IBM**, no dia de uma sessão. Os experimentos 1 a 4 rodam no **mesmo dia**, no mesmo computador:

1. Teste o código: `..\venv\Scripts\python -m unittest discover -s tests`.
2. Ensaio com o computador real, **sem enviar nada** (consulta as ligações e compila os circuitos nele): `..\venv\Scripts\python rodar.py 04 --verificar --online`, e o mesmo para 03, 02 e 01. Confira a coluna de portas de dois qubits e se nenhum circuito acusa `FALHOU`.
3. Confira quanto tempo ainda resta no seu plano da IBM.
4. Envie um experimento por vez: `..\venv\Scripts\python rodar.py 04 --enviar --computador ibm_fez`. O programa mostra o que vai sair e só envia depois de você digitar `ENVIAR`.
5. Quando o job terminar: `..\venv\Scripts\python rodar.py 04 --coletar --sessao AAAA-MM-DD_ibm_fez`. Para ver as sessões: `--listar`.

Uma sessão gravada não é reenviada nem sobrescrita. A análise dos dados e os relatórios de resultado vêm depois.

## Como acrescentar um experimento

1. Copie a pasta [_molde](_molde/README.md) para a próxima numeração, por exemplo `07_nome_curto`.
2. Escreva pergunta, indicador, controle, custo e critério de sucesso **antes** de executar.
3. Escolha o circuito, as técnicas e o computador na receita. Se o circuito ou a técnica ainda não existem, acrescente-os primeiro (veja a [capa](../README.md#como-o-repositório-cresce)).
4. Rode, colete e analise. Os dados de cada sessão ficam em `dados/` e **não são editados**.

[Visão geral](../README.md)
