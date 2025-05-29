# Sensor Utilizado: AcuRev 2100 Multi-Circuit
# https://www.accuenergy.com/wp-content/uploads/AcuRev-2100-Multi-Circuit-Submeter-Datasheet.pdf
from random import uniform, randint
from interfaces.ISimuladorSensor import ISimuladorSensor
from interfaces.EnumCenarios import EnumCenarios
from math import sqrt


class Harmonica(ISimuladorSensor):

    def __init__(self):
        super().__init__()
        self.nome_sensor = "AcuRev 2100 Multi-Circuit"
        self.unidade = "Porcentagem"

    def __formula_sensor__(self, cenario):

        FUNDAMENTAL_TENSION = 13.80

        if (cenario == EnumCenarios.EXCEPCIONAL):
            orders = 1
            min_tension = 13.79
            max_tension = FUNDAMENTAL_TENSION
        elif (cenario == EnumCenarios.NORMAL):
            orders = randint(3, 4)
            min_tension = 12.00
            max_tension = 13.78
        elif (cenario == EnumCenarios.TERRIVEL):
            orders = randint(5, 20)
            min_tension = 6.00
            max_tension = 11.09

        total_tension = 0
        for i in range (orders):
            total_tension += pow((uniform(min_tension, max_tension)) * -i, 2)

        return round(sqrt(total_tension)/FUNDAMENTAL_TENSION, 2)