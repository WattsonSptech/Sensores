import numpy as np

from interfaces.EnumCenarios import EnumCenarios
from interfaces.ISimuladorSensor import ISimuladorSensor
from interfaces.Registro import Registro


class Frequencia(ISimuladorSensor):
    __VALOR_BASE__ = 60

    def __init__(self) -> None:
        super().__init__()
        self.nome_sensor = "FrequencyGet"
        self.unidade = "Hz"

    def __formula_sensor__(self, cenario: EnumCenarios):
        variacao_moment = np.random.normal(0, 0.1)

        somador = 0
        pico = 0
        match cenario:
            case cenario.TERRIVEL:
                somador = 3
            case cenario.EXCEPCIONAL:
                somador = 0
            case _:
                somador = 0.1

                
        if np.random.rand() < 0.001:
            pico = np.random.pareto(2) * 12 + somador
        if np.random.pareto(2) < 1:
            pico = -pico
            pico -= somador

        frequencia = self.__VALOR_BASE__ + variacao_moment + pico
        return frequencia