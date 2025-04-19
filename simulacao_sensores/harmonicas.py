from ISimuladorSensor import ISimuladorSensor
from Registro import Registro
import numpy as np
from random import randint, uniform

class Harmonica(ISimuladorSensor):
    
    __VALOR_BASE__ = 0.0 

    def __init__(self) -> None:
        self.nome_sensor = "AcuRev 2100 Multi-Circuit"
        self.unidade = "Harmônicas (%)"

    def __formula_sensor__(self, noise=1):
        if noise == 1:
            minimum = 0.00
            maximum = 5.00
        elif noise == 2:
            minimum = 0.00
            maximum = 25.00
        elif noise == 3:
            minimum = 0.00
            maximum = 75.00
        elif noise == 4:
            minimum = 0.00
            maximum = 100.00
        else:
            print(f"No such value ({noise}) for noise is allowed. Using default values.")
            minimum = 0.00
            maximum = 5.00

        accuracy = 1.0
        is_accuracy_positive_or_negative = randint(0, 1)

        harmonics = accuracy + uniform(minimum, maximum) if is_accuracy_positive_or_negative == 0 else uniform(minimum, maximum) - accuracy

        if harmonics < 0:
            harmonics = 0.01
        if harmonics > 100:
            harmonics = 100.00

        return Registro(self.nome_sensor, self.unidade, round(harmonics, 2))

    def gerar_dados(self, quantidade, noise=1):
        for _ in range(quantidade):
            registro = self.__formula_sensor__(noise)
            print(registro)

Harmonica().gerar_dados(5, noise=3) 
