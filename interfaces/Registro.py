from datetime import datetime
from interfaces import EnumZonas


class Registro:
    nome_sensor: str
    unidade: str
    valor: float
    instante: str
    zona: EnumZonas

    def __init__(self, nome_sensor: str, unidade: str, valor: float, instante: datetime, zona: EnumZonas) -> None:
        self.nome_sensor = nome_sensor
        self.unidade = unidade
        self.valor = valor
        self.instante = instante.isoformat()
        self.zona = zona

    def __repr__(self) -> str:
        return f"{self.nome_sensor}: {self.valor} {self.unidade}"

    def to_json(self) -> dict:
        return {
            "valueType": self.unidade,
            "value": self.valor,
            "instant": self.instante,
            "zone": self.zona.name
        }