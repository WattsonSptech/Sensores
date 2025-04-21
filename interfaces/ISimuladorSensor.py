from abc import abstractmethod
from interfaces.Registro import Registro


class ISimuladorSensor:
    nome_sensor: str
    unidade: str

    def gerar_dados(self, vezes: int) -> list[Registro]:
        registros = []
        for i in range(vezes):
            valor = self.__formula_sensor__()
            r = Registro(self.nome_sensor, self.unidade, valor)

            registros.append(r)

        return registros

    @abstractmethod
    def __formula_sensor__(self) -> float|int:
        pass