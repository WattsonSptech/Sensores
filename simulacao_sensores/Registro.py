class Registro:
    sensor: str
    unidade: str
    valor: float

    def __init__(self, sensor: str, unidade: str, valor: float) -> None:
        self.sensor = sensor
        self.unidade = unidade
        self.valor = valor

    def __repr__(self) -> str:
        return f"{self.sensor}: {self.valor} {self.unidade}"