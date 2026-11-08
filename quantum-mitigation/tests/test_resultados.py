"""Testes das tabelas, do preenchimento de marcadores e do comando --analisar."""
import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import rodar
from mitigacao import resultados, sessao, tabelas
from mitigacao.execucao import simulador
from mitigacao.montagem import montar
from auxiliar import itens_basicos  # noqa: E402


def silencioso(funcao, *args, **kwargs):
    with contextlib.redirect_stdout(io.StringIO()):
        return funcao(*args, **kwargs)


class TabelasTest(unittest.TestCase):
    def test_formatacao(self):
        self.assertEqual(tabelas.fmt(0.12345), '0,1235')
        self.assertEqual(tabelas.pm(dict(valor=0.9, ep=0.0123), 3), '0,900 ± 0,012')
        t = tabelas.tabela(['a', 'b'], [(1, 2)], (1,))
        self.assertEqual(t.splitlines()[1], '| --- | ---: |')

    def test_preencher_troca_so_o_miolo_e_recusa_marcador_sem_tabela(self):
        texto = 'antes\n<!-- TABELA:x -->\nvelho\n<!-- /TABELA:x -->\ndepois'
        novo = tabelas.preencher(texto, {'x': '| t |'})
        self.assertEqual(novo, 'antes\n<!-- TABELA:x -->\n| t |\n<!-- /TABELA:x -->\ndepois')
        self.assertEqual(tabelas.preencher(novo, {'x': '| t |'}), novo)   # idempotente
        with self.assertRaises(KeyError):
            tabelas.preencher(texto, {'y': '| t |'})

    def test_sinal_dos_contrastes(self):
        def sessao_com(valor):
            c = dict(n=5, base='Z', fator=1, indicador='PZ', ajustado=None, bruto=dict(valor=valor, ep=0.01))
            return dict(contrastes=[c], itens={}, tipo='ibm')
        casos = [([0.1, 0.2, 0.3], 'positivo em todas'), ([-0.1, -0.2], 'negativo em todas'),
                 ([0.0, 0.0], 'zero em todas'), ([0.1, -0.1], 'sinais diferentes')]
        for valores, esperado in casos:
            res = {f's{i}': sessao_com(v) for i, v in enumerate(valores)}
            self.assertTrue(tabelas.t_contrastes(res).endswith(f'| {esperado} |'), esperado)


class AnalisarTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.pasta_exp = Path(self.tmp.name) / 'experimentos' / '99_teste'
        receita = SimpleNamespace(pergunta='teste', execucao='simulador', shots=1000)
        montados = montar(itens_basicos(), lambda n: simulador.vizinhos('simulador', n))
        for i, cenario in enumerate(('leitura', 'leitura_e_portas'), 1):
            silencioso(sessao.enviar_e_gravar, self.pasta_exp / 'dados' / f'{cenario}_bloco_01', self.pasta_exp,
                       receita, montados, 'simulador', 7 + i, dict(cenario=cenario))

    def test_gerar_resultados_tabelas_e_figuras(self):
        (self.pasta_exp / 'README.md').write_text(
            '# t\n<!-- TABELA:cenarios -->\nvelho\n<!-- /TABELA:cenarios -->\n', encoding='utf-8')
        saida = silencioso(resultados.gerar, self.pasta_exp, ['leitura'], 100)
        pasta = self.pasta_exp / 'resultados'
        self.assertEqual(sorted(saida['sessoes']), ['leitura_bloco_01', 'leitura_e_portas_bloco_01'])
        for arquivo in ('resultados.json', 'tabelas.md', 'comparacao_leitura.png', 'comparacao_leitura_e_portas.png'):
            self.assertTrue((pasta / arquivo).exists(), arquivo)
        dados = json.loads((pasta / 'resultados.json').read_text(encoding='utf-8'))
        self.assertTrue(all(r['validacao']['aprovado'] for r in dados.values()))
        self.assertIn('0,8409', (self.pasta_exp / 'README.md').read_text(encoding='utf-8'))
        self.assertIn('sessoes_leitura', saida['tabelas'])      # com 2 cenários, as tabelas ganham o sufixo

    def test_comando_analisar(self):
        receita = self.pasta_exp / 'experimento.py'
        receita.write_text("pergunta='t'\nexecucao='simulador'\ntecnicas=['leitura']\nitens=[]\n", encoding='utf-8')
        saida = io.StringIO()
        with mock.patch.object(rodar, 'RAIZ', Path(self.tmp.name)), \
                mock.patch.object(sys, 'argv', ['rodar.py', '99', '--analisar', '--repeticoes', '50']), \
                contextlib.redirect_stdout(saida):
            codigo = rodar.main()
        self.assertEqual(codigo, 0)
        self.assertIn('2 sessões analisadas', saida.getvalue())

    def test_sem_sessoes_coletadas(self):
        vazio = Path(self.tmp.name) / 'experimentos' / '98_vazio'
        vazio.mkdir()
        with self.assertRaises(ValueError):
            resultados.gerar(vazio, [], 10)


if __name__ == '__main__':
    unittest.main()
