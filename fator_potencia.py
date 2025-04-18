import random
import numpy as np
def gerar_dados_fator_potencia():
    # Geração da tensão, corrente e cálculo da potencia aparente
    tensao = round(random.uniform(80, 260), 1)
    corrente = round(random.uniform(0, 100), 2)
    potencia_aparente = round(tensao * corrente, 1)

    # Variáveis para simulação do fator de potencia
    fp_media = 0.97
    desvio_padrao_fp = 0.03
    porcent = random.random()
    prob_critica = 0.03
    prob_alerta = 0.08

    # Logica para casos
    if porcent < prob_critica:
        fator_potencia = round(random.uniform(0.60, 0.80), 3)
    elif porcent < prob_critica + prob_alerta:
        fator_potencia = round(random.uniform(0.80, 0.92), 3)
    else:
        fator_potencia = np.random.normal(loc=fp_media, scale=desvio_padrao_fp)
        fator_potencia = np.clip(fator_potencia, 0, 1)

    fator_potencia = float(round(fator_potencia, 2))

    return {
        "Potencia": potencia_aparente,
        "Fator de potência": fator_potencia
    }

gerar_dados_fator_potencia()
