"""Testes da verificação de independência dos erros de leitura (experimento 8, parte B)."""
import sys
import unittest
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from mitigacao import leitura_independencia as li  # noqa: E402


class IndependenciaTest(unittest.TestCase):
    def test_erros_sao_o_xor_com_o_preparado(self):
        e = li.erros({'0011': 2, '1111': 1}, '0011')
        self.assertEqual(e.shape, (3, 4))
        self.assertEqual(e.tolist(), [[0, 0, 0, 0], [0, 0, 0, 0], [1, 1, 0, 0]])

    def test_excesso_so_aparece_quando_os_erros_vem_juntos(self):
        rng = np.random.default_rng(3)
        p = np.full(6, 0.05)
        indep = (rng.random((4000, 6)) < p).astype(int)
        junto = indep.copy()
        flip = rng.random(4000) < 0.05
        junto[:, 0] ^= flip
        junto[:, 1] ^= flip
        r_indep, r_junto = (li.teste(e, np.random.default_rng(4), 200) for e in (indep, junto))
        self.assertGreater(r_indep['p_valor'], 0.01)
        self.assertEqual(r_junto['p_valor'], 1 / 201)
        self.assertGreater(r_junto['T'], 5 * r_junto['nulo_dp'])
        self.assertEqual(li.pares_mais_ligados(junto, 1)[0][:2], (0, 1))

    def test_o_embaralhamento_mantem_a_taxa_de_erro(self):
        e = (np.random.default_rng(5).random((500, 4)) < 0.1).astype(int)
        self.assertAlmostEqual(li.teste(e, np.random.default_rng(6), 20)['taxa_de_erro'], e.mean())


if __name__ == '__main__':
    unittest.main()
