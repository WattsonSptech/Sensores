import random
from datetime import datetime

from interfaces.EnumCenarios import EnumCenarios
from interfaces.ISimuladorSensor import ISimuladorSensor
from interfaces.EnumZonas import EnumZonas

class Corrente(ISimuladorSensor):

    __MAX_CURRENT__ = 800
    __ENROLL_PROPORTION__ = 160

    def __init__(self) -> None:
        super().__init__()
        self.nome_sensor = "RCI-32"
        self.unidade = "ampére"

    def __formula_sensor__(self, cenario: EnumCenarios, zona: EnumZonas, instante: datetime):

        percentual = 0
        match cenario:
            case cenario.NORMAL:
                primary_current = round(random.randint(400, self.__MAX_CURRENT__), 4)
                percentual = primary_current / self.__MAX_CURRENT__ * 100
            case cenario.TERRIVEL:
                primary_current = round(random.randint(self.__MAX_CURRENT__, 1200), 4)
                percentual = primary_current / self.__MAX_CURRENT__ * 100
            case cenario.EXCEPCIONAL:
                primary_current = round(random.randint(80, 400), 4)
                percentual = primary_current / self.__MAX_CURRENT__ * 100

        if percentual > 50 and percentual <= 100:
            secundary_current = 5
        elif percentual > 100 and percentual <= 150:
            secundary_current = round(primary_current / self.__ENROLL_PROPORTION__, 2)
        elif percentual >= 10 and percentual <= 50:
            secundary_current = round(primary_current / self.__ENROLL_PROPORTION__, 2)

        return secundary_current