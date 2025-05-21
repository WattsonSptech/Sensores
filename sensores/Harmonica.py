# Sensor Utilizado: AcuRev 2100 Multi-Circuit
# https://www.accuenergy.com/wp-content/uploads/AcuRev-2100-Multi-Circuit-Submeter-Datasheet.pdf
from random import uniform, randint
from interfaces.ISimuladorSensor import ISimuladorSensor
from interfaces.EnumCenarios import EnumCenarios


class Harmonica(ISimuladorSensor):

    def __init__(self):
        super().__init__()
        self.nome_sensor = "AcuRev 2100 Multi-Circuit"
        self.unidade = "Porcentagem"

    def __formula_sensor__(self, cenario):
        if (cenario == EnumCenarios.EXCEPCIONAL):
            minimum = 0.00
            maximum = 1.00
        elif (cenario == EnumCenarios.NORMAL):
            minimum = 1.00
            maximum = 5.00
        elif (cenario == EnumCenarios.TERRIVEL):
            minimum = 5.00
            maximum = 100.00

        accuracy = 1.0

        is_accuracy_positive_or_negative = randint(0, 1)

        harmonics = round((accuracy + (uniform(minimum, maximum)) if is_accuracy_positive_or_negative == 0 else (uniform(
            minimum, maximum)) - accuracy),2)

        if harmonics < 0:
            harmonics = 0.01
        if harmonics > 100:
            harmonics = 100.00

        return harmonics