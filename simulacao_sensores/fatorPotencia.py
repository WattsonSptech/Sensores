from ISimuladorSensor import ISimuladorSensor
from Registro import Registro
import random
import numpy as np

class FatorPotencia(ISimuladorSensor):
    
    __VALOR_BASE__ = 0.8  # Base para fator de potência

    def __init__(self) -> None:
        self.nome_sensor = "PZEM-004T"
        self.unidade = "Fator de Potência"

    def __formula_sensor__(self):
        fator_potencia = round(random.uniform(0.5, 1.0), 2)

        pico = 0
        if np.random.rand() < 0.001:  
            pico = np.random.pareto(2) * 2 
        if np.random.pareto(2) < 1:
            pico = -pico

        fator_potencia += pico  

        if fator_potencia < 0.0:
            fator_potencia = 0.0
        if fator_potencia > 1.5: 
            fator_potencia = 1.5

        return Registro(self.nome_sensor, self.unidade, round(fator_potencia, 2))

    def gerar_dados(self, quantidade):
        for _ in range(quantidade):
            registro = self.__formula_sensor__()
            print(registro)

FatorPotencia().gerar_dados(5)
