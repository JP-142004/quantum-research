"""Testes do experimento 8, parte A (calibração por qubit em 10 qubits, no simulador)."""
import importlib.util
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from mitigacao import leitura_escala_saida as saida  # noqa: E402
from mitigacao.execucao.ruido import CENARIOS, CORRELACIONADO  # noqa: E402
from mitigacao.montagem import verificar_ideal  # noqa: E402
from mitigacao.sessao import montar_receita  # noqa: E402

PARTE_A = Path(__file__).resolve().parents[1] / 'experimentos' / '08_leitura_escala' / 'a_simulador'


def receita_a():
    spec = importlib.util.spec_from_file_location('receita_8a', PARTE_A / 'experimento.py')
    receita = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(receita)
    return receita


class ReceitaTest(unittest.TestCase):
    def test_sessoes_e_cenarios(self):
        r = receita_a()
        self.assertEqual(len(r.sessoes), 6)
        self.assertEqual({s['opcoes_envio']['cenario'] for s in r.sessoes}, {'leitura', CORRELACIONADO})
        self.assertEqual(len({s['semente'] for s in r.sessoes}), 6)
        self.assertNotIn(CORRELACIONADO, CENARIOS)   # o experimento 5 percorre CENARIOS e não pode mudar

    def test_circuitos_batem_com_o_ideal(self):
        r = receita_a()
        montados = montar_receita(r, 'simulador')
        self.assertEqual(len(montados), 2 + 1024 + 4)
        self.assertTrue(all(verificar_ideal(m) is not False for m in montados))

    def test_rotulos(self):
        self.assertEqual(saida.rotulo('leitura_bloco_01'), 'indep.\n1')
        self.assertEqual(saida.rotulo('leitura_correlacionada_bloco_03'), 'correl.\n3')


@unittest.skipUnless((PARTE_A / 'resultados' / 'resultados.json').exists(), 'resultados ainda não gerados')
class ResultadosTest(unittest.TestCase):
    """O que o relatório da parte A afirma, conferido nos resultados gerados dos dados."""

    def setUp(self):
        import json
        self.res = json.loads((PARTE_A / 'resultados' / 'resultados.json').read_text(encoding='utf-8'))

    def decisoes(self, filtro, par):
        return [d['diferencas'][par]['decisao'] for nome, r in self.res.items() if filtro(nome)
                for d in r['itens'] if d['circuito'] == 'ghz']

    def test_sem_correlacao_nenhuma_comparacao_deu_diferente(self):
        for par in ('fatorizado-completo', 'fatorizado_dois-completo'):
            self.assertNotIn('diferente', self.decisoes(lambda n: 'correlacionada' not in n, par))

    def test_com_correlacao_todas_deram_diferente(self):
        for par in ('fatorizado-completo', 'fatorizado_dois-completo'):
            self.assertEqual(set(self.decisoes(lambda n: 'correlacionada' in n, par)), {'diferente'})

    def test_a_matriz_completa_recupera_o_valor_verdadeiro_com_correlacao(self):
        for nome, r in self.res.items():
            for d in r['itens']:
                if d['circuito'] == 'ghz':
                    self.assertLess(abs(d['ajustado']['completo']['valor'] - 1), 0.07, nome)


if __name__ == '__main__':
    unittest.main()
