from abc import ABC, abstractmethod
from Registro import Registro

class ISimuladorSensor:
    nome_sensor: str
    unidade: str

    def gerar_dados(self, vezes: int) -> list[Registro]:
        registros = []
        for i in range(vezes):
            r = self.__formula_sensor__()

            registros.append(r)
            print(r)
        
        return registros

    @abstractmethod
    def __formula_sensor__(self) -> Registro:
        pass