"""Testes da topologia e das técnicas (calibração de leitura e ZNE)."""
import sys
import unittest
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from mitigacao import tecnicas
from mitigacao.circuitos import nome_item
from mitigacao.tecnicas import leitura, zne
from mitigacao.topologia import escolher_qubits, vizinhos_linha


def matriz_produto(e01, e10):
    """Matriz de leitura de qubits independentes. Estados indexados com o qubit 0 no bit menos significativo."""
    n = len(e01)
    a = np.ones((2 ** n, 2 ** n))
    for q in range(n):
        erro = np.array([[1 - e01[q], e10[q]], [e01[q], 1 - e10[q]]])
        for obs in range(2 ** n):
            for ver in range(2 ** n):
                a[obs, ver] *= erro[(obs >> q) & 1, (ver >> q) & 1]
    return a


class TopologiaTest(unittest.TestCase):
    def test_linha_com_raiz_no_meio(self):
        fisicos, arestas = escolher_qubits(vizinhos_linha(5), 5, 2)
        self.assertEqual(fisicos, [0, 1, 2, 3, 4])
        self.assertEqual(arestas, [(2, 1), (2, 3), (1, 0), (3, 4)])

    def test_subconjunto_e_indices_logicos(self):
        fisicos, arestas = escolher_qubits(vizinhos_linha(20), 3, 10)
        self.assertEqual(fisicos, [9, 10, 11])
        self.assertEqual(arestas, [(1, 0), (1, 2)])

    def test_erros(self):
        with self.assertRaises(RuntimeError):
            escolher_qubits(vizinhos_linha(3), 5, 1)
        with self.assertRaises(ValueError):
            escolher_qubits(vizinhos_linha(3), 2, 9)
        self.assertEqual(escolher_qubits(vizinhos_linha(3), 1, 1), ([1], []))


class LeituraTest(unittest.TestCase):
    def test_exemplo_de_um_qubit_da_documentacao(self):
        a = np.array([[0.90, 0.20], [0.10, 0.80]])
        q, diag = leitura.corrigir(a, {'0': 0.55, '1': 0.45})
        self.assertAlmostEqual(q['0'], 0.5)
        self.assertAlmostEqual(q['1'], 0.5)
        self.assertAlmostEqual(diag['soma'], 1.0)

    def test_recupera_a_distribuicao_verdadeira(self):
        a = matriz_produto([0.01, 0.02, 0.03], [0.06, 0.05, 0.04])
        verdadeira = np.zeros(8)
        verdadeira[0] = verdadeira[7] = 0.5
        observada = a @ verdadeira
        q, _ = leitura.corrigir(a, {f'{i:03b}': float(v) for i, v in enumerate(observada)})
        np.testing.assert_allclose([q[f'{i:03b}'] for i in range(8)], verdadeira, atol=1e-12)

    def test_matriz_a_partir_das_contagens(self):
        e01, e10 = [0.01, 0.05], [0.05, 0.01]
        analitica = matriz_produto(e01, e10)
        contagens = {}
        for j in range(4):
            coluna = analitica[:, j] * 10000
            self.assertTrue(np.allclose(coluna, np.round(coluna)))
            contagens[nome_item(leitura._item(2, f'{j:02b}'))] = {f'{i:02b}': int(round(v))
                                                                 for i, v in enumerate(coluna) if round(v)}
        np.testing.assert_allclose(leitura.matriz(contagens, 2), analitica, atol=1e-12)

    def test_mapa_de_medidas_com_troca_de_qubits(self):
        a = matriz_produto([0.01, 0.08], [0.02, 0.10])  # índice = estado por qubit físico
        mapa = [(0, 1), (1, 0)]                         # o qubit físico 0 é lido no bit 1 e vice-versa
        perm = leitura._permutacao(mapa, 2)
        verdadeira_fisica = np.array([0.1, 0.2, 0.3, 0.4])
        observada_fisica = a @ verdadeira_fisica
        p_cl, q_cl = np.zeros(4), np.zeros(4)
        for s in range(4):
            p_cl[perm[s]], q_cl[perm[s]] = observada_fisica[s], verdadeira_fisica[s]
        q, _ = leitura.corrigir(a, {f'{i:02b}': float(v) for i, v in enumerate(p_cl)}, mapa)
        np.testing.assert_allclose([q[f'{i:02b}'] for i in range(4)], q_cl, atol=1e-12)

    def test_calibracao_instavel_e_modelo_nao_implementado(self):
        with self.assertRaises(ValueError):
            leitura.corrigir(np.ones((4, 4)) / 4, {'00': 1.0})
        with self.assertRaises(NotImplementedError):
            leitura.matriz({}, 2, modelo='fatorizado')

    def test_itens_de_calibracao(self):
        itens = leitura.itens_calibracao(5)
        self.assertEqual(len(itens), 32)
        self.assertEqual(len({nome_item(i) for i in itens}), 32)


class ZneTest(unittest.TestCase):
    def test_pesos_do_intercepto(self):
        np.testing.assert_allclose(zne.pesos_intercepto((1, 3, 5)), [13 / 12, 1 / 3, -5 / 12])

    def test_reta_exata_e_exemplo_da_documentacao(self):
        self.assertAlmostEqual(float(zne.extrapolar(np.array([1, 3, 5]) * -0.02 + 0.9)), 0.9)
        self.assertAlmostEqual(float(zne.extrapolar([0.9463, 0.8490, 0.7637])), 0.9898, places=3)

    def test_replicas_em_lote(self):
        lote = np.tile([0.9463, 0.8490, 0.7637], (4, 1))
        self.assertEqual(zne.extrapolar(lote).shape, (4,))
        with self.assertRaises(ValueError):
            zne.extrapolar([1, 2])

    def test_expandir(self):
        itens = zne.expandir([dict(circuito='ghz', n=5), dict(circuito='ghz', n=3)])
        self.assertEqual([i['fator'] for i in itens], [1, 3, 5, 1, 3, 5])


class RegistroDeTecnicasTest(unittest.TestCase):
    def test_todas_tem_nome(self):
        for nome in tecnicas.listar():
            self.assertEqual(tecnicas.obter(nome).NOME, nome)


if __name__ == '__main__':
    unittest.main()
