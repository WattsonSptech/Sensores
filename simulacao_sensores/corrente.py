from ISimuladorSensor import ISimuladorSensor
from Registro import Registro
import time
import numpy as np

class Corrente(ISimuladorSensor):
    
    __VALOR_BASE__ = 60

    def __init__(self) -> None:
        self.nome_sensor = "CorrenteGet"
        self.unidade = "A"

    def __formula_sensor__(self):
        primary_voltage = np.random.normal(1000, 36000)
        primary_enroll = 1
        secundary_enroll = 160
        power = 25

        primary_current = power / primary_voltage
        secundary_current = primary_current * (secundary_enroll / primary_enroll)

        if secundary_current < 5:
            secundary_current = 5

        format_time = time.strftime('%H:%M:%S')

        return Registro(self.nome_sensor, self.unidade, {"primary_current": primary_current,
                                                         "secundary_current": secundary_current})

Corrente().gerar_dados(5)