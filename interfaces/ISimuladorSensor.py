from abc import abstractmethod
from datetime import datetime, timedelta
from interfaces.EnumCenarios import EnumCenarios
from interfaces.Registro import Registro
from tqdm import tqdm

class ISimuladorSensor:
    nome_sensor: str
    unidade: str
    instante: datetime

    def __init__(self):
        self.instante = datetime.now()

    def gerar_dados(self, vezes: int, cenario: EnumCenarios) -> list[dict]:
        registros = []

        for i in tqdm(range(vezes)):
            valor = self.__formula_sensor__(cenario)
            self.instante = self.instante + timedelta(minutes=15 * i - 15)

            r = Registro(self.nome_sensor, self.unidade, valor, self.instante, cenario)
            registros.append(r.to_json())

        return registros

    @abstractmethod
    def __formula_sensor__(self, cenario: EnumCenarios) -> float|int:
        pass