import numpy as np

class Tensao:
    nome_sensor: str
    unidade: str
    TENSAO_NOMINAL = 127

    def __init__(self) -> None:
        self.nome_sensor = "Tensão"
        self.unidade = "volts"

    def gerar_dados(self, horas) -> np.ndarray:
        tempo = np.arange(horas)

        variacao_aleatoria = np.random.normal(0, 3, horas)
        padrao_diario = 5 * np.sin(2 * np.pi * tempo / 24)

        eventos_extremos = np.zeros(horas)
        n_eventos = max(1, int(horas * 0.05))

        for _ in range(n_eventos):
            inicio_evento = np.random.randint(0, horas - 1)

            duracao = int(np.random.normal(2, 1))
            duracao = max(1, min(18, duracao))
            fim_evento = min(inicio_evento + duracao, horas)

            if np.random.random() < 0.6:
                magnitude = -np.random.uniform(20,40)
            else:
                magnitude = np.random.uniform(15,30)

            eventos_extremos[inicio_evento:fim_evento] = magnitude

        tensao_final = self.TENSAO_NOMINAL + variacao_aleatoria + padrao_diario + eventos_extremos
        return tensao_final