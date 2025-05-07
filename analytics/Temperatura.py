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
    plt.title("Gráfico de Temperatura do sensor IR MLX90614")
    plt.xlabel("Tempo")
    plt.ylabel("Temperatura (°C)")

    media = sum(dados_y) / len(dados_y)
    num_picos = sum(1 for temp in dados_y if temp >= 100)

    plt.axhline(70, color='green', linestyle='-', linewidth=2, label='Normal (70°C)')
    plt.axhline(100, color='red', linestyle='-', linewidth=2, label='Muito Quente (100°C)')
    plt.axhline(media, color='purple', linestyle='-', linewidth=2,
                label=f'Média ({media:.2f}°C)')

    plt.legend(title=f'Picos >100°C: {num_picos} ocorrências')
    plt.tight_layout()
    plt.savefig("grafico_temperatura.png")
    plt.show()

if __name__ == "__main__":
    gerar_grafico_temperatura()
