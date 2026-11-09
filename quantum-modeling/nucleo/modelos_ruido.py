"""Modelos de ruido.

Nivel 0: modelo padrao da IBM (NoiseModel.from_backend), mas montado a partir
do snapshot de calibracao do dia do job, e nao da calibracao de hoje.
"""

from types import SimpleNamespace

from qiskit_aer.noise import NoiseModel
from qiskit_ibm_runtime.utils.backend_converter import convert_to_target


def nivel0(propriedades, configuracao):
    """Reconstroi o Target do backend com a calibracao salva e usa o mesmo
    caminho do NoiseModel.from_backend original (erros de porta, leitura e
    relaxacao termica). Qubits com defeito sao descartados pelo conversor."""
    target = convert_to_target(configuracao, propriedades)
    backend = SimpleNamespace(version=2, target=target,
                              operation_names=list(target.operation_names), dt=target.dt)
    return NoiseModel.from_backend(backend)
