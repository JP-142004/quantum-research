"""Testes da análise da parte B do experimento 8 (calibração por qubit em muitos qubits), com sessões do simulador."""
import importlib.util
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from mitigacao import leitura_ibm as lb, leitura_ibm_saida as saida, registro, sessao  # noqa: E402
from mitigacao.analise import indicador_do_item, pesos, vetor  # noqa: E402
from mitigacao.tecnicas import leitura  # noqa: E402

PARTE_B = Path(__file__).resolve().parents[1] / 'experimentos' / '08_leitura_escala' / 'b_ibm'


def receita_b():
    spec = importlib.util.spec_from_file_location('receita_8b', PARTE_B / 'experimento.py')
    receita = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(receita)
    return receita


class Receita:
    """A receita da parte B, para o simulador, com os itens de um tamanho só."""
    execucao, pergunta, tecnicas, shots = 'simulador', 'teste', [], 1000

    def __init__(self, n):
        itens = [dict(circuito='ghz', n=n, variante='conectado', base=b) for b in ('Z', 'X')]
        itens += [dict(circuito='simples', n=n, variante=v, base='Z') for v in ('0' * n, '1' * n, ('01' * n)[:n], ('10' * n)[:n])]
        itens += [dict(circuito='simples', n=n, variante=v, base=b, rotulo='controle')
                  for v, b in (('0' * n, 'Z'), ('1' * n, 'Z'), ('+' * n, 'X'), ('+' * (n - 1) + '-', 'X'))]
        self.itens = itens


def simular(tmp, n, cenario, semente=77):
    pasta = Path(tmp) / 'dados' / f'{cenario}_{n}'
    receita = Receita(n)
    sessao.enviar_e_gravar(pasta, Path(tmp), receita, sessao.montar_receita(receita, 'simulador'), 'simulador', semente,
                           dict(cenario=cenario))
    return registro.ler_sessao(pasta)


class LeituraIbmTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.sessoes = {(n, c): simular(cls.tmp.name, n, c) for n in (5, 10) for c in ('leitura', 'leitura_correlacionada')}

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_a_receita_da_parte_b_tem_os_mesmos_itens_que_o_teste(self):
        r = receita_b()
        self.assertEqual([i for i in r.itens if i['n'] == 10], Receita(10).itens)
        self.assertEqual(len(r.itens), 20)

    def test_a_conta_esparsa_e_igual_a_denso(self):
        """PZ e CX corrigidos pelas tabelas de zeros e uns: soma sobre as sequências observadas contra a matriz inteira."""
        ficha, cont = self.sessoes[(5, 'leitura')]
        n = 5
        cal = {i['item']['variante']: i for i in ficha['itens'] if i['item']['n'] == n and i['item']['rotulo'] is None
               and i['item']['circuito'] == 'simples'}
        grupo = [(lb._preparado(v), *lb._lista(cont[cal[v]['nome']], n)) for v in ('0' * n, '1' * n)]
        inv = lb._inversas(lb.tabelas(grupo, n))
        nomes = {nome: cont[nome] for nome in cont}
        a = leitura.matriz(nomes, n, None, 'fatorizado_dois')
        for i in ficha['itens']:
            if i['item']['circuito'] != 'ghz':
                continue
            nome_ind, peso, _ = indicador_do_item(i['item'])
            bits, vezes = lb._lista(cont[i['nome']], n)
            denso = float(pesos(peso, n) @ np.linalg.solve(a, vetor(cont[i['nome']], n, 1000)))
            self.assertAlmostEqual(lb.indicador(nome_ind, bits, vezes, inv), denso, places=9, msg=nome_ind)

    def test_sem_correlacao_nao_rejeita_e_o_ghz_chega_perto_de_1(self):
        res = lb.analisar_tamanho(*self.sessoes[(10, 'leitura')], 10, repeticoes=60)
        self.assertEqual(saida.veredito_independencia(res['independencia']), 'não rejeitada')
        for x in saida._ghz(res):
            self.assertLess(abs(x['ajustado']['valor'] - 1), 0.1)
            self.assertGreater(x['ganho']['valor'], 0.2)
        self.assertTrue(saida.ganho_ok(res))

    def test_com_correlacao_rejeita_e_o_ajuste_passa_do_ideal(self):
        res = lb.analisar_tamanho(*self.sessoes[(10, 'leitura_correlacionada')], 10, repeticoes=60)
        self.assertEqual(saida.veredito_independencia(res['independencia']), 'rejeitada')
        self.assertTrue(all(x['ajustado']['valor'] > 1.1 for x in saida._ghz(res)))
        # a comparação entre contextos não vê o erro conjunto (ele muda os dois grupos do mesmo jeito)
        self.assertNotEqual(saida.veredito_contexto(res['contexto']['decisoes']), 'diferente')

    def test_qubits_diferentes_entre_calibracao_e_circuito_param_a_analise(self):
        ficha, cont = self.sessoes[(5, 'leitura')]
        ficha = {**ficha, 'itens': [dict(i) for i in ficha['itens']]}
        ficha['itens'][0]['qubits_fisicos'] = list(reversed(ficha['itens'][0]['qubits_fisicos']))
        with self.assertRaises(ValueError):
            lb.analisar_tamanho(ficha, cont, 5, repeticoes=2)

    def test_gerar_grava_os_resultados(self):
        pasta = Path(self.tmp.name) / 'b_teste'
        (pasta / 'dados').mkdir(parents=True)
        shutil.copytree(Path(self.tmp.name) / 'dados' / 'leitura_10', pasta / 'dados' / '2026-11-30_ibm_fez')
        shutil.copy(PARTE_B / 'README.md', pasta / 'README.md')
        antes = (pasta / 'README.md').read_text(encoding='utf-8')
        info = saida.gerar(pasta, repeticoes=20)
        self.assertEqual(info['sessoes'], ['2026-11-30_ibm_fez'])
        for nome in ('resultados_ibm.json', 'tabelas_ibm.md', 'ghz_10_e_20_qubits.png'):
            self.assertTrue((pasta / 'resultados' / nome).exists(), nome)
        depois = (pasta / 'README.md').read_text(encoding='utf-8')
        self.assertNotEqual(antes, depois)
        self.assertIn('só 1 de 3 sessões', depois)   # a tabela de critérios avisa que faltam sessões


if __name__ == '__main__':
    unittest.main()
