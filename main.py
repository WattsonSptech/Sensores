from datetime import datetime
import json
import os
from math import floor
from time import sleep
import dotenv
from tqdm import tqdm
import requests
from aws_helper import AwsHelper
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
    package_length = int(os.getenv("PACKAGE_DATA_LENGTH", "0"))

    gerenciar_arquivo_root('archives')

    aws = None
    if send_to_aws:
        aws = AwsHelper()
        print('Instância preparada para envio de dados criada!')

    #cenarios = [EnumCenarios.TERRIVEL, EnumCenarios.NORMAL, EnumCenarios.EXCEPCIONAL]
    cenarios = [EnumCenarios.NORMAL]
    while True:
        print("\tGerando dados...")
        dados_simulados = []
        for c in cenarios:
            dados_simulados.extend(obter_dados_cenario(floor(package_length / len(cenarios)), c))
        
        if aws is not None:
            print("\n\tEnviando dados para Iot Core...")
            aws.send_data(dados_simulados)

        if record_logs:
            print("\n\tGravando dados para locamente...")
            salvar_local(dados_simulados)

        print("\n")
        for _ in tqdm(range(0, gen_timeout), desc="\tSegundos para a próxima geração"):
            sleep(1)
        print("\n")