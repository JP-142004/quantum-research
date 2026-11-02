# 09. Como instalar, executar e conferir

[← Anterior](../08-zne/README.md) · [Índice do livro](../../../../README.md) · [Próximo →](../10-codigo-dados/README.md)

## Antes de executar

Todos os comandos abaixo partem da raiz do checkout, a pasta que contém `quantum-mitigation` e `quantum-modeling`. Os exemplos usam PowerShell no Windows. Não precisam de GPU ou credenciais IBM para análise, testes e simulação local. A instalação de dependências requer acesso ao índice de pacotes.

Para começar por uma cópia nova da branch documentada:

```powershell
git clone --branch mitigation https://github.com/JP-142004/quantum-research.git
cd quantum-research
git status --short --branch
```

Se já tem um checkout com alterações, não o substitua: confira `git status` e use a cópia existente ou outra pasta. Anote o commit com `git rev-parse HEAD` ao registrar uma execução.

## Analisar as três rodadas sem IBM

```powershell
py -3.12 -m venv .venv-analise
.\.venv-analise\Scripts\python.exe -m pip install -r quantum-mitigation/requirements-analise.txt
.\.venv-analise\Scripts\python.exe quantum-mitigation/scripts/resumir_resultados.py
.\.venv-analise\Scripts\python.exe quantum-mitigation/scripts/comparar_rodadas.py
```

O primeiro script recria os dois CSVs históricos. O segundo lê os três JSONs reais e recria o JSON comparativo, o relatório e os quatro arquivos de gráficos. **Essas saídas derivadas são sobrescritas; os dados brutos não são.** Para não modificar sequer os derivados do checkout principal, faça essa reprodução em outra cópia.

Se `py` não estiver disponível, use `python` apontando para a instalação desejada. Não é necessário ativar o ambiente, porque chamamos seu executável diretamente. Em Linux/macOS, o equivalente é `python3 -m venv` e o executável fica em `.venv-analise/bin/python`.

## Testar e simular localmente

```powershell
py -3.12 -m venv .venv-simulacao
.\.venv-simulacao\Scripts\python.exe -m pip install -r quantum-mitigation/requirements-simulacao.txt
.\.venv-simulacao\Scripts\python.exe -m unittest discover -s quantum-mitigation/tests -v
.\.venv-simulacao\Scripts\python.exe quantum-mitigation/scripts/validar_protocolo_local.py --execucao minha_validacao_01
```

O programa cria `quantum-mitigation/dados/simulados/minha_validacao_01`. São 12 blocos, 486.000 shots simulados e 2.000 réplicas bootstrap por bloco. Os números de blocos e shots estão fixados no código atual; não há opções CLI para alterá-los. O nome da execução aceita letras ASCII, números, hífen e underscore.

Se a pasta já existe, a execução para com erro em vez de sobrescrevê-la. Escolha um novo nome para outra execução. Se uma execução falhar, o manifesto pode permanecer como `iniciada`, com arquivos parciais preservados; essa pasta não é um resultado concluído.

## Auditar um registro salvo

```powershell
.\.venv-simulacao\Scripts\python.exe quantum-mitigation/scripts/verificar_registro_local.py quantum-mitigation/dados/simulados/validacao_2026_11_01
```

Esse comando lê contagens, análises, manifesto e QPY, e grava `verificacao.json` na mesma pasta. Para o registro incluído, o resultado esperado é `aprovado`, com 12 blocos, 486.000 shots, 26 hashes e dois QPY. A auditoria não consulta a IBM.

Os hashes são dos bytes dos arquivos. Uma conversão de finais de linha LF/CRLF pode alterar um hash sem alterar os valores JSON. Em um clone novo destinado à auditoria byte a byte, pode-se usar `git -c core.autocrlf=false clone --branch mitigation URL PASTA`, substituindo URL e PASTA. Se houver divergência, investigue primeiro arquivo, checkout e finais de linha; não atualize o manifesto apenas para fazer a auditoria passar.

## Ler QPY sem executar circuitos

```python
from qiskit import qpy
from pathlib import Path

caminho = Path('quantum-mitigation/dados/simulados/validacao_2026_11_01/comparacao.qpy')
with caminho.open('rb') as arquivo:
    circuitos = qpy.load(arquivo)
print(len(circuitos))  # 40 circuitos armazenados
print(circuitos[0].count_ops())
```

Carregar QPY não envia um job. Os nomes semânticos e sua ordem estão no manifesto; não dependa apenas do nome automático de um objeto de circuito.

## Scripts que acessam a IBM

O [catálogo de scripts](../../../../scripts/README.md) distingue análise local de acesso remoto. Scripts históricos em `experimentos` geralmente executam submissão no corpo do arquivo; importá-los também pode executar esse corpo. Não use uma rotina que importe todos os arquivos Python para “testar” o repositório.

`repetir_mitigacao.py` separa `--verificar`, `--coletar` e `--enviar`. `--verificar` fica local, mas o arquivo importa Qiskit Runtime e exige que essa dependência esteja instalada. `--coletar` consulta um job registrado e pode regravar seu JSON quando concluído. `--enviar` cria um job real e recusa uma rodada já registrada. Não incluímos um comando de envio no roteiro de reprodução local. A rodada 3 já está concluída.

Antes de um experimento novo, será preciso conferir backend, conectividade, orçamento, versões e opções. Os requirements históricos não fixam versões; os ambientes de análise e simulação têm listas próprias. Não se deve assumir que scripts históricos funcionem sem revisão com qualquer versão futura do serviço.

## Problemas comuns

| Sintoma | O que conferir |
| --- | --- |
| `ModuleNotFoundError` | Se o executável Python pertence ao ambiente onde instalou os requirements |
| `FileExistsError` na simulação | Se o nome em `--execucao` já foi usado |
| Arquivo relativo não encontrado | Se o terminal está na raiz do checkout |
| Hash diferente | Integridade, finais de linha, versão do arquivo e pasta auditada |
| Calibração instável | Dados, contagens e modelo; não ignorar a exceção nem recortar estimativas para ocultá-la |
| QPY não carrega | Compatibilidade da versão do Qiskit com a que gerou o arquivo |

Não execute uma nova submissão para resolver um problema de leitura ou análise de resultados já salvos.

---

[← Anterior](../08-zne/README.md) · [Índice do livro](../../../../README.md) · [Próximo →](../10-codigo-dados/README.md)
