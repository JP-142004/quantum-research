"""Testes da análise. O teste central: com as probabilidades exatas do modelo (sem flutuação
de shots), a correção de leitura tem de devolver exatamente o estado anterior à leitura."""
import contextlib
import io
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from mitigacao import analise, sessao
from mitigacao.execucao import info_compilado, simulador
from mitigacao.execucao.ruido import referencia_exata
from mitigacao.montagem import montar
from mitigacao.tecnicas import leitura, zne

from auxiliar import Q5, itens_basicos, vizinhos_sim  # noqa: E402

class CorrecaoExataTest(unittest.TestCase):
    def test_correcao_recupera_o_estado_anterior_a_leitura(self):
        for cenario in ('leitura', 'leitura_e_portas'):
            montados = montar(itens_basicos(), vizinhos_sim)
            job = simulador.enviar(montados, 10, 1, cenario=cenario)   # só para compilar
            ref = referencia_exata(job['compilados'], cenario)
            cal = leitura.itens_calibracao(5, qubits=Q5)
            from mitigacao.circuitos import nome_item
            a = np.column_stack([ref[nome_item(i)]['observado'] for i in cal])
            nomes = [m['nome'] for m in montados if 'simples_5q' not in m['nome'] or 'controle' in m['nome']]
            perms = [leitura.permutacao(info_compilado(job['compilados'][n])['mapa_medidas'], 5) for n in nomes]
            p = np.array([ref[n]['observado'] for n in nomes])
            q = leitura.corrigir_varios(a, p, perms)
            for j, n in enumerate(nomes):
                np.testing.assert_allclose(q[j], ref[n]['antes_leitura'], atol=1e-10, err_msg=f'{cenario} {n}')

    def test_corrigir_varios_equivale_a_corrigir(self):
        rng = np.random.default_rng(3)
        a = np.eye(4) * 0.9 + 0.1 / 4
        p = rng.dirichlet(np.ones(4), size=2)
        mapas = [[(0, 1), (1, 0)], [(0, 0), (1, 1)]]
        perms = [leitura.permutacao(m, 2) for m in mapas]
        em_lote = leitura.corrigir_varios(a, p, perms)
        for j in range(2):
            q, _ = leitura.corrigir(a, {f'{i:02b}': float(v) for i, v in enumerate(p[j])}, mapas[j])
            np.testing.assert_allclose(em_lote[j], [q[f'{i:02b}'] for i in range(4)], atol=1e-12)


class SessaoCompletaTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)

    def sessao(self, itens, cenario, semente=11):
        receita = SimpleNamespace(pergunta='teste', execucao='simulador', shots=1000)
        pasta_exp = Path(self.tmp.name) / 'experimentos' / '99_teste'
        pasta = pasta_exp / 'dados' / f'{cenario}_{semente}'
        montados = montar(itens, vizinhos_sim)
        with contextlib.redirect_stdout(io.StringIO()):
            sessao.enviar_e_gravar(pasta, pasta_exp, receita, montados, 'simulador', semente, dict(cenario=cenario))
        return pasta

    def test_cenario_ideal_nao_muda_nada(self):
        r = analise.analisar(self.sessao(itens_basicos(), 'ideal'), ('leitura',), repeticoes=100)
        for d in r['itens'].values():
            self.assertAlmostEqual(d['bruto']['valor'], 1.0, places=9)
            self.assertAlmostEqual(d['ajustado']['valor'], 1.0, places=9)
        self.assertAlmostEqual(r['condicionamento'], 1.0)
        self.assertTrue(r['validacao']['aprovado'])

    def test_leitura_ajustado_fica_perto_do_exato_antes_da_leitura(self):
        r = analise.analisar(self.sessao(itens_basicos(), 'leitura'), ('leitura',), repeticoes=300)
        self.assertTrue(r['validacao']['aprovado'], r['validacao'])
        for d in r['itens'].values():
            self.assertLess(d['bruto']['valor'], d['referencia']['antes_leitura'] + 1e-9)  # a leitura só piora o bruto
            self.assertGreater(d['ganho']['valor'], 0)
            self.assertGreater(d['ganho']['ic95'][0], 0)
        self.assertEqual(len(r['contrastes']), 2)  # conectado menos original, em Z e em X
        self.assertGreater(r['contrastes'][0]['ajustado']['ep'], 0)

    def test_portas_com_ruido_deixam_o_ajustado_longe_de_um(self):
        r = analise.analisar(self.sessao(itens_basicos(), 'leitura_e_portas'), ('leitura',), repeticoes=300)
        original = r['itens']['ghz_5q_original_Z']
        self.assertLess(original['ajustado']['valor'], 0.92)           # o erro das portas não some
        self.assertAlmostEqual(original['referencia']['antes_leitura'], 0.8409, places=3)
        conectado = r['itens']['ghz_5q_conectado_Z']
        self.assertGreater(conectado['ajustado']['valor'], original['ajustado']['valor'])

    def test_zne_extrapola_para_perto_da_referencia(self):
        r = analise.analisar(self.sessao(itens_basicos(True), 'leitura_e_portas'), ('leitura', 'zne'), repeticoes=300)
        self.assertEqual(len(r['zne']), 2)
        z = next(g for g in r['zne'] if g['base'] == 'Z')
        self.assertAlmostEqual(z['referencia']['zne'], 0.9898, places=3)
        self.assertLess(abs(z['zne']['valor'] - z['referencia']['zne']), 6 * z['zne']['ep'])
        self.assertGreater(z['zne']['ep'], 0)
        self.assertEqual(len(z['ajustado_por_fator']), 3)

    def test_sem_calibracao_so_ha_valores_brutos(self):
        itens = [dict(circuito='ghz', n=n, variante='original') for n in (3, 5)]
        r = analise.analisar(self.sessao(itens, 'leitura'), (), repeticoes=10)
        self.assertIsNone(r['condicionamento'])
        for d in r['itens'].values():
            self.assertIsNone(d['ajustado'])
            self.assertGreater(d['bruto']['ep'], 0)

    def test_calibracao_incompleta_e_recusada(self):
        itens = itens_basicos()
        itens = [i for i in itens if i.get('variante') != '10101']
        with self.assertRaises(ValueError):
            analise.analisar(self.sessao(itens, 'leitura'), ('leitura',), repeticoes=10)

    def test_sessao_sem_contagens(self):
        pasta = self.sessao([dict(circuito='ghz', n=3, variante='original')], 'ideal')
        (pasta / 'contagens.json').unlink()
        with self.assertRaises(ValueError):
            analise.analisar(pasta, (), repeticoes=10)

    def test_e_calibracao(self):
        base = dict(circuito='simples', n=5, variante='01010', base='Z', rotulo=None)
        self.assertTrue(analise.e_calibracao(base))
        self.assertFalse(analise.e_calibracao(dict(base, rotulo='controle')))
        self.assertFalse(analise.e_calibracao(dict(base, variante='0+010')))
        self.assertFalse(analise.e_calibracao(dict(base, n=1, variante='0')))


if __name__ == '__main__':
    unittest.main()
