import random
import numpy as np
from interfaces.ISimuladorSensor import ISimuladorSensor
from sensores.Corrente import Corrente
from sensores.Tensao import Tensao
from interfaces.EnumCenarios import EnumCenarios
from interfaces.EnumZonas import EnumZonas

class Potencia(ISimuladorSensor):

    __TENSAO__ = Tensao()
    __CORRENTE__ = Corrente()

    __FP_MEDIA__ = 0.97
    __DESVIO_PADRAO__ = 0.03
    __PROB_CRITICA__ = 0.03
    __PROB_ALERTA__ = 0.08

    def __init__(self):
        super().__init__()
        self.nome_sensor = "SDM630"
        self.unidade = "watts"
    
    def __formula_sensor__(self, cenario: EnumCenarios, zona: EnumZonas) -> float|int:
        # tensao = round(random.uniform(80, 260), 1)
        # corrente = round(random.uniform(0, 100), 2)
        tensao = self.__TENSAO__.__formula_sensor__(cenario, zona)
        corrente = self.__CORRENTE__.__formula_sensor__(cenario, zona)

        potencia_aparente = round(tensao * corrente, 1)
    
        prob_critica = 0.03
        prob_alerta = 0.08
        match cenario:
            case cenario.TERRIVEL:
                prob_critica = 0.70
                prob_alerta = 0.95
            case cenario.EXCEPCIONAL:
                prob_critica = 0.005
                prob_alerta = 0.01

        # Variáveis para simulação do fator de potencia
        porcent = random.random()

        # Logica para casos
        if porcent < prob_critica:
            fator_potencia = round(random.uniform(0.60, 0.80), 3)
        elif porcent < prob_alerta:
            fator_potencia = round(random.uniform(0.80, 0.92), 3)
        else:
            fator_potencia = np.random.normal(
                loc=self.__FP_MEDIA__, scale=self.__DESVIO_PADRAO__
            )
            fator_potencia = np.clip(fator_potencia, 0, 1)
    
        fator_potencia = float(round(fator_potencia, 2))
    
        return fator_potencia