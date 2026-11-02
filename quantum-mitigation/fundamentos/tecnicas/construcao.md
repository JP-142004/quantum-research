# Construção com menos portas

**Ideia.** O mesmo estado pode ser preparado por sequências diferentes de portas. Se uma sequência exige CX entre qubits que não são vizinhos no computador, o compilador insere portas extras. Escolher a sequência que segue as ligações físicas reduz as portas executadas.

**Por que ajuda.** Se cada porta de dois qubits tivesse 1% de chance de erro (valor só ilustrativo), a chance de nenhuma dar erro em 13 portas seria 0,99¹³ ≈ 0,88, e em 4 portas, 0,99⁴ ≈ 0,96. Menos portas, menos chances de erro.

**No projeto.** É uma **variante do circuito**, não um código à parte: o GHZ tem a variante `original` (o qubit 0 liga a todos) e a `conectada` (árvore a partir de um qubit raiz, seguindo as ligações do computador). Comparam-se as duas no mesmo job ([circuitos/ghz.md](../circuitos/ghz.md)). Numa execução anterior do projeto, com 5 qubits no `ibm_fez`, o original ficou com 13 portas de dois qubits depois de compilado e o conectado com 4.

**Limite.** Reduz o erro das portas, mas não o elimina. Também não separa o efeito das portas do da profundidade e do tempo de espera dos qubits, porque os três mudam juntos.

[Técnicas](README.md)
