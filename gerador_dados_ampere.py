import time
import os
import random

def calculate_current():
  max_current = 800
  enroll_proportion = 160
  primary_current = round(random.randint(16, max_current), 4)

  percentual = primary_current/max_current*100
  if percentual > 5 and percentual <= 120:
    secundary_current = 5
  elif percentual >= 2.5 and percentual < 5:
    secundary_current = round(primary_current/enroll_proportion, 2)
  else:
    secundary_current = round(primary_current/enroll_proportion, 2)
 

  time.strftime('%H:%M:%S')
  os.environ['TZ'] = 'America/Sao Paulo'
  format_time = time.strftime('%H:%M:%S')

  return {
        "valor_leitura": {
            "corrente_primaria": primary_current,
            "corrente_secundaria": secundary_current,
            "tempo": format_time
        },
        "tipo_dado": {
            "nome": "Ampere"
        },
        "sensor": {
            "nome": 'RCI-32'
        }
    }

print(calculate_current())


  