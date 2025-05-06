import json
import numpy as np
import matplotlib.pyplot as plt

class Corrente():
    def gerar_grafico(self):        
        dados = []
        with open('dados.json') as f:
            for line in f:
                item = json.loads(line)
                if(item['valueType'][0] == 'a'):
                    dados.append(item['value'])

        filtered_data = {
        "Normal": np.array([dados[i] for i in range(0, len(dados)) if dados[i] == 5]),
        "Terrivel": np.array([dados[i] for i in range(0, len(dados)) if dados[i] > 5]),
        "Excepcional": np.array([dados[i] for i in range(0, len(dados)) if dados[i] < 5])
        }
        down_size = int(min(len(filtered_data['Terrivel']), len(filtered_data['Excepcional']))*2)
        if filtered_data['Normal'].size > down_size:
            filtered_data['Normal'] = np.random.choice(filtered_data['Normal'], size=down_size, replace=False)

        x_normal = range(len(filtered_data['Normal']))
        x_terrivel = range(len(filtered_data['Terrivel']))
        x_excepcional = range(len(filtered_data['Excepcional']))
        plt.scatter(x_normal,filtered_data['Normal'],label='Normal')
        plt.scatter(x_terrivel,filtered_data['Terrivel'],label='Terrivel')
        plt.scatter(x_excepcional,filtered_data['Excepcional'],label='Excepcional')

        plt.xlabel('índice')
        plt.ylabel('Amperes')
        plt.title('Scatter Plot - Ampere')
        plt.grid(True)
        plt.axhline(y=5, color='gray', linestyle='--', label='Limite normal')
        desvios_negativos = np.abs(filtered_data["Terrivel"] - 5)
        plt.scatter(range(len(desvios_negativos)), filtered_data["Terrivel"], c=desvios_negativos, cmap='Reds', label='Tolerável acima de 5A')
        desvios_toleraveis = np.abs(filtered_data["Excepcional"] - 5)
        plt.scatter(range(len(desvios_toleraveis)), filtered_data["Excepcional"], c=desvios_toleraveis, cmap='Greens', label='Tolerável abaixo de 5A')
        # print(np.mean(filtered_data['Terrivel']),'\n',np.mean(filtered_data['Normal']),'\n',np.mean(filtered_data['Excepcional']))
        
        plt.legend()
        plt.show()

         
if __name__ == "__main__":
    sensor = Corrente()
    sensor.gerar_grafico()
