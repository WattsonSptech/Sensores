import datetime
import numpy as np
from numpy.random import randint
from interfaces.EnumCenarios import EnumCenarios
from interfaces.EnumZonas import EnumZonas
from interfaces.ISimuladorSensor import ISimuladorSensor

class Tensao(ISimuladorSensor):
    
    __VALOR_BASE__ = 23000

    def __init__(self) -> None:
        super().__init__()
        self.nome_sensor = "LV25-P"
        self.unidade = "volts"

    def __formula_sensor__(self, cenario: EnumCenarios, zona: EnumZonas, instante: datetime.datetime):
        variacao_moment = np.random.normal(0, 150)

        pico = 0
        if randint(0, 750) < (zona.value * 100):
            pico = randint(4000, 5000)

            pico = -pico if randint(0,2) == 1 else pico

        tensao = self.__VALOR_BASE__ + variacao_moment + pico
        return tensao