from random import random
from interfaces.ISimuladorSensor import ISimuladorSensor

class Corrente(ISimuladorSensor):

    __MAX_CURRENT__ = 800
    __ENROLL_PROPORTION__ = 160

    def __init__(self) -> None:
        self.nome_sensor = "RCI-32"
        self.unidade = "ampére"

    def __formula_sensor__(self):
        primary_current = round(random.randint(16, self.__MAX_CURRENT__), 4)

        percentual = primary_current / self.__MAX_CURRENT__ * 100
        if percentual > 5 and percentual <= 120:
            secundary_current = 5
        elif percentual >= 2.5 and percentual < 5:
            secundary_current = round(primary_current / self.__ENROLL_PROPORTION__, 2)
        else:
            secundary_current = round(primary_current / self.__ENROLL_PROPORTION__, 2)

        return secundary_current