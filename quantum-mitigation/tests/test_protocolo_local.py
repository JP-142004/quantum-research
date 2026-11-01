"""Testes locais com alvos analíticos e regressão de mapeamento após SWAP."""
import sys
import unittest
from pathlib import Path

import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, ReadoutError

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from protocolo_local import (circuitos, compilar, validar_circuitos, ideal,
    esperado, corrigir, matriz_leitura, pesos, vetor, intercepto)
from validar_protocolo_local import conferir_referencia


class ProtocoloLocalTest(unittest.TestCase):
    def test_distribuicoes_e_roteamento(self):
        for zne, tamanho in [(False, 40), (True, 42)]:
            logicos = circuitos(zne)
            self.assertEqual(len(logicos), tamanho)
            validar_circuitos(logicos, compilar(logicos))

    def test_controle_negativo_e_paridade(self):
        p = ideal(circuitos()['controle_menos_X'])
        self.assertAlmostEqual(p[1], 1)
        self.assertAlmostEqual(pesos('controle_menos_X') @ p, -1)

    def test_canal_assimetrico_e_mapa(self):
        qc = QuantumCircuit(5, 5)
        qc.measure(range(5), range(5))
        a = matriz_leitura(qc, 'leitura')
        self.assertAlmostEqual(a[0, 0], .99*.98*.97*.96*.95)
        self.assertAlmostEqual(a[31, 31], .94*.95*.96*.97*.98)
        swapped = QuantumCircuit(5, 5)
        swapped.measure(range(5), [4, 1, 2, 3, 0])
        novo = matriz_leitura(swapped, 'leitura')
        self.assertAlmostEqual(novo[1, 0] / novo[0, 0], .05/.95)
        probs = np.column_stack([esperado('original_Z'), esperado('original_X')])
        np.testing.assert_allclose(corrigir(a, a @ probs), probs, atol=1e-12)
        refs = {f'cal_{i:05b}': {'observado': a[:, i]} for i in range(32)}
        comps = {nome: qc for nome in refs}
        comps['teste_X'] = swapped
        refs['teste_X'] = dict(observado=novo @ probs[:, 1], antes_leitura=probs[:, 1])
        self.assertLess(conferir_referencia(comps, refs, 'leitura'), 1e-12)

    def test_aer_convencao_leitura(self):
        # Canal determinístico assimétrico: todo estado observado como 1.
        modelo = NoiseModel()
        modelo.add_readout_error(ReadoutError([[0, 1], [0, 1]]), [0])
        qc = QuantumCircuit(1, 1)
        qc.measure(0, 0)
        counts = AerSimulator(noise_model=modelo).run(qc, shots=32, seed_simulator=7).result().get_counts()
        self.assertEqual(counts, {'1': 32})

    def test_invalido_e_singular(self):
        for counts in [{'0': 1000}, {'00000': -1}, {'00000': 999}, {'00000': 1000.0}]:
            with self.assertRaises(ValueError):
                vetor(counts, 1000)
        with self.assertRaises(ValueError):
            corrigir(np.ones((32, 32))/32, np.ones(32)/32)

    def test_extrapolacao_linear_e_identidade(self):
        np.testing.assert_allclose(intercepto(np.array([1, 3, 5])*.02 + .8), .8)
        p = np.column_stack([esperado('original_Z'), esperado('original_X')])
        np.testing.assert_allclose(corrigir(np.eye(32), p), p)


if __name__ == '__main__':
    unittest.main()
