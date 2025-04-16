from ISimuladorSensor import ISimuladorSensor
from Registro import Registro
import numpy as np

class Tensao(ISimuladorSensor):
    
    __VALOR_BASE__ = 23000

    def __init__(self) -> None:
        self.nome_sensor = "XPTO"
        self.unidade = "volts"

    def __formula_sensor__(self):
        variacao_moment = np.random.normal(0, 150)

        pico = 0
        if np.random.rand() < 0.001:
            pico = np.random.pareto(2) * 1000
        if np.random.pareto(2) < 1:
            pico = -pico

        tensao = self.__VALOR_BASE__ + variacao_moment + pico

        return Registro(self.nome_sensor, self.unidade, tensao)

Tensao().gerar_dados(5)