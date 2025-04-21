import numpy as np
from interfaces.ISimuladorSensor import ISimuladorSensor
from interfaces.Registro import Registro


class Tensao(ISimuladorSensor):
    
    __VALOR_BASE__ = 23000

    def __init__(self) -> None:
        self.nome_sensor = "LV25-P"
        self.unidade = "volts"

    def __formula_sensor__(self):
        variacao_moment = np.random.normal(0, 150)

        pico = 0
        if np.random.rand() < 0.001:
            pico = np.random.pareto(2) * 1000
        if np.random.pareto(2) < 1:
            pico = -pico

        tensao = self.__VALOR_BASE__ + variacao_moment + pico
        return tensao