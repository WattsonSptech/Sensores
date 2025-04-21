import random
import numpy as np
from interfaces.ISimuladorSensor import ISimuladorSensor
from sensores.Corrente import Corrente
from sensores.Tensao import Tensao

class Potencia(ISimuladorSensor):

    __TENSAO__ = Tensao()
    __CORRENTE__ = Corrente()

    __FP_MEDIA__ = 0.97
    __DESVIO_PADRAO__ = 0.03
    __PROB_CRITICA__ = 0.03
    __PROB_ALERTA__ = 0.08

    def __init__(self):
        self.nome_sensor = "SDM630"
        self.unidade = "watts"
    
    def __formula_sensor__(self) -> float|int:
        # tensao = round(random.uniform(80, 260), 1)
        # corrente = round(random.uniform(0, 100), 2)
        tensao = self.__TENSAO__.__formula_sensor__()
        corrente = self.__CORRENTE__.__formula_sensor__()

        potencia_aparente = round(tensao * corrente, 1)
    
        # Variáveis para simulação do fator de potencia
        porcent = random.random()
    
        # Logica para casos
        if porcent < self.__PROB_CRITICA__:
            fator_potencia = round(random.uniform(0.60, 0.80), 3)
        elif porcent < self.__PROB_CRITICA__ + self.__PROB_ALERTA__:
            fator_potencia = round(random.uniform(0.80, 0.92), 3)
        else:
            fator_potencia = np.random.normal(
                loc=self.__FP_MEDIA__, scale=self.__DESVIO_PADRAO__
            )
            fator_potencia = np.clip(fator_potencia, 0, 1)
    
        fator_potencia = float(round(fator_potencia, 2))
    
        return fator_potencia