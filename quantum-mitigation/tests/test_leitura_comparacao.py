"""Testes do experimento 7 (calibração de leitura completa contra os modelos por qubit)."""
import contextlib
import io
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from mitigacao import leitura_comparacao as lc, leitura_saida  # noqa: E402

RAIZ = Path(__file__).resolve().parents[1] / 'experimentos'
DADOS_4 = RAIZ / '04_calibracao_leitura'
TEM_DADOS = (DADOS_4 / 'dados').exists()


class DecisaoTest(unittest.TestCase):
    def test_tres_resultados_possiveis(self):
        self.assertEqual(lc.decisao([-0.008, 0.012]), 'equivalente')
        self.assertEqual(lc.decisao([-0.03, 0.025]), 'inconclusivo')
        self.assertEqual(lc.decisao([0.025, 0.04]), 'diferente')
        self.assertEqual(lc.decisao([-0.05, -0.021]), 'diferente')

    def test_a_margem_e_inclusiva_e_vem_do_registro(self):
        self.assertEqual(lc.MARGEM, 0.02)
        self.assertEqual(lc.decisao([-0.02, 0.02]), 'equivalente')
        self.assertEqual(lc.SEMENTE_DIVISAO, 20261122)


@unittest.skipUnless(TEM_DADOS, 'sem os dados do experimento 4')
class SobreOsDadosDoExperimento4Test(unittest.TestCase):
    sessao = DADOS_4 / 'dados' / '2026-11-08_ibm_fez'

    def test_o_ajuste_completo_repete_o_do_experimento_4(self):
        r = lc.comparar(self.sessao, repeticoes=20)
        antigo = json.loads((DADOS_4 / 'resultados' / 'resultados.json').read_text(encoding='utf-8'))[self.sessao.name]
        for d in r['itens']:
            esperado = antigo['itens'][d['nome']]['ajustado']['valor']
            self.assertAlmostEqual(d['ajustado']['completo']['valor'], esperado, places=9, msg=d['nome'])

    def test_mesma_semente_mesmo_resultado(self):
        a, b = lc.comparar(self.sessao, repeticoes=10), lc.comparar(self.sessao, repeticoes=10)
        self.assertEqual(a, b)

    def test_estrutura_do_resultado(self):
        r = lc.comparar(self.sessao, repeticoes=10)
        self.assertEqual(len(r['itens']), 6)   # GHZ em Z e X e os 4 controles
        self.assertEqual(set(r['previsao']), set(lc.MODELOS))
        d = r['itens'][0]
        self.assertEqual(set(d['diferencas']), {f'{a}-{b}' for a, b in lc.COMPARACOES})
        self.assertIn(d['diferencas']['fatorizado-completo']['decisao'], {'equivalente', 'diferente', 'inconclusivo'})

    def test_gerar_grava_resultados_e_nao_toca_nos_dados(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        pasta = Path(tmp.name) / '07_teste'
        pasta.mkdir()
        shutil.copy(RAIZ / '07_leitura_fatorizada' / 'README.md', pasta / 'README.md')
        antes = sorted((p, p.stat().st_mtime_ns) for p in (DADOS_4 / 'dados').rglob('*') if p.is_file())
        with contextlib.redirect_stdout(io.StringIO()):
            saida = leitura_saida.gerar(pasta, DADOS_4, 10)
        self.assertEqual(len(saida['sessoes']), 3)
        for nome in ('resultados.json', 'tabelas.md', 'comparacao_leitura.png'):
            self.assertTrue((pasta / 'resultados' / nome).exists(), nome)
        self.assertNotIn('<!-- TABELA:metodos -->\n<!--', (pasta / 'README.md').read_text(encoding='utf-8'))
        depois = sorted((p, p.stat().st_mtime_ns) for p in (DADOS_4 / 'dados').rglob('*') if p.is_file())
        self.assertEqual(antes, depois)


if __name__ == '__main__':
    unittest.main()
