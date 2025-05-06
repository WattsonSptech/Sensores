
import json
import matplotlib.pyplot as plt
    
def gerar_grafico():
    dados_x = []
    dados_y = []
    with open('dados.json') as f:
        for line in f:
            item = json.loads(line)
            if(item['valueType'] == 'Porcentagem'):
                dados_x.append(item['EventProcessedUtcTime'])
                dados_y.append(item['value'])
    
    plt.plot(dados_x, dados_y, color='blue', linewidth=1)
    plt.title("Gráfico Harmônicas")
    plt.xlabel("Variação de Tempo")
    plt.ylabel("Valor (%)")
    plt.axhline(1, color='green', linestyle='-', linewidth=2, label='Estado Excelente')
    plt.axhline(5, color='yellow', linestyle='-', linewidth=2, label='Estado Normal')
    plt.axhline(100, color='red', linestyle='-', linewidth=2, label='Estado Terrível')
    plt.axhline((sum(dados_y)/len(dados_y)), color='purple', linestyle='-', linewidth=2, label='Média')
    plt.legend()
    plt.show()

    
if __name__ == "__main__":
    gerar_grafico()