from datetime import datetime

from interfaces.EnumCenarios import EnumCenarios


class Registro:
    sensor: str
    unidade: str
    valor: float
    instante: str
    cenario: EnumCenarios

    def __init__(self, sensor: str, unidade: str, valor: float, cenario: EnumCenarios) -> None:
        self.sensor = sensor
        self.unidade = unidade
        self.valor = valor
        self.instante = datetime.now().isoformat()
        self.cenario = cenario

    def __repr__(self) -> str:
        return f"{self.sensor}: {self.valor} {self.unidade}"

    def to_json(self) -> dict:
        return {
            "deviceID": "eda-watson",
            # "sensor": self.sensor,
            "valueType": self.unidade,
            "value": self.valor,
            "instant": self.instante,
            "scenery": self.cenario.name
        }