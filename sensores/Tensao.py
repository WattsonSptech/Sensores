import numpy as np
from interfaces.EnumZonas import EnumZonas

from interfaces.EnumCenarios import EnumCenarios
from interfaces.EnumZonas import EnumZonas
from interfaces.ISimuladorSensor import ISimuladorSensor

class Tensao(ISimuladorSensor):
    
    __VALOR_BASE__ = 23000

    def __init__(self) -> None:
        super().__init__()
        self.nome_sensor = "LV25-P"
        self.unidade = "volts"

    def __formula_sensor__(self, cenario: EnumCenarios, zona: EnumZonas):
        variacao_moment = np.random.normal(0, 150)

        propabilidade_pico: float = 10
        # match cenario:
        #     case cenario.TERRIVEL:
        #         propabilidade_pico = 0.0002
        #     case cenario.EXCEPCIONAL:
        #         propabilidade_pico = 0.000005
        #     case _:
        #         propabilidade_pico = 0.00001

        propabilidade_pico = propabilidade_pico * zona.value

        horario = self.instante.hour
        if 17 <= horario <= 23:
            propabilidade_pico = propabilidade_pico * pow(10, 2)
        elif horario >= 0 or 11 <= horario <= 14:
            propabilidade_pico = propabilidade_pico * pow(10, 1.5)

        pico = 0
        if np.random.rand() < propabilidade_pico:
            pico = np.random.pareto(2) * 1000
        if np.random.pareto(2) < 1:
            pico = -pico

        tensao = self.__VALOR_BASE__ + variacao_moment + pico
        return tensao