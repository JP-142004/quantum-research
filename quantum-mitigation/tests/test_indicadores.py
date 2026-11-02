"""Testes dos indicadores e do bootstrap, com os exemplos de fundamentos/indicadores.md."""
import sys
import unittest
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from mitigacao import estatistica, indicadores
from mitigacao.circuitos import ghz


def ideal_z(bits):
    return ghz.prob_ideal(bits, 5, 'Z')


class IndicadoresTest(unittest.TestCase):
    def test_exemplo_da_documentacao(self):
        # 477 zeros, 445 uns e 78 de outras sequências, em 1.000 shots
        contagens = {'00000': 477, '11111': 445, '00001': 50, '10000': 28}
        p = indicadores.fracoes(contagens)
        self.assertAlmostEqual(indicadores.probabilidade_sucesso(p, ideal_z), 0.922)
        self.assertAlmostEqual(indicadores.distancia_ideal(p, ideal_z), 0.078)

    def test_pz_e_cx(self):
        pz, cx = ghz.INDICADORES['PZ'], ghz.INDICADORES['CX']
        z = indicadores.fracoes({'00000': 454, '11111': 441, '00001': 105})
        self.assertAlmostEqual(indicadores.valor(z, pz['peso']), 0.895)
        x_pares = {f'{i:05b}': 0 for i in range(32)}
        x = indicadores.fracoes({'00000': 903, '00001': 97})
        self.assertAlmostEqual(indicadores.valor(x, cx['peso']), 0.806)
        self.assertEqual(len(x_pares), 32)

    def test_pz_igual_a_probabilidade_de_sucesso(self):
        p = indicadores.fracoes({'00000': 300, '11111': 500, '01010': 200})
        pz = indicadores.valor(p, ghz.INDICADORES['PZ']['peso'])
        self.assertAlmostEqual(pz, indicadores.probabilidade_sucesso(p, ideal_z))

    def test_distancia_ideal_extremos(self):
        self.assertAlmostEqual(indicadores.distancia_ideal(dict(zip(['00000', '11111'], [.5, .5])), ideal_z), 0)
        self.assertAlmostEqual(indicadores.distancia_ideal({'00001': 1.0}, ideal_z), 1.0)

    def test_erro_padrao_da_documentacao(self):
        self.assertAlmostEqual(indicadores.erro_padrao(0.895, 1000, 'fracao'), 0.0097, places=4)
        self.assertAlmostEqual(indicadores.erro_padrao(0.806, 1000, 'correlacao'), 0.0187, places=4)
        self.assertAlmostEqual(indicadores.erro_padrao_diferenca(0.0118, 0.0100), 0.0155, places=4)
        with self.assertRaises(ValueError):
            indicadores.erro_padrao(0.5, 10, 'outro')


class EstatisticaTest(unittest.TestCase):
    def test_reamostrar_mantem_o_total(self):
        rng = np.random.default_rng(1)
        novo = estatistica.reamostrar({'0': 700, '1': 300}, rng)
        self.assertEqual(sum(novo.values()), 1000)

    def test_bootstrap_bate_com_a_formula_analitica(self):
        contagens = {'a': {'0': 895, '1': 105}}
        replicas = estatistica.bootstrap(lambda c: c['a'].get('0', 0) / 1000, contagens, repeticoes=3000, semente=7)
        analitico = indicadores.erro_padrao(0.895, 1000, 'fracao')
        self.assertAlmostEqual(estatistica.resumo(replicas)['erro_padrao'], analitico, delta=0.1 * analitico)

    def test_bootstrap_e_reprodutivel(self):
        contagens = {'a': {'0': 600, '1': 400}}
        f = lambda c: c['a'].get('0', 0)  # noqa: E731
        a = estatistica.bootstrap(f, contagens, repeticoes=50, semente=3)
        b = estatistica.bootstrap(f, contagens, repeticoes=50, semente=3)
        np.testing.assert_array_equal(a, b)

    def test_intervalo_contem_o_valor(self):
        replicas = estatistica.bootstrap(lambda c: c['a'].get('0', 0) / 1000, {'a': {'0': 500, '1': 500}},
                                         repeticoes=500, semente=1)
        inferior, superior = estatistica.resumo(replicas)['ic95']
        self.assertLess(inferior, 0.5)
        self.assertGreater(superior, 0.5)


if __name__ == '__main__':
    unittest.main()
