import json
import matplotlib.pyplot as plt

def gerar_grafico_temperatura():
    dados_x = []
    dados_y = []
    with open('dados.json') as f:
        for line in f:
            item = json.loads(line)
            if item['valueType'] == 'Â°C' or item['valueType'] == '°C':
                dados_x.append(item['EventProcessedUtcTime'])
                dados_y.append(item['value'])

    plt.plot(dados_x, dados_y, color='orange', linewidth=1)
    plt.title("Gráfico de Temperatura")
    plt.xlabel("Tempo")
    plt.ylabel("Temperatura (°C)")

    plt.axhline(70, color='green', linestyle='-', linewidth=2, label='Frio (Normal)')
    plt.axhline(100, color='red', linestyle='-', linewidth=2, label='Muito Quente (Crítico)')

    media = sum(dados_y) / len(dados_y)

    plt.axhline(media, color='purple', linestyle='-', linewidth=2, label='Média')
    plt.legend()
    # plt.xticks(rotation=45)
    # plt.tight_layout()
    plt.savefig("grafico_temperatura.png")
    plt.show()

if __name__ == "__main__":
    gerar_grafico_temperatura()
