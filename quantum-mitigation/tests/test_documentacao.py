"""Testes da documentação: tabelas geradas, links e números citados no texto.

Não usam Qiskit nem acessam a IBM. Executar a partir da raiz do repositório:
    python -m unittest discover -s quantum-mitigation/tests -v
"""
import csv
import json
import subprocess
import sys
import unittest
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
SCRIPTS = BASE / 'scripts'
sys.path.insert(0, str(SCRIPTS))
import gerar_tabelas  # noqa: E402


def executar(script, *args):
    return subprocess.run([sys.executable, str(SCRIPTS / script), *args], capture_output=True, text=True)


class DocumentacaoTest(unittest.TestCase):
    def test_tabelas_atualizadas(self):
        r = executar('gerar_tabelas.py', '--verificar')
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_links_relativos(self):
        r = executar('verificar_links.py')
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_numeros_do_texto_vem_dos_dados(self):
        artigo = (BASE / 'docs/relatorio.md').read_text(encoding='utf-8')
        escala = list(csv.DictReader(open(BASE / 'dados/processados/resumo_escala.csv', encoding='utf-8')))
        self.assertEqual(escala[0]['populacao_z'], '0.922')
        self.assertEqual(escala[-1]['populacao_z'], '0.109')
        rod = json.load(open(BASE / 'dados/processados/comparacao_rodadas.json', encoding='utf-8'))['rodadas']
        r3 = rod[2]
        z = r3['metricas']['populacao_z']
        self.assertAlmostEqual(z['bruto'], (454 + 441) / 1000)
        self.assertEqual(f"{z['ajustado']:.4f}", '0.9648')
        gz = [r['metricas']['populacao_z']['ganho'] for r in rod]
        gx = [r['metricas']['correlacao_x']['ganho'] for r in rod]
        self.assertEqual((f'{min(gz):.3f}', f'{max(gz):.3f}'), ('0.070', '0.072'))
        self.assertEqual((f'{min(gx):.3f}', f'{max(gx):.3f}'), ('0.148', '0.164'))
        for texto in ('0,922', '0,109', '0,9648', '0,070 a 0,072', '0,148 a 0,164', '0,9899', '0,8409', '0,9463'):
            self.assertIn(texto, artigo)

    def test_zne_referencia(self):
        ref = gerar_tabelas._manifesto()['referencias']['zne']['leitura_e_portas']
        pz = [gerar_tabelas._pz(ref[f'zne_{f}_Z']['antes_leitura']) for f in (1, 3, 5)]
        self.assertEqual(f'{gerar_tabelas._reta((1, 3, 5), pz):.4f}', '0.9899')

    def test_contagens_da_rodada_3(self):
        d = json.load(open(BASE / 'dados/brutos/04_mitigacao_leitura/rodada_03/rodada_03.json', encoding='utf-8'))
        z, x = d['contagens']['GHZ_Z'], d['contagens']['GHZ_X']
        self.assertEqual((z['00000'], z['11111'], sum(z.values())), (454, 441, 1000))
        pares = sum(v for k, v in x.items() if k.count('1') % 2 == 0)
        self.assertEqual((pares, sum(x.values()) - pares), (903, 97))


if __name__ == '__main__':
    unittest.main()
