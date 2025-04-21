from interfaces.ISimuladorSensor import ISimuladorSensor
from interfaces.Registro import Registro
import numpy as np

class Temperatura(ISimuladorSensor):
    
    __VALOR_BASE__ = 70

    def __init__(self) -> None:
        self.nome_sensor = "IR MLX90614"
        self.unidade = "°C"

    def __formula_sensor__(self):
        variacao_moment = np.random.normal(0, 0.1)

        pico = 0
        if np.random.rand() < 0.001:
            pico = 100 - self.__VALOR_BASE__ - variacao_moment  

        temperatura = self.__VALOR_BASE__ + variacao_moment + pico

        return Registro(self.nome_sensor, self.unidade, temperatura)

    def gerar_dados(self, quantidade):
        for _ in range(quantidade):
            registro = self.__formula_sensor__()
            print(registro)

Temperatura().gerar_dados(10)
