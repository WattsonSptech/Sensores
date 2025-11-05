import os
import json
from datetime import datetime

class LocalFiles:

    @staticmethod
    def salvar_local(dados: list[dict]):
        print("\n\tGravando dados para locamente...")
        path = "./logs"
        filename = "telemetry-{}.json".format(datetime.now().strftime("%d-%m-%Y_%H-%M-%S .%f")[:-3])

        if not os.path.exists(path):
            os.mkdir(path)

        with open(f"{path}/{filename}", 'w') as f:
            json.dump([dict(d) for d in dados], f, indent=4)
        print("\t[😃] Sucesso!")
