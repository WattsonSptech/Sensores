from abc import abstractmethod

from interfaces.EnumCenarios import EnumCenarios
from interfaces.Registro import Registro
import psutil as ps
import numpy as np

class ISimuladorSensor:
    nome_sensor: str
    unidade: str

    def gerar_dados(self, vezes: int, cenario: EnumCenarios) -> list[Registro]:

        usages = {
                'cpu': [],
                'memory': []
        }

        registros = []
        for i in range(vezes):
            valor = self.__formula_sensor__(cenario)
            r = Registro(self.nome_sensor, self.unidade, valor)
            registros.append(r.to_json())
            usages['cpu'].append(ps.cpu_percent())
            usages['memory'].append(ps.virtual_memory().percent)


        xpoints = np.array(list(range(0, len(data))))
        ypoints = np.array(data)

        plt.plot(xpoints, ypoints)
        plt.show()

        return registros

    @abstractmethod
    def __formula_sensor__(self, cenario: EnumCenarios) -> float|int:
        pass