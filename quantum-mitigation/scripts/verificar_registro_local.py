"""Audita hashes, QPY, totais e coerência estatística de uma execução local."""
import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
from qiskit import qpy
from protocolo_local import circuitos, validar_circuitos, pesos, vetor


def verificar(pasta):
    manifesto = json.loads((pasta / 'manifesto.json').read_text(encoding='utf-8'))
    if manifesto['estado'] != 'concluida' or manifesto['origem'] != 'simulacao_local_CPU':
        raise ValueError('Registro incompleto ou origem inesperada')
    for nome, esperado in manifesto['arquivos'].items():
        obtido = hashlib.sha256((pasta / nome).read_bytes()).hexdigest()
        if obtido != esperado:
            raise ValueError(f'Arquivo alterado: {nome}')
    for protocolo in ('comparacao', 'zne'):
        nomes = list(manifesto['circuitos'][protocolo])
        with (pasta / f'{protocolo}.qpy').open('rb') as arquivo:
            compilados = qpy.load(arquivo)
        if len(nomes) != len(compilados):
            raise ValueError('QPY incompleto')
        validar_circuitos(circuitos(protocolo == 'zne'), dict(zip(nomes, compilados)))
    shots_total, blocos, max_z_bruto, max_z_ajustado = 0, 0, 0., 0.
    for caminho in sorted(pasta.glob('*_contagens.json')):
        registro = json.loads(caminho.read_text(encoding='utf-8'))
        analise = json.loads(caminho.with_name(caminho.name.replace('_contagens', '_analise')).read_text(encoding='utf-8'))
        refs = manifesto['referencias'][registro['protocolo']][registro['cenario']]
        if set(refs) != set(registro['contagens']):
            raise ValueError('Circuitos divergentes')
        for nome, counts in registro['contagens'].items():
            observado = vetor(counts, registro['shots'])
            shots_total += sum(counts.values())
            if nome.startswith('cal_'):
                continue
            w = pesos(nome)
            alvo_obs = np.array(refs[nome]['observado'])
            media = w @ alvo_obs
            ep = np.sqrt(max(0, (w*w) @ alvo_obs - media**2) / registro['shots'])
            desvio = abs(w @ observado - media)
            if ep < 1e-9:
                if desvio > 1e-8:
                    raise ValueError('Métrica determinística divergente')
            else:
                max_z_bruto = max(max_z_bruto, float(desvio/ep))
            m = analise['circuitos'][nome]['ajustado']
            alvo_pre = float(w @ np.array(refs[nome]['antes_leitura']))
            if m['erro_padrao'] > 1e-9:
                max_z_ajustado = max(max_z_ajustado, abs(m['valor']-alvo_pre)/m['erro_padrao'])
            elif abs(m['valor']-alvo_pre) > 1e-8:
                raise ValueError('Ajuste determinístico divergente')
        blocos += 1
    if shots_total != manifesto['shots_simulados'] or blocos != 12:
        raise ValueError('Registro incompleto')
    # Sanidade numérica ampla, não teste confirmatório de cobertura de IC.
    if max_z_bruto > 6 or max_z_ajustado > 6:
        raise ValueError('Desvio acima do limite de sanidade de seis erros padrão')
    saida = dict(resultado='aprovado', arquivos_hash_verificados=len(manifesto['arquivos']),
        qpy_verificados=2, blocos=blocos, shots_simulados=shots_total,
        maior_desvio_bruto_em_ep=max_z_bruto, maior_desvio_ajustado_em_ep=max_z_ajustado,
        criterio='Sanidade ampla: até 6 EP do modelo exato; não é teste de cobertura ou evidência de validade do hardware.')
    (pasta / 'verificacao.json').write_text(json.dumps(saida, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    return saida


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('pasta', type=Path)
    args = parser.parse_args()
    print(json.dumps(verificar(args.pasta), ensure_ascii=False, indent=2))
