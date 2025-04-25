import random
import math

def gerar_dados_pzem():
    tensao = round(random.uniform(80, 260), 1)
    corrente = round(random.uniform(0, 100), 2)
    potencia_aparente = round(tensao * corrente, 1)
    fator_potencia = round(random.uniform(0.5, 1.0), 2)

    return {
        "Potência ": potencia_aparente,
        "Fator de Potência": fator_potencia
    }

gerar_dados_pzem()
