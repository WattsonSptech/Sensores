import json
import matplotlib.pyplot as plot
from datetime import datetime

dados_y = []
qtd_aceitavel = 0
qtd_ruim = 0
qtd_critica = 0

with open('dados.json') as f:
    for line in f:
        item = json.loads(line)
        if item['valueType'] == 'watts':
            dados_y.append(item['value'])

            if item['value'] > 0.92:
                qtd_aceitavel += 1
            elif item['value'] > 0.70:
                qtd_ruim += 1
            else:
                qtd_critica += 1

fig, (ax1, ax2) = plot.subplots(1, 2, figsize=(12, 5))

ax1.plot(range(len(dados_y)), dados_y)
ax1.set_title("Gráfico Fator de Potência")
ax1.set_xlabel("Variação de Tempo")
ax1.set_ylabel("Valor (%)")

labels = ['Aceitável', 'Ruim', 'Crítico']
sizes = [qtd_aceitavel, qtd_ruim, qtd_critica]
colors = ['#8ac926', '#ffca3a', '#ff595e']

ax2.pie(
    sizes,
    colors=['#8ac926', '#ffca3a', '#ff595e'],
    autopct='%1.1f%%',
    textprops={'size': 'smaller'},
    radius=1
)

ax2.legend(labels, 
          title="Cenarios",
          loc="lower right",
          bbox_to_anchor=(1.2, 0)
          )

ax2.set_title("Gráfico Cenários")

# Ajuste de layout
plot.tight_layout()
plot.show()
