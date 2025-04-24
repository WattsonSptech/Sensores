# Sensor Utilizado: AcuRev 2100 Multi-Circuit
# https://www.accuenergy.com/wp-content/uploads/AcuRev-2100-Multi-Circuit-Submeter-Datasheet.pdf
from random import uniform, randint
from interfaces.ISimuladorSensor import ISimuladorSensor
from interfaces.Registro import Registro


class Harmonica(ISimuladorSensor):

    __NOISE__ = 4

    def __init__(self):
        self.nome_sensor = "AcuRev 2100 Multi-Circuit"
        self.unidade = "Hertz"

    def __formula_sensor__(self):
        # Noise/ruído: indica a faixa de valores que poderão ser retornados. Em situações normais, o valor da harmônica deve estar entre 0% e 5%, onde, quando maior for essa porcentagem,
        # pior é a qualidade da energia.

        # Valores disponíveis para noise:
        # 1 - Low
        # 2 - Medium
        # 3 - High
        # 3 - Very High

        if (self.__NOISE__ == 1):
            minimum = 0.00
            maximum = 5.00
        elif (self.__NOISE__ == 2):
            minimum = 0.00
            maximum = 25.00
        elif (self.__NOISE__ == 3):
            minimum = 0.00
            maximum = 75.00
        elif (self.__NOISE__ == 4):
            minimum = 0.00
            maximum = 100.00
        else:
            print(f"No such value ({self.__NOISE__}) for noise is allowed. Using default values.")
            minimum = 0.00
            maximum = 5.00

        accuracy = 1.0

        # se o valor do random for 0, irá somar 1 no valor final da harmônica. Se for 1, irá diminuir 1 no valor final da harmônica.
        is_accuracy_positive_or_negative = randint(0, 1)

        harmonics = accuracy + (uniform(minimum, maximum)) if is_accuracy_positive_or_negative == 0 else (uniform(
            minimum, maximum)) - accuracy

        if harmonics < 0:
            harmonics = 0.01
        if harmonics > 100:
            harmonics = 100.00

        return harmonics