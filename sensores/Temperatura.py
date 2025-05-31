from interfaces.ISimuladorSensor import ISimuladorSensor
from interfaces.EnumCenarios import EnumCenarios
from interfaces.Registro import Registro
import numpy as np
from interfaces.EnumZonas import EnumZonas

class Temperatura(ISimuladorSensor):
    
    __VALOR_BASE__ = 72.5 

    def __init__(self) -> None:
        super().__init__()
        self.nome_sensor = "IR MLX90614"
        self.unidade = "°C"

    def __formula_sensor__(self, cenario: EnumCenarios, zona: EnumZonas = None):
        variacao_moment = np.random.normal(0, 1.5)

        propabilidade_pico: float
        match cenario:
            case cenario.TERRIVEL:
                propabilidade_pico = 0.1
            case cenario.EXCEPCIONAL:
                propabilidade_pico = 0.000001
            case _:
                propabilidade_pico = 0.001

        pico = 0
        if np.random.rand() < propabilidade_pico:
            pico = max(0, np.random.pareto(2) * 10)
            if self.__VALOR_BASE__ + variacao_moment + pico > 100:
                pico = 100 - self.__VALOR_BASE__ - variacao_moment

        temperatura = self.__VALOR_BASE__ + variacao_moment + pico

        return temperatura
