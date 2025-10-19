from datetime import datetime, timedelta
import numpy as np
import pandas as pd
from pandas import DatetimeIndex


class GeradorTensao:

    TENSAO_NOMINAL = 127
    zonas: list[str]

    def __init__(self, zonas: list[str]):
        self.zonas = zonas

    def gerar_dados_zonas(self, inicio: datetime, fim: datetime) -> list[dict]:
        timestamps = pd.date_range(start=inicio, end=fim, freq='h')
        dados_totais = []
        for z in self.zonas:
            dados_brutos = self._gerar_vals_numericos(len(timestamps))
            dados_totais.extend(self._encapsular_dados(dados_brutos,timestamps,z))

        return dados_totais

    def setup_inicial(self, dias: int) -> list[dict]:
        fim = datetime.now()
        inicio = fim - timedelta(days=dias)
        return self.gerar_dados_zonas(inicio, fim)

    @staticmethod
    def _gerar_vals_numericos(horas) -> np.ndarray:
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

        tensao_final = GeradorTensao.TENSAO_NOMINAL + variacao_aleatoria + padrao_diario + eventos_extremos
        return tensao_final

    def _encapsular_dados(self, vals_numericos: np.ndarray, timestamps: DatetimeIndex, zona: str) -> list[dict]:
        dados_encapsul = []
        for val, ts in zip(vals_numericos, timestamps):
            dados_encapsul.append({'timestamp': ts, 'valor': val, 'zona': zona})
        return dados_encapsul