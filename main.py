from sensores.Corrente import Corrente
from sensores.Harmonica import Harmonica
from sensores.Potencia import Potencia
from sensores.Tensao import Tensao

Corrente().gerar_dados(5)
Harmonica().gerar_dados(5)
Potencia().gerar_dados(5)
Tensao().gerar_dados(5)