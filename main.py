from datetime import datetime
import json
import os
from math import floor
from time import sleep
import dotenv
from tqdm import tqdm
from azure_helper import AzureHelper
from interfaces.EnumCenarios import EnumCenarios
from sensores import Corrente, Frequencia, Harmonica, Potencia, Temperatura, Tensao

def obter_dados_cenario(quantidade: int, cenario: EnumCenarios):
    dados = []
    sensores = [Corrente, Frequencia, Harmonica, Potencia, Tensao, Temperatura]

    for s in sensores:
        dados.extend(s().gerar_dados(quantidade, cenario))

    return dados

def salvar_local(dados: list[dict]):
    path = "./logs"
    filename = f"generation-{datetime.now().strftime("%d-%m-%Y_%H-%M-%S .%f")[:-3]}.json"

    if not os.path.exists(path):
        os.mkdir(path)

    with open(f"{path}/{filename}", 'w') as f:
        json.dump([dict(d) for d in dados], f, indent=4)
    print("\t[😃] Sucesso!")

if __name__ == "__main__":
    print("GERADOR DE DADOS ALGAS")
    print("Versão 3.0")
    print()
    dotenv.load_dotenv()

    send_to_azure = os.getenv("SENT_TO_AZURE", "0") == "1"
    record_logs = os.getenv("RECORD_LOGS", "0") == "1"
    gen_timeout = int(os.getenv("GENERATION_TIMEOUT"))
    package_length = int(os.getenv("PACKAGE_DATA_LENGTH", "0"))

    azh = None
    if send_to_azure:
        print()
        azh = AzureHelper()
        print()

    cenarios = [EnumCenarios.TERRIVEL, EnumCenarios.NORMAL, EnumCenarios.EXCEPCIONAL]
    while True:

        print("\tGerando dados...")
        dados_simulados = []
        for c in cenarios:
            dados_simulados.extend(obter_dados_cenario(floor(package_length / len(cenarios)), c))

        if azh is not None:
            print("\n\tEnviando dados para Azure...")
            azh.send_data(dados_simulados)

        if record_logs:
            print("\n\tGravando dados para locamente...")
            salvar_local(dados_simulados)

        print("\n")
        for _ in tqdm(range(0, gen_timeout), desc="\tSegundos para a próxima geração"):
            sleep(1)
        print("\n")