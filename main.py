from datetime import datetime, timedelta
import json
import os
import dotenv
import pandas as pd
import requests
from time import sleep
from tqdm import tqdm
from aws_helper import AwsHelper
from interfaces.EnumZonas import EnumZonas
from sensores.Tensao import Tensao

def salvar_local(dados: list[dict]):
    path = "./logs"
    filename = "generation-{}.json".format(datetime.now().strftime("%d-%m-%Y_%H-%M-%S .%f")[:-3])

    if not os.path.exists(path):
        os.mkdir(path)

    with open(f"{path}/{filename}", 'w') as f:
        json.dump([dict(d) for d in dados], f, indent=4)
    print("\t[😃] Sucesso!")

def gerenciar_arquivo_root(diretorio:str):
    if not os.path.exists(diretorio):
        os.makedirs(diretorio)

    if not os.path.exists(f'{diretorio}/AmazonRootCA1.pem'):
        try:
            root_ca1_url = "https://www.amazontrust.com/repository/AmazonRootCA1.pem"
            response = requests.get(root_ca1_url)
            response.raise_for_status()
            with open('archives/AmazonRootCA1.pem','wb') as file:
                file.write(response.content)
                print('Arquivo ROOT CA1 da Amazon baixado com sucesso!')
        except requests.exceptions.RequestException as e:
            print(f'Ocorreu um erro na chamada:{e}')
    else:
        print(f'Arquivo ROOT CA1 da Amazon já existe no diretorio: {diretorio}')

if __name__ == "__main__":
    print("GERADOR DE DADOS ALGAS")
    print("Versão 4.0")
    print()
    dotenv.load_dotenv()

    send_to_aws = os.getenv("SENT_TO_AWS", "0") == "1"
    record_logs = os.getenv("RECORD_LOGS", "0") == "1"
    gen_timeout = int(os.getenv("GENERATION_TIMEOUT"))

    gerenciar_arquivo_root('archives')

    aws = None
    if send_to_aws:
        aws = AwsHelper()
        print('Instância preparada para envio de dados criada!')

    zonas = [ez.name for ez in EnumZonas]
    tensao = Tensao()

    fim = datetime.now()
    inicio = fim - timedelta(days=14)
    timestamps = pd.date_range(start=inicio, end=fim, freq='h')
    horas = len(timestamps)

    setup_inicial = {}
    for z in zonas:
        setup_inicial[z] = tensao.gerar_dados(horas)

    inicio = datetime.now()
    while True:
        print("\tGerando dados...")
        fim = inicio + timedelta(days=1)
        timestamps = pd.date_range(start=inicio, end=fim, freq='h')
        horas = len(timestamps)

        dados_zonas = {}
        for z in zonas:
            dados_zonas[z] = tensao.gerar_dados(horas)
        
        # if aws is not None:
        #     print("\n\tEnviando dados para Iot Core...")
        #     aws.send_data(dados_gerados)
        #
        # if record_logs:
        #     print("\n\tGravando dados para locamente...")
        #     salvar_local(dados_gerados)

        print(dados_zonas)
        print("\n")
        for _ in tqdm(range(0, gen_timeout), desc="\tSegundos para a próxima geração"):
            sleep(1)
        print("\n")