"""Testes do registro das sessões: gravar uma vez, nunca sobrescrever."""
import json
import sys
import tempfile
import unittest
from pathlib import Path

from qiskit import QuantumCircuit

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from mitigacao import registro


class RegistroTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.pasta = Path(self.tmp.name) / 'dados' / '2026-11-10_teste'
        self.circuito = QuantumCircuit(1, 1)
        self.circuito.measure(0, 0)

    def tearDown(self):
        self.tmp.cleanup()

    def test_gravar_novo_recusa_sobrescrever(self):
        arquivo = Path(self.tmp.name) / 'a.txt'
        registro.gravar_novo(arquivo, 'um')
        with self.assertRaises(FileExistsError):
            registro.gravar_novo(arquivo, 'dois')
        self.assertEqual(arquivo.read_text(encoding='utf-8'), 'um')
        self.assertFalse((Path(self.tmp.name) / 'a.txt.tmp').exists())

    def test_sessao_completa(self):
        registro.registrar_envio(self.pasta, dict(job_id='j1', shots=10), [self.circuito])
        ficha, contagens = registro.ler_sessao(self.pasta)
        self.assertEqual(ficha['job_id'], 'j1')
        self.assertIsNone(contagens)
        registro.registrar_coleta(self.pasta, {'a': {'0': 6, '1': 4}}, 10)
        self.assertEqual(registro.ler_sessao(self.pasta)[1], {'a': {'0': 6, '1': 4}})
        self.assertEqual(registro.listar_sessoes(self.pasta.parent.parent), [self.pasta])

    def test_nao_reenvia_nem_recoleta(self):
        registro.registrar_envio(self.pasta, dict(job_id='j1', shots=10), [self.circuito])
        with self.assertRaises(FileExistsError):
            registro.registrar_envio(self.pasta, dict(job_id='j2', shots=10), [self.circuito])
        registro.registrar_coleta(self.pasta, {'a': {'0': 10}}, 10)
        with self.assertRaises(FileExistsError):
            registro.registrar_coleta(self.pasta, {'a': {'1': 10}}, 10)
        self.assertEqual(json.loads((self.pasta / 'ficha.json').read_text(encoding='utf-8'))['job_id'], 'j1')

    def test_contagens_invalidas(self):
        for ruim in ({'a': {'0': 9}}, {'a': {'0': 5.0, '1': 5}}, {'a': {'0': 5, '11': 5}},
                     {'a': {'x': 10}}, {'a': {'0': -1, '1': 11}}):
            with self.assertRaises(ValueError, msg=str(ruim)):
                registro.validar_contagens(ruim, 10)

    def test_listar_sem_dados(self):
        self.assertEqual(registro.listar_sessoes(Path(self.tmp.name) / 'inexistente'), [])


if __name__ == '__main__':
    unittest.main()
