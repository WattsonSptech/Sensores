import psutil as ps


class Registro:
    sensor: str
    unidade: str
    valor: float
    usoCpu: float
    usoMemoria: float

    def __init__(self, sensor: str, unidade: str, valor: float) -> None:
        self.sensor = sensor
        self.unidade = unidade
        self.valor = valor
        self.usoCpu = ps.cpu_percent()
        self.usoMemoria = ps.virtual_memory().percent


    def __repr__(self) -> str:
        return f"{self.sensor}: {self.valor} {self.unidade} | cpu: {self.usoCpu} | memory: {self.usoMemoria}"

    def to_json(self) -> dict:
        return {
            "deviceID": "eda-watson",
            # "sensor": self.sensor,
            "valueType": self.unidade,
            "value": self.valor
        }
    
    def addPcMonitoring(self, cpu: float, memory: float):
        self.usoCpu = cpu,
        self.usoMemoria = memory