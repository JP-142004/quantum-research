# 11. Histórico, conclusões e próximos passos

[← Anterior](../10-codigo-dados/README.md) · [Índice do livro](../../../../README.md) · [Próximo →](../12-glossario-fontes/README.md)

## O que já existia

O repositório já tinha a estrutura das duas frentes, o script de modelagem e os resultados de linha de base de GHZ de 5 a 50 qubits. O README da modelagem identifica João Paulo como responsável. A organização da frente de mitigação preservou essa área; não implementou o ajuste evolutivo mencionado como direção futura.

## O que foi organizado e acrescentado

| Commit | Conteúdo |
| --- | --- |
| `d798852` | Organização dos arquivos de mitigação, dados e inventário de importação |
| `958a680` | Programa de repetição e registro do envio da rodada 3 |
| `daa2b2f` | Resultados concluídos da rodada 3 |
| `e2fea3b` | Comparação de três rodadas, gráficos, resumo e plano |
| `1e21d5a` | Protocolo local, controles, piloto ZNE e testes |
| `8ff5086` | Resultados simulados, auditoria e registro de trabalho |

Os três primeiros foram trazidos de outra cópia local para a cópia do Desktop. As alterações preparadas no Desktop eram idênticas ao primeiro commit; um stash local preservou esse estado. Stash é um backup local e não acompanha automaticamente um clone do GitHub.

Os seis commits foram publicados na branch `mitigation` após autorização. A branch `main` não recebeu merge por essa operação. O [registro de trabalho](../../registro_trabalho.md) contém o histórico detalhado; o texto sobre ausência de push foi contextualizado para separar a etapa local da publicação posterior. O histórico Git inclui a revisão documental de 2 de novembro de 2026 após os commits da tabela.

## Conclusões sustentadas

1. Nos três registros reais de cinco qubits, a mitigação de leitura aumenta PZ e CX. O efeito do estimador é consistente em sinal nesse conjunto, com incerteza de amostragem estimada.
2. No modelo local, a inversão recupera a distribuição anterior à leitura dentro da precisão numérica dos testes exatos. Isso não remove o canal de ruído de portas que foi aplicado antes.
3. Nesse modelo de portas, a construção conectada tem indicadores melhores que a original, coerente com sua menor quantidade de operações ruidosas.
4. O piloto ZNE local permite estudar extrapolação, viés e variância; não demonstra desempenho de ZNE na IBM.

## Afirmações que os registros não sustentam

Não medimos a fidelidade completa do GHZ. Não demonstramos a eliminação dos erros de portas. Não caracterizamos todos os tipos de ruído do Fez. Não temos arquivos brutos de todos os controles históricos ou de GHZ conectado de 50 qubits. Não demonstramos estabilidade temporal com três rodadas e metadados históricos incompletos. Os 486.000 shots locais não são novas medidas reais da IBM.

## Próximo experimento proposto

O [plano](../../../plano_experimentos.md) propõe três blocos reais com calibração comum por bloco, duas construções em Z/X e controles independentes: 40 circuitos × 1.000 shots × 3 = 120.000 medidas. A simulação desse formato foi realizada, mas sua submissão real continua pendente.

Antes do hardware, é necessário selecionar um backend disponível, verificar conexões e propriedades, compilar para suas instruções reais e revisar o orçamento. As opções e os limites do código histórico não são garantia de compatibilidade futura. O novo executor local não inclui uma implementação de envio desse protocolo de 40 circuitos.

O piloto ZNE futuro seria outro protocolo, de 42 circuitos por bloco e 126.000 medidas em três blocos. Só deve ser interpretado depois de examinar controles e sensibilidade ao modelo. Esses números são orçamentos de amostras, não estimativas de tempo ou custo de QPU.

## Como registrar a continuidade

Cada novo conjunto deve registrar objetivo, origem, backend ou simulador, qubits, circuitos compilados, opções, sementes, versões, horários, contagens e análise. Falhas e decisões de exclusão também devem ser registradas. Não reutilize um nome de execução concluída para outro experimento e não misture dados simulados com dados reais.

O que muda na documentação deve acompanhar o que muda no código e nos dados. Um resultado novo precisa entrar no índice e nos relatórios; uma hipótese ou plano deve continuar identificado como tal até ser executado.

---

[← Anterior](../10-codigo-dados/README.md) · [Índice do livro](../../../../README.md) · [Próximo →](../12-glossario-fontes/README.md)
