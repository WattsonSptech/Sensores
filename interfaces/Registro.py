from datetime import datetime

from interfaces import EnumZonas
from interfaces.EnumCenarios import EnumCenarios


class Registro:
    nome_sensor: str
    unidade: str
    valor: float
    instante: str
    cenario: EnumCenarios
    zona: EnumZonas

    def __init__(self, nome_sensor: str, unidade: str, valor: float, instante: datetime, cenario: EnumCenarios, zona: EnumZonas) -> None:
        self.nome_sensor = nome_sensor
        self.unidade = unidade
        self.valor = valor
        self.instante = instante.isoformat()
        self.cenario = cenario
        self.zona = zona

    def __repr__(self) -> str:
        return f"{self.nome_sensor}: {self.valor} {self.unidade}"

    def to_json(self) -> dict:
        return {
            "valueType": self.unidade,
            "value": self.valor,
            "instant": self.instante,
            "scenery": self.cenario.name,
            "zone": self.zona.name
        }