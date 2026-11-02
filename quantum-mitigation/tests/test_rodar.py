"""Testes do comando rodar.py, em uma pasta temporária. Nenhum teste acessa a IBM:
o envio à IBM é substituído por um falso que usa o simulador."""
import contextlib
import io
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import rodar
from mitigacao.execucao import ibm, simulador
from mitigacao.topologia import vizinhos_linha

RECEITA = '''
pergunta = "Teste"
execucao = "{execucao}"
computador = "{computador}"
shots = 100
repeticoes = 2
itens = [dict(circuito="ghz", n=3, variante=v) for v in ("original", "conectado")]
opcoes_envio = {opcoes}
'''


class RodarTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.raiz = Path(self.tmp.name)
        patcher = mock.patch.object(rodar, 'RAIZ', self.raiz)
        patcher.start()
        self.addCleanup(patcher.stop)
        self.addCleanup(self.tmp.cleanup)

    def receita(self, numero, execucao, computador, opcoes='{}'):
        pasta = self.raiz / 'experimentos' / f'{numero:02d}_teste'
        pasta.mkdir(parents=True)
        (pasta / 'experimento.py').write_text(
            RECEITA.format(execucao=execucao, computador=computador, opcoes=opcoes), encoding='utf-8')
        return pasta

    def rodar(self, *argumentos):
        saida = io.StringIO()
        with mock.patch.object(sys, 'argv', ['rodar.py', *argumentos]), contextlib.redirect_stdout(saida):
            try:
                codigo = rodar.main()
            except SystemExit as e:
                codigo = e.code
        return codigo, saida.getvalue()

    def test_verificar_nao_grava_nada(self):
        pasta = self.receita(1, 'ibm', 'ibm_teste')
        codigo, saida = self.rodar('01', '--verificar')
        self.assertEqual(codigo, 0)
        self.assertIn('2 circuitos x 100 shots = 200 medidas por sessão', saida)
        self.assertIn('400 medidas no total', saida)
        self.assertFalse((pasta / 'dados').exists())

    def test_simulador_envia_e_grava_a_sessao(self):
        pasta = self.receita(2, 'simulador', 'simulador', opcoes="dict(cenario='ideal')")
        codigo, _ = self.rodar('02', '--enviar', '--sessao', 'sessao1')
        self.assertEqual(codigo, 0)
        self.assertTrue((pasta / 'dados' / 'sessao1' / 'contagens.json').exists())
        _, saida = self.rodar('02', '--listar')
        self.assertIn('sessao1 (coletada)', saida)

    def test_nao_regrava_a_mesma_sessao(self):
        self.receita(3, 'simulador', 'simulador', opcoes="dict(cenario='ideal')")
        self.rodar('03', '--enviar', '--sessao', 's')
        codigo, _ = self.rodar('03', '--enviar', '--sessao', 's')
        self.assertIn('já existe', str(codigo))

    def test_ibm_sem_confirmacao_nao_envia(self):
        pasta = self.receita(4, 'ibm', 'ibm_teste')
        with mock.patch.object(ibm, 'vizinhos', return_value=vizinhos_linha(10)), \
                mock.patch.object(ibm, 'enviar', side_effect=AssertionError('não deveria enviar')) as enviar, \
                mock.patch('builtins.input', return_value='nao'):
            codigo, _ = self.rodar('04', '--enviar')
        self.assertIn('Nada foi enviado', str(codigo))
        enviar.assert_not_called()
        self.assertFalse((pasta / 'dados').exists())

    def test_ibm_com_confirmacao_e_coleta_em_dois_tempos(self):
        pasta = self.receita(5, 'ibm', 'ibm_teste')
        pronto = {}

        def enviar_falso(montados, shots, semente, computador, **extras):
            job = simulador.enviar(montados, shots, semente, computador, cenario='ideal')
            pronto.update(job['contagens'])
            return dict(job, job_id='job-falso', contagens=None, opcoes=dict(dd=False))

        # linha de 3 qubits: o simulador que imita a IBM aqui só conhece os qubits 0 a n-1
        with mock.patch.object(ibm, 'vizinhos', return_value=vizinhos_linha(3)), \
                mock.patch.object(ibm, 'enviar', side_effect=enviar_falso), \
                mock.patch.object(ibm, 'coletar', return_value=None) as coletar, \
                mock.patch('builtins.input', return_value='ENVIAR'):
            self.rodar('05', '--enviar', '--sessao', 's')
            sessao = pasta / 'dados' / 's'
            self.assertTrue((sessao / 'ficha.json').exists())
            self.assertFalse((sessao / 'contagens.json').exists())
            _, saida = self.rodar('05', '--coletar', '--sessao', 's')
            self.assertIn('ainda não terminou', saida)
            coletar.return_value = pronto
            self.rodar('05', '--coletar', '--sessao', 's')
            self.assertTrue((sessao / 'contagens.json').exists())
            codigo, _ = self.rodar('05', '--coletar', '--sessao', 's')
            self.assertIn('já foi coletada', str(codigo))

    def test_experimento_inexistente(self):
        (self.raiz / 'experimentos').mkdir()
        codigo, _ = self.rodar('09', '--verificar')
        self.assertIn('encontrei 0 pastas', str(codigo))


if __name__ == '__main__':
    unittest.main()
