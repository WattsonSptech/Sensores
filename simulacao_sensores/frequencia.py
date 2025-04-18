from ISimuladorSensor import ISimuladorSensor
from Registro import Registro
import numpy as np

class Frequencia(ISimuladorSensor):
    
    __VALOR_BASE__ = 60

    def __init__(self) -> None:
        self.nome_sensor = "FrequencyGet"
        self.unidade = "Hz"

    def __formula_sensor__(self):
        variacao_moment = np.random.normal(0, 0.1)

        pico = 0
        if np.random.rand() < 0.001:
            pico = np.random.pareto(2) * 12
        if np.random.pareto(2) < 1:
            pico = -pico

        frequencia = self.__VALOR_BASE__ + variacao_moment + pico

        return Registro(self.nome_sensor, self.unidade, frequencia)

Frequencia().gerar_dados(5)