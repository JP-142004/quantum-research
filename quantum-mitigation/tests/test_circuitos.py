"""Testes dos circuitos. O primeiro teste percorre TODOS os circuitos registrados, então um
circuito novo é testado sem escrever teste novo (basta declarar EXEMPLOS no módulo dele)."""
import sys
import unittest
from itertools import product
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from mitigacao import circuitos
from mitigacao.montagem import montar, verificar_ideal
from mitigacao.topologia import vizinhos_linha


class CircuitosTest(unittest.TestCase):
    def test_todos_os_circuitos_batem_com_o_ideal_declarado(self):
        self.assertTrue(circuitos.listar())
        for nome in circuitos.listar():
            modulo = circuitos.obter(nome)
            self.assertTrue(modulo.EXEMPLOS, f'{nome} precisa declarar EXEMPLOS')
            for (n, variante), base in product(modulo.EXEMPLOS, ('Z', 'X')):
                itens = [dict(circuito=nome, n=n, variante=variante, base=base)]
                with self.subTest(circuito=nome, n=n, variante=variante, base=base):
                    montado = montar(itens, vizinhos_linha)[0]
                    self.assertTrue(verificar_ideal(montado))

    def test_a_verificacao_pega_um_circuito_errado(self):
        montado = montar([dict(circuito='ghz', n=5, variante='original')], vizinhos_linha)[0]
        self.assertTrue(verificar_ideal(montado))
        # tira a última porta: o circuito passa a produzir outro estado
        errado = montado['circuito'].copy_empty_like()
        for instrucao in montado['circuito'].data:
            if not (instrucao.operation.name == 'cx' and instrucao.qubits[1] == montado['circuito'].qubits[4]):
                errado.append(instrucao.operation, instrucao.qubits, instrucao.clbits)
        self.assertFalse(verificar_ideal(dict(montado, circuito=errado)))
        # um estado simples com o bit trocado também é pego
        simples = montar([dict(circuito='simples', n=3, variante='010')], vizinhos_linha)[0]
        trocado = dict(simples, item=dict(simples['item'], variante='011'))
        self.assertFalse(verificar_ideal(trocado))

    def test_prob_ideal_soma_um(self):
        for nome in circuitos.listar():
            modulo = circuitos.obter(nome)
            for (n, variante), base in product(modulo.EXEMPLOS, ('Z', 'X')):
                if n > 6:
                    continue
                soma = sum(modulo.prob_ideal(f'{i:0{n}b}', n, base, variante) for i in range(2 ** n))
                self.assertAlmostEqual(soma, 1.0, msg=f'{nome} {n} {variante} {base}')

    def test_ghz_prob_ideal_com_50_qubits_sem_enumerar(self):
        ghz = circuitos.obter('ghz')
        self.assertEqual(ghz.prob_ideal('0' * 50, 50, 'Z', 'original'), 0.5)
        self.assertEqual(ghz.prob_ideal('0' * 49 + '1', 50, 'Z', 'original'), 0.0)
        self.assertEqual(ghz.prob_ideal('0' * 48 + '11', 50, 'X', 'original'), 2.0 ** -49)
        self.assertEqual(ghz.prob_ideal('0' * 49 + '1', 50, 'X', 'original'), 0.0)

    def test_ghz_numero_de_portas(self):
        original = circuitos.construir(dict(circuito='ghz', n=5, variante='original'))
        conectado = circuitos.construir(dict(circuito='ghz', n=5, variante='conectado'),
                                        arestas=[(2, 1), (2, 3), (1, 0), (3, 4)])
        self.assertEqual(original.count_ops()['cx'], 4)
        self.assertEqual(conectado.count_ops()['cx'], 4)
        triplo = circuitos.construir(dict(circuito='ghz', n=5, variante='conectado', fator=3),
                                     arestas=[(2, 1), (2, 3), (1, 0), (3, 4)])
        self.assertEqual(triplo.count_ops()['cx'], 12)

    def test_conectado_exige_arestas(self):
        with self.assertRaises(ValueError):
            circuitos.construir(dict(circuito='ghz', n=5, variante='conectado'))

    def test_simples_ordem_dos_bits(self):
        # o símbolo da direita é o qubit 0
        simples = circuitos.obter('simples')
        self.assertEqual(simples.prob_ideal('00001', 5, 'Z', '00001'), 1.0)
        self.assertEqual(simples.prob_ideal('00001', 5, 'X', '++++-'), 1.0)
        self.assertEqual(simples.prob_ideal('00000', 5, 'X', '++++-'), 0.0)

    def test_itens_invalidos(self):
        for ruim in (dict(circuito='ghz', n=5, base='Y'), dict(circuito='ghz', n=5, fator=2)):
            with self.assertRaises(ValueError):
                circuitos.completar(ruim)

    def test_nomes_dos_itens_sao_unicos(self):
        itens = [dict(circuito='simples', n=1, variante=v, qubits=[q]) for v in '01' for q in range(3)]
        nomes = {circuitos.nome_item(i) for i in itens}
        self.assertEqual(len(nomes), 6)


if __name__ == '__main__':
    unittest.main()
