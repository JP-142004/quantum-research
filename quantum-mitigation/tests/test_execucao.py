"""Testes da execução: simulador local e a regra de importar o IBM só quando necessário."""
import sys
import unittest
from pathlib import Path

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, ReadoutError

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from mitigacao.execucao import embaralhar, ibm, ruido, simulador
from mitigacao.montagem import montar


def montados(itens):
    return montar(itens, lambda n: simulador.vizinhos('simulador', n))


class ExecucaoTest(unittest.TestCase):
    def test_ibm_nao_importa_o_runtime_ao_ser_carregado(self):
        self.assertNotIn('qiskit_ibm_runtime', sys.modules)
        self.assertFalse(ibm.INSTANTANEO)
        self.assertEqual(ibm.OPCOES, dict(dd=False, twirling_gates=False, twirling_measure=False, init_qubits=True))

    def test_convencao_de_leitura_do_aer(self):
        modelo = NoiseModel()
        modelo.add_readout_error(ReadoutError([[0, 1], [0, 1]]), [0])  # sempre lê 1
        qc = QuantumCircuit(1, 1)
        qc.measure(0, 0)
        contagens = AerSimulator(noise_model=modelo).run(qc, shots=32, seed_simulator=7).result().get_counts()
        self.assertEqual(contagens, {'1': 32})

    def test_cenarios_de_ruido(self):
        with self.assertRaises(ValueError):
            ruido.modelo_ruido('outro', 5)
        self.assertEqual(len(ruido.modelo_ruido('ideal', 5).noise_instructions), 0)
        self.assertIn('cx', ruido.modelo_ruido('leitura_e_portas', 5).noise_instructions)

    def test_embaralhar_e_reprodutivel(self):
        nomes = [f'c{i}' for i in range(20)]
        self.assertEqual(embaralhar(nomes, 1), embaralhar(nomes, 1))
        self.assertEqual(sorted(embaralhar(nomes, 1)), sorted(nomes))
        self.assertNotEqual(embaralhar(nomes, 1), embaralhar(nomes, 2))

    def test_simulador_ideal_so_devolve_resultados_ideais(self):
        itens = [dict(circuito='ghz', n=3, variante='original'), dict(circuito='simples', n=3, variante='101')]
        job = simulador.enviar(montados(itens), 200, 5, cenario='ideal')
        for nome, contagens in simulador.coletar(job).items():
            self.assertEqual(sum(contagens.values()), 200)
        self.assertEqual(set(job['contagens']['simples_3q_101_Z']), {'101'})
        self.assertLessEqual(set(job['contagens']['ghz_3q_original_Z']), {'000', '111'})

    def test_simulador_e_reprodutivel(self):
        itens = [dict(circuito='simples', n=3, variante='000')]
        a = simulador.enviar(montados(itens), 500, 11, cenario='leitura')
        b = simulador.enviar(montados(itens), 500, 11, cenario='leitura')
        self.assertEqual(a['contagens'], b['contagens'])

    def test_leitura_introduz_erros(self):
        job = simulador.enviar(montados([dict(circuito='simples', n=3, variante='000')]), 1000, 3, cenario='leitura')
        contagens = job['contagens']['simples_3q_000_Z']
        self.assertGreater(len(contagens), 1)
        self.assertGreater(contagens['000'], 800)

    def test_conectado_sem_troca_e_original_com_portas_extras(self):
        itens = [dict(circuito='ghz', n=5, variante=v) for v in ('original', 'conectado')]
        job = simulador.enviar(montados(itens), 100, 2, cenario='ideal')
        original, conectado = (job['info'][f'ghz_5q_{v}_Z']['portas_2q'] for v in ('original', 'conectado'))
        self.assertEqual(conectado, 4)
        self.assertGreater(original, conectado)
        self.assertEqual(job['info']['ghz_5q_conectado_Z']['mapa_medidas'], [(q, q) for q in range(5)])

    def test_ficha_do_job(self):
        job = simulador.enviar(montados([dict(circuito='simples', n=2, variante='01')]), 50, 9, cenario='ideal')
        self.assertEqual(job['job_id'], 'simulador-9')
        self.assertEqual(job['opcoes']['cenario'], 'ideal')
        self.assertEqual(list(job['compilados']), job['ordem'])


if __name__ == '__main__':
    unittest.main()
