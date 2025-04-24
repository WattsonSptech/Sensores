from abc import abstractmethod

from interfaces.EnumCenarios import EnumCenarios
from interfaces.Registro import Registro


class ISimuladorSensor:
    nome_sensor: str
    unidade: str

    def gerar_dados(self, vezes: int, cenario: EnumCenarios) -> list[Registro]:
        registros = []
        for i in range(vezes):
            valor = self.__formula_sensor__(cenario)
            r = Registro(self.nome_sensor, self.unidade, valor)
            registros.append(r.to_json())

        return registros

    @abstractmethod
    def __formula_sensor__(self, cenario: EnumCenarios) -> float|int:
        pass