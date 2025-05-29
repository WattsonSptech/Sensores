from abc import abstractmethod
from datetime import datetime, timedelta
from math import ceil

from interfaces.EnumCenarios import EnumCenarios
from interfaces.EnumZonas import EnumZonas
from interfaces.Registro import Registro
from tqdm import tqdm

class ISimuladorSensor:
    nome_sensor: str
    unidade: str
    instante: datetime

    def __init__(self):
        self.instante = datetime.fromisoformat("1980-01-01")

    def gerar_dados(self, vezes: int, cenario: EnumCenarios) -> list[dict]:
        registros = []

        zonas = [z.name for z in EnumZonas]
        vezes_por_zona = ceil(vezes / len(zonas))
        zona_por_registro = []
        for z in zonas:
            [zona_por_registro.append(z) for _ in range(vezes_por_zona)]

        for i in tqdm(range(vezes)):
            valor = self.__formula_sensor__(cenario)
            self.instante = self.instante + timedelta(minutes=15 * i - 15)

            r = Registro(
                self.nome_sensor, self.unidade, valor, self.instante, cenario,
                zonas[i]
            )
            registros.append(r.to_json())

        return registros

    @abstractmethod
    def __formula_sensor__(self, cenario: EnumCenarios) -> float|int:
        pass