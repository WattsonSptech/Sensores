from abc import abstractmethod
from datetime import datetime, timedelta
from math import ceil
from interfaces.EnumCenarios import EnumCenarios
from interfaces.EnumZonas import EnumZonas
from interfaces.Registro import Registro
from random import randint

class ISimuladorSensor:
    nome_sensor: str
    unidade: str

    def gerar_dados(self, vezes: int, cenario: EnumCenarios) -> list[dict]:
        registros = []

        zonas = [z for z in EnumZonas]
        instante = datetime.now()

        for _ in range(vezes):
            for z in zonas:
                valor = self.__formula_sensor__(cenario, z, instante)
                registros.append(Registro(
                    self.nome_sensor, self.unidade, valor, instante, cenario,
                    z
                ).to_json())

                instante = instante - timedelta(hours=randint(1, 48))

        return registros

    @abstractmethod
    def __formula_sensor__(self, cenario: EnumCenarios, zona: EnumZonas, instante: datetime) -> float|int:
        pass